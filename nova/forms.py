from django import forms
from django.contrib.auth.models import User
from nova.models import *
from django.core.exceptions import ValidationError

class SignupModel(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "password", "email"]
        
class SignupForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
        
class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserdataModel
        fields = ["profilestatus", "contact", "lmark",
                  "local", "city", "district", "state", "pincode"]
        
    def clean_contact(self):
        contact = self.cleaned_data.get('contact')
        if contact and (len(str(contact)) != 10 or not str(contact).isdigit()):
            raise ValidationError("Contact number must be exactly 10 digits.")
        return contact

    def clean_pincode(self):
        pincode = self.cleaned_data.get('pincode')
        if pincode and (len(str(pincode)) != 6 or not str(pincode).isdigit()):
            raise ValidationError("Invalid pincode")
        return pincode
    
class ReviewForm(forms.ModelForm):
    class Meta:
        model = ReviewModel
        fields = ["rating", "review"]