from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for AccessRequestsAPI.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = None  # type: ignore[assignment]
    last_name = None  # type: ignore[assignment]

    class Role(models.TextChoices):
        EMPLOYEE = 'EMPLOYEE', _('Employee')
        MANAGER = 'MANAGER', _('Manager')
        ADMIN = 'ADMIN', _('Admin')

    department = CharField(_("Department"), max_length=100, blank=True)
    role = CharField(_("Role"), max_length=20, choices=Role.choices, default=Role.EMPLOYEE)

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
