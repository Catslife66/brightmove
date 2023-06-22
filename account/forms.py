from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


class UserRegistrationForm(UserCreationForm):
    #is_agent = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'is_agent')


    def clean(self):
        
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        if User.objects.filter(username__iexact=username).exists():
            self.add_error('username', 'This username is already taken.')

        if User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'This email is already registered.')

        return cleaned_data
    

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'is_agent')


class UserAuthenticationForm(AuthenticationForm):
    remember_me = forms.CharField(label='Remember me', widget=forms.CheckboxInput, required=False)


