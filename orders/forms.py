# forms.py
from django import forms
from .models import BannerOrder

class BannerOrderForm(forms.ModelForm):
    class Meta:
        model = BannerOrder
        fields = ['width', 'height', 'text', 'phone', 'bg_color', 'text_color', 'grommet_type', 'image']
        widgets = {
            'bg_color': forms.TextInput(attrs={'type': 'color'}),
            'text_color': forms.TextInput(attrs={'type': 'color'}),
        }