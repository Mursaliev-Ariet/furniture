from django import forms
from .models import Order, ContactMessage

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['organization', 'contact_name', 'phone', 'email', 'city', 'street', 'house', 'comment']

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'phone', 'email', 'comment']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'phone': forms.TextInput(attrs={'placeholder': '+7 999 999-99-99'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Электронная почта'}),
            'comment': forms.Textarea(attrs={'placeholder': 'Комментарий', 'rows': 4}),
        }