from django import forms
from .models import AIResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'form-control'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Konfirmasi Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
class AIForm(forms.ModelForm):
    class Meta:
        model = AIResponse
        fields = ['prompt']
        widgets = {
            'prompt': forms.Textarea(attrs={
                'placeholder': 'What your Bootstrap template will be about? Write in any language.',
                'class': 'aiTextarea',
                'id': 'aiPromt',
                'rows': 6,
            }),
        }

