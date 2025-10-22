from django import forms
from shipping.models import ShippingAddres
from lib.validators import min_length_validator
from django.core.exceptions import ValidationError  



class ShippingAddressForm(forms.ModelForm):
    # zip_code = forms.CharField(validators=[min_length_validator])

    class Meta:
        model = ShippingAddres
        fields = ('city', 'zip_code', 'addres', 'number')
        # exclude = ('user',)
        # fields = '__all__'

    def clean_zip_code(self):
        zip_code = self.cleaned_data['zip_code']
        if len(zip_code) != 16:
            raise ValidationError("length is not 16")
        
        return zip_code
    

    def clean(self):
        cleaned_data = super().clean()


        return cleaned_data