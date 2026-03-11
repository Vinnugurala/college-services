from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, StudentProfile, XeroxOrder, MenuItem, Canteen, XeroxCenter

class CustomUserCreationForm(UserCreationForm):
    role = forms.ChoiceField(choices=User.ROLE_CHOICES, required=True)
    phone_number = forms.CharField(max_length=15, required=False)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email', 'role', 'phone_number')

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['hostel_name', 'room_number']

class XeroxOrderForm(forms.ModelForm):
    class Meta:
        model = XeroxOrder
        fields = ['document', 'copies', 'color_type', 'print_type']

class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = ['name', 'description', 'price', 'is_available', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class CanteenForm(forms.ModelForm):
    class Meta:
        model = Canteen
        fields = ['name', 'description', 'image']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class XeroxCenterForm(forms.ModelForm):
    class Meta:
        model = XeroxCenter
        fields = ['name', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
