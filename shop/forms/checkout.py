from django import forms

from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


# PAYMENT_CHOICES = (
#     ('MTN_MOBILE_MONEY', 'mtn mobile money'),
#     ('PAYPAL', 'paypal'),
# )


class CheckOutForm(forms.Form):
    shipping_address = forms.CharField(required=False,
                                       widget=forms.TextInput(attrs={
                                           'id': "c_shipping_address",
                                           "class": "form-control", "placeholder": "Street address"})
                                       )
    shipping_address2 = forms.CharField(required=False,
                                        widget=forms.TextInput(attrs={
                                            'id': 'o_shipping_address',
                                            "class": "form-control",
                                            "placeholder": "Apartment, suite, unit etc. (optional)"})
                                        )
    shipping_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'id': "shipping_country",
            'class': 'form-control selectpicker',
        }))
    shipping_zip = forms.CharField(required=False)
    shipping_region = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    shipping_user_email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    shipping_user_phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={"class": "form-control"}))

    billing_address = forms.CharField(required=False,
                                      widget=forms.TextInput(attrs={
                                          'id': "c_billing_address",
                                          "class": "form-control",
                                          "placeholder": "Street address"})
                                      )
    billing_address2 = forms.CharField(required=False,
                                       widget=forms.TextInput(attrs={
                                           'id': 'o_billing_address',
                                           "class": "form-control",
                                           "placeholder": "Apartment, suite, unit etc. (optional)"})
                                       )
    billing_country = CountryField(blank_label='(select country)').formfield(
        required=False,
        widget=CountrySelectWidget(attrs={
            'id': "billing_country",
            'class': 'form-control selectpicker',
        }))
    billing_zip = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    billing_region = forms.CharField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))
    billing_user_email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control"}))
    billing_user_phone_number = forms.CharField(max_length=15, widget=forms.TextInput(attrs={"class": "form-control"}))

    use_different_shipping_address = forms.BooleanField(required=False)

    set_default_shipping = forms.BooleanField(required=False)
    use_default_shipping = forms.BooleanField(required=False)

    set_default_billing = forms.BooleanField(required=False)
    use_default_billing = forms.BooleanField(required=False)
    
    order_notes = forms.CharField(widget=forms.Textarea(attrs={"class": "form-control",
                                                               "cols": "30", "rows": "4",
                                                               "placeholder": "Write your notes here..."}),
                                  required=False)

    # payment_option = forms.ChoiceField(widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
