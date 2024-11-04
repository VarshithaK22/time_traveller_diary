from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import DiaryEntry

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class DiaryEntryForm(forms.ModelForm):
    class Meta:
        model = DiaryEntry
        fields = ['title', 'content', 'date_of_journey', 'location', "mood", "time_period", "destination_date", "image"]
        widgets = {
            'date_of_journey': forms.DateInput(attrs={
                'type': 'date',  
                'class': 'form-control',  
                'placeholder': 'YYYY-MM-DD',  
            }),
            "destination_date": forms.DateInput(attrs={
                'type': 'date',  
                'class': 'form-control',  
                'placeholder': 'YYYY-MM-DD',  
            }),
        }

class DiaryEntrySearchForm(forms.Form):
    query = forms.CharField(label='Key word', max_length=100, required=False)
    time_period = forms.ChoiceField(
        label='Time Period',
        choices=[('', 'All')] + DiaryEntry.TIME_PERIOD_CHOICES,  # Include an option for all time periods
        required=False
    )