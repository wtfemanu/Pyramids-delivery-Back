"""
Database models.
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Manager for users."""

    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('Users must have an email address.')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create, save and return a new superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User model in the system."""

    email = models.EmailField(max_length=255, unique=True, verbose_name=_('email'), help_text=_('Email'))
    username = models.CharField(max_length=255, unique=True, blank=True, null=True, verbose_name=_('username'), help_text=_('Username'))
    first_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Nome'), help_text=_('Nome'))
    last_name = models.CharField(max_length=255, blank=True, null=True, verbose_name=_('Sobrenome'), help_text=_('Sobrenome'))
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True, verbose_name=_('Foto de Perfil'))
    
    is_active = models.BooleanField(
        default=True, verbose_name=_('Usuário está ativo'), help_text=_('Indica que este usuário está ativo.')
    )
    is_staff = models.BooleanField(
        default=False,
        verbose_name=_('Usuário é da equipe'),
        help_text=_('Indica que este usuário pode acessar o Admin.'),
    )

    objects = UserManager()

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['username'] # Campos obrigatórios ao criar via terminal

    class Meta:
        """Meta options for the model."""

        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'