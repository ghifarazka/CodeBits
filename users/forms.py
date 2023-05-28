from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'
        self.fields['username'].label = False
        self.fields['email'].label = False
        self.fields['password1'].label = False
        self.fields['password2'].label = False
    
    username = forms.CharField(max_length=150, help_text='')
    email = forms.EmailField()
    password1 = forms.CharField(widget=forms.PasswordInput, help_text='')
    password2 = forms.CharField(widget=forms.PasswordInput, help_text='')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']