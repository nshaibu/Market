from django import forms

from django_countries.widgets import CountrySelectWidget

from users.models import User


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'date_of_birth',
                  'phone_number', 'street_address', 'country', 'city', 'region_or_state', )

        widgets = {
            'username': forms.TextInput(attrs={"class": "form-control"}),
            'first_name': forms.TextInput(attrs={"class": "form-control"}),
            'last_name': forms.TextInput(attrs={"class": "form-control"}),
            'email': forms.TextInput(attrs={"class": "form-control"}),
            'gender': forms.Select(attrs={"class": "form-control selectpicker"}),
            'date_of_birth': forms.DateTimeInput(attrs={"class": "form-control custom-datetimepicker"}),
            'phone_number': forms.TextInput(attrs={"class": "form-control"}),
            'street_address': forms.TextInput(attrs={"class": "form-control", "required": False}),
            'country': CountrySelectWidget(attrs={"class": "form-control selectpicker", "required": False}),
            'city': forms.TextInput(attrs={"class": "form-control", "required": False}),
            'region_or_state': forms.TextInput(attrs={"class": "form-control", "required": False}),
        }
