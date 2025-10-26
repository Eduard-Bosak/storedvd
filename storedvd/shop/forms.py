"""
Формы для приложения магазина
"""
from django import forms

class SearchForm(forms.Form):
    """Форма поиска товаров"""
    q = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Поиск'}))
