from django import forms
from .models import Stock, Position

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ["ticker"]

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ["stock_symbol", "stock_shares", "stock_price"]


class EditHoldingForm(forms.ModelForm):
    
    class Meta:
        model = Position
        
        fields = ["stock_shares", "stock_price"]