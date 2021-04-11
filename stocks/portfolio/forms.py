from django import forms
from .models import Portfolio

class SaveEfficientFrontierForm(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name', 'description', )