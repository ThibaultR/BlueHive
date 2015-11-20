from django.db import models
from django.utils import timezone
from django.utils.http import urlquote
from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.urlresolvers import reverse

class UserType(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)


class UserRating(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    value = models.IntegerField(default=0)
    description = models.CharField(max_length=254, blank=True)

class Nationality(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    code = models.CharField(max_length=254, blank=True)
    value = models.CharField(max_length=254, blank=True)

    def __unicode__(self):
        return unicode(self.value)

class Language(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=254)
    abbreviation =  models.CharField(max_length=20)

    def __unicode__(self):
        return unicode(self.value)

class License(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=254)
    description = models.CharField(max_length=254, blank=True)

    def __unicode__(self):
        return unicode(self.value)

class UserGroup(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    value = models.CharField(max_length=254)

    def __unicode__(self):
        return unicode(self.value)





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
    date_created = models.DateTimeField(_('date joined'), default=timezone.now)
    date_altered = models.DateTimeField(auto_now=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=False)
    last_name = models.CharField(_('last name'), max_length=30, blank=False)
    # -1 deactivated, 0 new user, 1 active user, 2 moderator, 3 administrator
    account_status = models.IntegerField(default= 0)
    user_group = models.ManyToManyField(UserGroup, default=1)
    rating = models.ForeignKey(UserRating, default=4)
    comment = models.CharField(max_length=254, blank=True)
    phone_number = models.IntegerField()
    birth_date = models.DateField()
    social_security_number = models.CharField(max_length=254)
    address = models.CharField(max_length=254)
    zip_code = models.CharField(max_length=254)
    city = models.CharField(max_length=254)
    nationality = models.ForeignKey(Nationality, default=198)
    education = models.CharField(max_length=254)
    job_position = models.CharField(max_length=254, blank=True)
    work_experience = models.CharField(max_length=254, blank=True)
    passport_number = models.CharField(max_length=254, blank=True)
    passport_authority = models.CharField(max_length=254, blank=True)
    passport_issue_date = models.DateField(null=True)
    passport_expiration_date = models.DateField(null=True)
    bank_name = models.CharField(max_length=254, blank=True)
    bank_iban = models.CharField(max_length=254, blank=True)
    bank_bic = models.CharField(max_length=254, blank=True)
    language = models.ManyToManyField(Language,  null=True, blank=True)
    license = models.ManyToManyField(License,  null=True, blank=True)
    #https://coderwall.com/p/bz0sng/simple-django-image-upload-to-model-imagefield
    image = models.ImageField(upload_to = 'user_pictures/', default = 'user_pictures/None/no-img.jpg')


    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin '
                                               'site.'))
    is_active = models.BooleanField(_('active'), default=True,
                                    help_text=_('Designates whether this user should be treated as '
                                                'active. Unselect this instead of deleting accounts.'))

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

    def __str__(self):              # __unicode__ on Python 2
        return self.email

class Event(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=254)
    comment = models.CharField(max_length=254, blank=True)
    description = models.TextField(max_length=254, blank=True)
    location = models.CharField(max_length=254)
    begin_time = models.DateTimeField()
    end_time = models.CharField(max_length=254)
    user_group = models.ForeignKey(UserGroup, default=1)
    #-1 killed, 0 nothing done, 1 users set, 2 times users set, 3 everything ok
    status = models.IntegerField(default=0)

    def __unicode__(self):
        return self.name


class EventRequest(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_altered = models.DateTimeField(auto_now=True)
    event_id = models.ForeignKey(Event)
    user_id = models.ForeignKey(CustomUser)
    user_comment = models.CharField(max_length=254, blank=True)
    # -1 rejected, 0 wait, 1 accepted
    status = models.IntegerField(default = 0)
    begin_time = models.CharField(default='', max_length=254, blank=True)
    end_time = models.CharField(default = '', max_length=254, blank=True)
    mail_sent = models.BooleanField(default = False)

    unique_together = ("event_id", "user_id")


class Author(models.Model):
    name = models.CharField(max_length=200)

    def get_absolute_url(self):
        return reverse('author-detail', kwargs={'pk': self.pk})



