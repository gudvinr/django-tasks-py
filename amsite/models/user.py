from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # FIXME: we should not redefine fields and must inherit AbstractBaseUser and PermissionsMixin instead
    username_validator = None

    username = models.EmailField(
        _('email address'),
        unique=True,
        error_messages={
            'unique': _("A user with that email already exists.")
        }
    )
