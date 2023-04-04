from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'email@email.com'
    }))

    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'address', 'postal_code', 'city']
        widgets = {field: forms.TextInput(attrs={'class': 'form-control', 'id': field, 'placeholder': field})
                   for field in fields
                   }
