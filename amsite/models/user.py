import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # FIXME: we should not redefine fields and must inherit AbstractBaseUser and PermissionsMixin instead
    username_validator = None

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists.")
        }
    )

    age = models.PositiveIntegerField(_('age'), null=True, blank=True)
    phone = models.CharField(_('phone number'), max_length=15, blank=True)
    region = models.CharField(_('region'), max_length=30, blank=True)
