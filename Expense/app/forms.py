from .models import Expense
from django import forms

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['name','cost','category']