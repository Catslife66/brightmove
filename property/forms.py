from django import forms
from django.forms import modelformset_factory, inlineformset_factory
from .models import Address, PropertyFeature, PropertyPrice, Property, PropertyImage


class PropertyAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('line_1', 'line_2', 'town', 'region', 'postcode')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['line_2'].widget.attrs.update({"required": False})
        self.fields['region'].widget.attrs.update({"required": False})

    def cleaned_data(self):
        cleaned_data = super().clean()
        line_1 = cleaned_data.get('line_1')
        town = cleaned_data.get('town')
        postcode = cleaned_data.get('postcode')
        addr = Property.objects.filter(
            is_active=True, 
            property_address__line_1__iexact=line_1, 
            property_address__town__iexact=town, 
            property_address__postcode__iexact=postcode
        )
        
        if addr.exists():
            raise forms.ValidationError('This address has been registered.')
        
        return cleaned_data


class PropertyFeatureForm(forms.ModelForm):
    class Meta:
        model = PropertyFeature
        fields = ('property_type', 'bedroom', 'toilet')


class PropertyPriceForm(forms.ModelForm):
    class Meta:
        model = PropertyPrice
        fields = ('price_type', 'price')


class PropertyUploadForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ('description', )


class PropertyImageForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ('image', 'is_feature', 'alt_text') 

    
ImageFormset = modelformset_factory(
    PropertyImage,
    form=PropertyImageForm,
    extra=1,
    can_delete=True,
    max_num=20,
    validate_max=True
)

ImageInlineFormset = inlineformset_factory(
    Property,
    PropertyImage,
    form=PropertyImageForm,
    formset=ImageFormset,
    extra=1,
    can_delete=True,
    max_num=20,
    validate_max=True
)


class EmailForm(forms.Form):
    email_from = forms.EmailField(label='From')
    send_to = forms.EmailField(label='To')
    subject = forms.CharField(label='Subject')
    message = forms.CharField(label='Message', widget=forms.Textarea)