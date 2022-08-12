from django import forms
from .models import DeliveryInfo
from locations.models import County, City
from store.models import Customer
# from allauth.account.forms import SignupForm


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = DeliveryInfo
        fields = ['mobile_number', 'address', 'county', 'city', 'postcode', ]