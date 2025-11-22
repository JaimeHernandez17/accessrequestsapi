from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from django.db.models import Q
from accessrequestsapi.access_control.models import System, AccessRequest, AuditLog
from accessrequestsapi.access_control.api.serializers import SystemSerializer, AccessRequestSerializer
from accessrequestsapi.users.models import User
from accessrequestsapi.access_control.permissions import IsEmployee, IsManager, IsAdmin

class SystemViewSet(viewsets.ModelViewSet):
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

class AccessRequestViewSet(viewsets.ModelViewSet):
    serializer_class = AccessRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == User.Role.ADMIN:
            return AccessRequest.objects.all()
        elif user.role == User.Role.MANAGER:
            # Manager sees requests from their department
            return AccessRequest.objects.filter(requester__department=user.department)
        else:
            # Employee sees only their own requests
            return AccessRequest.objects.filter(requester=user)

    def perform_create(self, serializer):
        serializer.save(requester=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def approve(self, request, pk=None):
        return self._update_status(request, AccessRequest.Status.APPROVED)

    @action(detail=True, methods=['post'], permission_classes=[IsManager | IsAdmin])
    def reject(self, request, pk=None):
        return self._update_status(request, AccessRequest.Status.REJECTED)

    def _update_status(self, request, new_status):
        access_request = self.get_object()
        
        # Manager check: must be same department
        if request.user.role == User.Role.MANAGER:
            if access_request.requester.department != request.user.department:
                return Response({"detail": "You can only act on requests from your department."}, status=status.HTTP_403_FORBIDDEN)

        old_status = access_request.status
        access_request.status = new_status
        access_request.acted_by = request.user
        access_request.acted_at = timezone.now()
        access_request.save()

        # Audit Log
        AuditLog.objects.create(
            request=access_request,
            performed_by=request.user,
            old_status=old_status,
            new_status=new_status
        )

        return Response(AccessRequestSerializer(access_request, context={'request': request}).data)
