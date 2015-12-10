from datetime import datetime

from django import forms
from django.forms import extras
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from BlueHive.models import CustomUser, Event, UserGroup, EventRequest, NewProfilePicture
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from django.contrib.auth.forms import ReadOnlyPasswordHashField

MY_DATE_FORMATS = ['%d.%m.%Y', ]


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        # self.fields["language"].widget = forms.CheckboxSelectMultiple()
        # self.fields["language"].help_text = ""
        # del self.fields['username']

    class Meta:
        model = CustomUser

        fields = ['email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'social_security_number', 'address',
                  'zip_code',
                  'city', 'nationality', 'education', 'job_position', 'work_experience', 'language', 'license',
                  'profile_picture']
        widgets = {'language': forms.CheckboxSelectMultiple,
                   'license': forms.CheckboxSelectMultiple,
                   'birth_date': extras.SelectDateWidget(years=range(datetime.now().year - 70,
                                                                     datetime.now().year - 14))
                   }


class CustomUserChangeForm(UserChangeForm):
    """A form for updating users.
    Includes all the fields on the user, but replaces the password field
    with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label="Password", help_text=(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = CustomUser
        exclude = ['date_created', 'rating', 'user_type', 'passport_issue_date', 'passport_expiration_date',
                   'user_group', 'account_status', 'email']
        widgets = {'language': forms.CheckboxSelectMultiple, 'license': forms.CheckboxSelectMultiple,
                   'birth_date': extras.SelectDateWidget(years=range(datetime.now().year - 70,
                                                                     datetime.now().year - 14))
                   }

    def __init__(self, *args, **kwargs):
        """Init the form."""
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        """Clean password.
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.
        :return str password:
        """
        return self.initial["password"]


class UserChangePasswordForm(forms.Form):
    """
    A form that lets a user change their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields were not matching."),
        'password_incorrect': ("Your old password was entered incorrectly. "
                               "Please enter it again."),
    }
    old_password = forms.CharField(label=("Old password"),
                                   widget=forms.PasswordInput,
                                   required=False)
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput,
                                    required=False)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput,
                                    required=False)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserChangePasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password


class AdminChangePasswordForm(forms.Form):
    """
    A form that lets a user change their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields were not matching."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput,
                                    required=False)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput,
                                    required=False)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2


class AdminCustomUserChangeForm(UserChangeForm):
    """A form for updating users.
    Includes all the fields on the user, but replaces the password field
    with admin's password hash display field.
    """

    password = ReadOnlyPasswordHashField(label="Password", help_text=(
        "Raw passwords are not stored, so there is no way to see "
        "this user's password, but you can change the password "
        "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = CustomUser
        dateOptions = {
            'format': 'yyyy-mm-dd',
            'endDate': datetime.now().strftime('%Y-%m-%d'),
            'autoclose': True,
            'showMeridian' : True
        }
        exclude = ['date_created', 'user_type', 'passport_issue_date', 'passport_expiration_date', 'account_status']
        widgets = {'language': forms.CheckboxSelectMultiple,
                   'license': forms.CheckboxSelectMultiple,
                   'user_group': forms.CheckboxSelectMultiple,
                   'birth_date': extras.SelectDateWidget(years=range(datetime.now().year - 70,
                                                                     datetime.now().year - 14))
                   }

    def __init__(self, *args, **kwargs):
        """Init the form."""
        super(AdminCustomUserChangeForm, self).__init__(*args, **kwargs)

    def clean_password(self):
        """Clean password.
        Regardless of what the user provides, return the initial value.
        This is done here, rather than on the field, because the
        field does not have access to the initial value.
        :return str password:
        """
        return self.initial["password"]


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude = ['status']
        #TODO validate that date is not in past also in the backend
        dateTimeOptions = {
            'format': 'yyyy-mm-dd hh:ii',
            'startDate': datetime.now().strftime('%Y-%m-%d'),
            'autoclose': True,
            'showMeridian' : True
        }

        # fields = '__all__'
        widgets = {'description': forms.Textarea(attrs={'rows': 4}),
                   'begin_time': DateTimeWidget(options=dateTimeOptions, bootstrap_version=3)}



class EventRequestForm(forms.ModelForm):
    class Meta:
        model = EventRequest
        # exclude = ['status']
        fields = ['event_id', 'user_id', 'user_comment']


class UserGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        """Init the form."""
        super(UserGroupForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserGroup
        fields = '__all__'


class NewProfilePictureForm(forms.ModelForm):
    class Meta:
        model = NewProfilePicture
        exclude = ['user_id']
