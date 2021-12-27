import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import RegexValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManger(BaseUserManager):
    """Manager for working with user creations"""

    def create_user(self, email, password, **extra_fields):
        """Creating an user"""
        if not email:
            raise ValueError(_('Email is required'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Creating a superuser"""
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff', False):
            raise ValueError('Superuser must have is_staff=True.')

        if not extra_fields.get('is_superuser', False):
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """Class for creating a custom table in a db"""

    GENDER_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female'))
    )

    id = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
        unique=True,
        help_text=_('format: required, unique'),
        verbose_name=_('id for user'),
    )
    email = models.EmailField(
        max_length=128,
        unique=True,
        help_text=_(
            'format: max-128, required, unique'
        ),
        verbose_name=_("user's email")
    )
    first_name = models.CharField(
        max_length=128,
        help_text=_(
            'format: max-128, required'
        ),
        verbose_name=_("user's name")
    )
    last_name = models.CharField(
        max_length=128,
        help_text=_(
            'format: max-128, required'
        ),
        verbose_name=_("user's last name")
    )
    dob = models.DateField(
        help_text=_(
            'format: Y-m-d'
        ),
        verbose_name=_("user's date of birth")
    )
    phone_regex = RegexValidator(
        regex=r'\A\+998\d{9}\Z',
        message=_('Phone number must be entered in the format: "+998 ** *** ** **".Up to the 12 digits allowed.')
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=13,
        unique=True,
        help_text=_(
            'format: max-13, required, unique'
        ),
        verbose_name=_("user's phone number"),
    )
    gender = models.CharField(
        choices=GENDER_CHOICES,
        max_length=1,
        help_text=_(
            'format: required'
        ),
        verbose_name=_("user's gender"),
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('user creation date'),
        help_text=_('format: Y-m-d H:M:S'),
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('user update date'),
        help_text=_('format: Y-m-d H:M:S')
    )
    is_active = models.BooleanField(
        default=True,
        help_text=_('format: true=user visible'),
        verbose_name=_('user visibility')
    )
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'dob', 'phone_number', 'gender']

    object = UserManger()

    class Meta:
        unique_together = ('last_name', 'first_name')
        verbose_name = _('User')
        verbose_name_plural = _('Users')

    def __str__(self):
        return str(self.email)


class UserImage(models.Model):
    """Class for creation an image fields table in a database"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(
        upload_to='images/users/%Y/%m/%d',
        help_text=_(
            'format: required'
        ),
        verbose_name=_("user's image")
    )
    alt_text = models.CharField(
        max_length=128,
        default=_("user's image"),
        verbose_name=_('alternative text'),
        help_text=_('format: max-128, required')
    )

    class Meta:
        verbose_name = _("image")
        verbose_name_plural = _("images")

    def __str__(self):
        return str(self.id)


class Address(models.Model):
    """Class for creating a profile table in a db"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='addresses'
    )
    country = models.CharField(
        max_length=128,
        help_text=_(
            'format: max-128, required'
        ),
        verbose_name=_('country')
    )
    city = models.CharField(
        max_length=128,
        help_text=_(
            'format: max-128, required'
        ),
        verbose_name=_('city')
    )
    street = models.CharField(
        max_length=128,
        help_text=_(
            'format: max-128, required'
        ),
        verbose_name=_('street')
    )
    apartment = models.TextField(
        blank=False,
        null=False,
        help_text=_(
            'format: required',
        ),
        verbose_name=_('apartment')
    )
    is_default = models.BooleanField(default=False)

    class Meta:
        verbose_name = _('Address')
        verbose_name_plural = _('Addresses')

    def __str__(self):
        return str(self.user.email)
