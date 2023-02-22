from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _

from .managers import UserManager
from .storages import PublicMediaStorage


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    first_name = models.CharField(_('nome'), max_length=30, blank=True)
    last_name = models.CharField(_('sobrenome'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('data de ingresso'), auto_now_add=True)
    is_active = models.BooleanField(_('ativo'), default=True)
    is_staff = models.BooleanField(_('equipe'), default=False)
    avatar = models.ImageField(storage=PublicMediaStorage(), null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('usuário')
        verbose_name_plural = _('usuários')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return '{} {}'.format(self.first_name, self.last_name).strip()

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)