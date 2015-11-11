from django import forms
from django.contrib.auth.models import User
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
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email",)

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = '__all__'

#Form inherits from UserCreationForm
class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Hold anything that isn't a form field
    class Meta:
        model = CustomUser
        fields = '__all__'

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()
        return user

class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = '__all__'

class UserProfileForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('email',)