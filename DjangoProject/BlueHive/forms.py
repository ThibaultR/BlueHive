from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from models import CustomUser
from models import Event

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
                  'city', 'nationality', 'education', 'job_position', 'work_experience', 'language', 'license', 'image']
        widgets = {'language': forms.CheckboxSelectMultiple, 'license': forms.CheckboxSelectMultiple, 'birth_date': forms.DateInput}



class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        #del self.fields['username']

    def save(self, commit=True):
        user = super(CustomUserChangeForm, self).save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = CustomUser
        exclude = ['last_login', 'date_joined', 'is_active', 'is_superuser', 'is_staff']
        fields = ['first_name', 'last_name', 'phone_number', 'birth_date', 'social_security_number', 'address', 'zip_code',
                  'city', 'nationality', 'education', 'job_position', 'work_experience', 'language', 'license', 'image']
        widgets = {'language': forms.CheckboxSelectMultiple, 'license': forms.CheckboxSelectMultiple, 'birth_date': forms.DateInput}


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'

