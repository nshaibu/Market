import re

from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label_suffix='', required=True, label="Username/Email",
                               help_text="Please enter your username or email address.",
                               widget=forms.TextInput(attrs={
                                   "id": "FormUsername",
                                   "name": "username",
                                   "class": "form-control"
                               }))
    password = forms.CharField(max_length=100, min_length=8, label_suffix='', required=True,
                               widget=forms.PasswordInput(attrs={
                                   "id": "FormPassword",
                                   "name": "password",
                                   "class": "form-control",
                                   "aria-describedby": "FormPasswordHelpBlock"}))

    def check_email(self):
        value = self.cleaned_data["username"]
        return re.match('^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$', value)
