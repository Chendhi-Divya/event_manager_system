from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'})
        }

class OTPForm(forms.Form):
    otp = forms.CharField(label='Enter OTP', widget=forms.TextInput(attrs={'class': 'form-control'}))
