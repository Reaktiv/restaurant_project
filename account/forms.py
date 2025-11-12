from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms.models import ModelForm

from account.models import CustomUser, Profile


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username' ,'phone', 'email', )
        labels = {'email': 'Elektron pochta', 'phone':'Telefoningiz'}
        help_texts = {'username': 'Noyob text kiriting'}
        widgets = {'phone': forms.TextInput(attrs={'placeholder':'+998 .. ... .. ..'})}

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'phone', 'first_name', 'last_name', 'email')

class ProfileChangeForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('image', )
