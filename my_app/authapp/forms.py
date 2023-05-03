from django import forms
from django.forms import ModelForm
from authapp.models import Register


class RegisterForm(ModelForm):
    class Meta:
        model = Register
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()}


class LoginForm(forms.Form):
    username = forms.CharField(label="")
    password = forms.CharField(label='', widget=forms.PasswordInput)

# class EditProfileForm(forms.ModelForm):
#     password1 = forms.CharField(widget=forms.PasswordInput(), label='')
#     password2 = forms.CharField(widget=forms.PasswordInput(), label='')
#
#     class Meta:
#         model = Register
#         fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
#         labels = {
#             'username': '',
#             'email': '',
#             'first_name': 'First Name',
#             'last_name': '',
#         }
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['username'].initial = ''
#         self.fields['email'].initial = ''
#         self.fields['first_name'].initial = ''
#         self.fields['last_name'].initial = ''
