from django import forms
from .models import Item, Category, Location, Resolution

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['title', 'description', 'category', 'location', 'date', 'image']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-input'}),
            'title': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'What did you lose/find?'}),
            'description': forms.Textarea(attrs={'class': 'form-input', 'rows': 4, 'placeholder': 'Describe the item...'}),
            'category': forms.Select(attrs={'class': 'form-input'}),
            'location': forms.Select(attrs={'class': 'form-input'}),
        }

class ResolutionForm(forms.ModelForm):
    class Meta:
        model = Resolution
        fields = ['receiver_username', 'receiver_contact', 'notes']
        widgets = {
            'receiver_username': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Username of person who received the item'}),
            'receiver_contact': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Phone or email of receiver'}),
            'notes': forms.Textarea(attrs={'class': 'form-input', 'rows': 2, 'placeholder': 'Any additional notes (optional)'}),
        }

