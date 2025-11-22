from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import AccessRequest, AuditLog, System


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "criticality")
    list_filter = ("criticality",)
    search_fields = ("name", "code")


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "requester",
        "system",
        "status",
        "created_at",
        "updated_at",
    )
    list_filter = ("status", "created_at", "updated_at")
    search_fields = ("requester__username", "requester__email", "system", "reason")
    readonly_fields = ("created_at", "updated_at")
    date_hierarchy = "created_at"
    ordering = ("-created_at",)

    fieldsets = (
        (None, {"fields": ("requester", "system", "reason", "status")}),
        (
            _("Fechas"),
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "request",
        "performed_by",
        "timestamp",
    )
    list_filter = ("timestamp",)
    search_fields = (
        "request__id",
        "performed_by__username",
        "performed_by__email",
    )
    readonly_fields = ("timestamp",)
    date_hierarchy = "timestamp"
    ordering = ("-timestamp",)

    fieldsets = (
        (None, {"fields": ("request", "performed_by")}),
        (_("Detalles"), {"fields": ("old_status", "new_status")}),
        (_("Marca de tiempo"), {"fields": ("timestamp",)}),
    )
