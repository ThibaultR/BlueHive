from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager

'''https://www.caktusgroup.com/blog/2013/08/07/migrating-custom-user-model-django/'''
class CustomUserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    A fully featured User model with admin-compliant permissions that uses
    a full-length email field as the username.

    Email and password are required. Other fields are optional.
    """
    email = models.EmailField(_('email address'), max_length=254, unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return "/users/%s/" % urlquote(self.email)

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        "Returns the short name for the user."
        return self.first_name

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])


class Event(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    comment = models.CharField(max_length=254, blank=True)
    description = models.TextField(max_length=254, blank=True)
    location = models.CharField(max_length=254)
    begin_time = models.DateField
    end_time = models.CharField(max_length=254)
    #group_id as a FOREIGN KEY to the GROUPS
    #-1 killed, 0 nothing done, 1 users set, 2 times users set, 3 everything ok
    status = models.IntegerField

    def __unicode__(self):
        return self.name

class UserType(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)

class UserRating(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)
    description = models.CharField(max_length=254, blank=True)

class Language(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    abbreviation =  models.CharField(max_length=20)

class License(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True)

'''
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    user_type = models.ForeignKey(UserType)
    rating = models.ForeignKey(UserRating)
    comment = models.CharField(max_length=254, blank=True)
    phone_number = models.IntegerField(blank=True)
    birth_date = models.DateField()
    social_security_number = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    zip_code = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    nationality = models.CharField(max_length=254)
    education = models.CharField(max_length=254)
    job_position = models.CharField(max_length=254)
    work_experience = models.CharField(max_length=254)
    passport_number = models.CharField(max_length=254)
    passport_authority = models.CharField(max_length=254)
    passport_issue_date = models.DateField()
    passport_expiration_date = models.DateField()
    bank_name = models.CharField(max_length=254, blank=True)
    bank_iban = models.CharField(max_length=254, blank=True)
    bank_bic = models.CharField(max_length=254, blank=True)
'''


class UserLanguage(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(CustomUser)
    language_id = models.ForeignKey(Language)


class UserLicense(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(CustomUser)
    license_id = models.ForeignKey(License)




