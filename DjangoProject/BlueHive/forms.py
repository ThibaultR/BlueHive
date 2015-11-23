from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from models import CustomUser
from models import Event
from models import UserGroup
from models import EventRequest
from models import NewProfilePicture
from django.contrib.auth.forms import ReadOnlyPasswordHashField

MY_DATE_FORMATS = ['%d.%m.%Y',]


class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        #self.fields["language"].widget = forms.CheckboxSelectMultiple()
        #self.fields["language"].help_text = ""
        #del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone_number', 'birth_date', 'social_security_number', 'address', 'zip_code',
                  'city', 'nationality', 'education', 'job_position', 'work_experience', 'language', 'license', 'profile_picture']
        widgets = {'language': forms.CheckboxSelectMultiple, 'license': forms.CheckboxSelectMultiple, 'birth_date': forms.DateInput()}



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
        exclude = ['date_created', 'rating', 'user_type', 'passport_issue_date', 'passport_expiration_date', 'user_group']
        widgets = {'language': forms.CheckboxSelectMultiple, 'license': forms.CheckboxSelectMultiple, 'birth_date': forms.DateInput}


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


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        exclude = ['status']
        #fields = '__all__'


class EventRequestForm(forms.ModelForm):

    class Meta:
        model = EventRequest
        #exclude = ['status']
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


