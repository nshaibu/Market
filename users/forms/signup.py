from django import forms

from ..models import User


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=80, label="Username", label_suffix='', widget=forms.TextInput(attrs={
        "id": "SigUpFormUsername",
        "name": "username",
        "class": "form-control"}))
    first_name = forms.CharField(max_length=80, label_suffix='', widget=forms.TextInput(attrs={
        "id": "SignUpFormFirstName",
        "name": "first_name",
        "class": "form-control"
    }))
    last_name = forms.CharField(max_length=80, label_suffix='', widget=forms.TextInput(attrs={
        "id": "SignUpFormLastName",
        "name": "last_name",
        "class": "form-control"
    }))
    email = forms.EmailField(label_suffix='', widget=forms.EmailInput(attrs={
        "id": "FormEmail",
        "name": "email",
        "class": "form-control"
    }))
    password = forms.CharField(max_length=100, label_suffix='', min_length=8, required=True,
                               help_text='At least 8 characters and 1 digit',
                               widget=forms.PasswordInput(attrs={
                                   "id": "FormPassword",
                                   "class": "form-control",
                                   "aria-describedby": "FormPasswordHelpBlock"}))
    confirm_password = forms.CharField(max_length=100, label_suffix='', min_length=8, required=True,
                                       widget=forms.PasswordInput(attrs={
                                           "id": "FormPassword",
                                           "class": "form-control",
                                           "aria-describedby": "FormPasswordHelpBlock"}))
    phone_number = forms.CharField(max_length=15, label_suffix='', widget=forms.TextInput(attrs={
        "id": "FormPhone",
        "type": "tel",
        "class": "form-control",
        "aria-describedby": "FormPhoneHelpBlock"}))
    gender = forms.ChoiceField(choices=User.GENDER, label_suffix='', required=True, widget=forms.Select(attrs={
        "class": "form-control selectpicker",
        "id": "GenderSelect",
        "name": "gender",
    }))
    # user_type = forms.ChoiceField(choices=User.USER_TYPE, required=True, widget=forms.Select(attrs={
    #     "class": "form-control selectpicker",
    #     "id": "UserTypeSelect",
    #     "name": "user_type",
    # }))

    user_type = forms.CharField(widget=forms.HiddenInput(attrs={"value": User.USER_TYPE_CUSTOMER}))

    error_css_class = "text-danger"

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Account with such name already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Account with such email already exists.")
        return email

    def clean_confirm_password(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]

        if password != confirm_password:
            raise forms.ValidationError("Password not matched", code="password_match")
        return password
