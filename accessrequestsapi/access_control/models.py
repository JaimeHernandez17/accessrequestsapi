from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

class System(models.Model):
    class Criticality(models.TextChoices):
        LOW = 'LOW', _('Low')
        MEDIUM = 'MEDIUM', _('Medium')
        HIGH = 'HIGH', _('High')

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    criticality = models.CharField(max_length=10, choices=Criticality.choices, default=Criticality.LOW)

    def __str__(self):
        return f"{self.name} ({self.code})"

class AccessRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', _('Pending')
        APPROVED = 'APPROVED', _('Approved')
        REJECTED = 'REJECTED', _('Rejected')

    requester = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='access_requests')
    system = models.ForeignKey(System, on_delete=models.CASCADE, related_name='access_requests')
    reason = models.TextField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    acted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='acted_requests')
    acted_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.requester} -> {self.system} ({self.status})"

class AuditLog(models.Model):
    request = models.ForeignKey(AccessRequest, on_delete=models.CASCADE, related_name='audit_logs')
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    old_status = models.CharField(max_length=10)
    new_status = models.CharField(max_length=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audit {self.request.id}: {self.old_status} -> {self.new_status}"
