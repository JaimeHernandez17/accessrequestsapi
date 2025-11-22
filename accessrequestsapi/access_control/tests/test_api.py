import pytest
from rest_framework.test import APIClient
from rest_framework import status
from accessrequestsapi.users.models import User
from accessrequestsapi.access_control.models import System, AccessRequest, AuditLog

@pytest.mark.django_db
class TestAccessRequests:
    def setup_method(self):
        self.client = APIClient()
        
        # Users
        self.employee = User.objects.create_user(username='emp', email='emp@example.com', password='password', role=User.Role.EMPLOYEE, department='IT')
        self.manager = User.objects.create_user(username='mgr', email='mgr@example.com', password='password', role=User.Role.MANAGER, department='IT')
        self.admin = User.objects.create_user(username='adm', email='adm@example.com', password='password', role=User.Role.ADMIN, department='HR')
        
        # System
        self.system = System.objects.create(name='ERP', code='ERP01', criticality=System.Criticality.HIGH)

    def test_employee_create_request(self):
        self.client.force_authenticate(user=self.employee)
        data = {'system': self.system.id, 'reason': 'Need access'}
        response = self.client.post('/api/access-requests/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert AccessRequest.objects.count() == 1
        assert AccessRequest.objects.first().requester == self.employee

    def test_employee_approve_fail(self):
        req = AccessRequest.objects.create(requester=self.employee, system=self.system, reason='Test')
        self.client.force_authenticate(user=self.employee)
        response = self.client.post(f'/api/access-requests/{req.id}/approve/')
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_manager_approve_success(self):
        req = AccessRequest.objects.create(requester=self.employee, system=self.system, reason='Test')
        self.client.force_authenticate(user=self.manager)
        response = self.client.post(f'/api/access-requests/{req.id}/approve/')
        assert response.status_code == status.HTTP_200_OK
        req.refresh_from_db()
        assert req.status == AccessRequest.Status.APPROVED
        assert req.acted_by == self.manager
        assert AuditLog.objects.count() == 1

    def test_manager_approve_other_dept_fail(self):
        other_emp = User.objects.create_user(username='other', email='other@example.com', password='password', role=User.Role.EMPLOYEE, department='HR')
        req = AccessRequest.objects.create(requester=other_emp, system=self.system, reason='Test')
        self.client.force_authenticate(user=self.manager) # IT Manager
        response = self.client.post(f'/api/access-requests/{req.id}/approve/')
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_admin_create_system(self):
        self.client.force_authenticate(user=self.admin)
        data = {'name': 'CRM', 'code': 'CRM01', 'criticality': 'LOW'}
        response = self.client.post('/api/systems/', data)
        assert response.status_code == status.HTTP_201_CREATED
        assert System.objects.count() == 2
