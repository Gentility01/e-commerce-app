from django import forms
from django.forms.widgets import CheckboxInput, Widget
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget


PAYMENT_CHOICES = (
    
    ('S','Stripe'),
    ('P','PayPAl')
)

class CheckoutForm(forms.Form):
    street_address       = forms.CharField(
                                widget=forms.TextInput(attrs={
                                    'placeholder':'1234 Main St',
                                    'class':'form-control',
                                    'id':'address'
                                    }))
    apartment_address    = forms.CharField(required=False,  widget=forms.TextInput(attrs={
                                    'placeholder':'Apartment or suite',
                                    'class':'form-control',
                                    'id':'address-2'
                                    
                                     }))
    country              = CountryField(blank_label='(Select country)').formfield(Widget=CountrySelectWidget(
                                    attrs={
                                        'class':'custom-select d-block w-100'
                                    }
    ))
    zip                  = forms.CharField( widget=forms.TextInput(attrs={
        'class':'form-control'
    }) )
    same_shipping_address = forms.BooleanField(required=False, widget=forms.CheckboxInput())
    save_info            = forms.BooleanField( required=False, widget=forms.CheckboxInput())
    payment_option       = forms.ChoiceField(
                            widget=forms.RadioSelect, choices=PAYMENT_CHOICES)
    