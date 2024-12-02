from django import forms
from .models import Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['date', 'seat_number']

    # Remove custom input_formats and use default date input
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))


class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'password1': 'Password',
            'password2': 'Password confirmation',
        }
        help_texts = {
            'username': 'Required. 150 characters or fewer. Letters, digits, and @/./+/-/_ only.',
        }
        error_messages = {
            'username': {
                'unique': 'A user with that username already exists.',
            },
            'password1': {
                'password_too_similar': 'Your password is too similar to your personal information.',
                'password_too_short': 'Your password must contain at least 8 characters.',
                'password_too_common': 'Your password is too common.',
                'password_entirely_numeric': 'Your password can’t be entirely numeric.',
            },
        }

    email = forms.EmailField(required=True, help_text="Enter a valid email address.")