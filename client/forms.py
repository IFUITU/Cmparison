from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from .models import User

class UserForm(forms.ModelForm):
    confirm = forms.CharField(max_length=128, validators=[MinLengthValidator(6)], widget=forms.PasswordInput(), required=True)
    password = forms.CharField(max_length=128, validators=[MinLengthValidator(6)], widget=forms.PasswordInput(), required=True)

    class Meta:
        model = User
        fields = ['company_name', "username", 'phone',  'password', 'confirm']
        help_texts = {
            'username': None,
        }
        widgets = {
            'phone': forms.TextInput(
                attrs={
                    'placeholder': '+988',
                }
            )
        }
    # def clean(self):
    #     print(self.cleaned_data)


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40)
    password = forms.CharField(max_length=20, widget=forms.PasswordInput, validators=[MinLengthValidator(6)])

