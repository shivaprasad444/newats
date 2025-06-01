from django import forms
from django.db import models
from .models import Timesheets
from datetime import datetime

class LoginForm(forms.Form):
    email    = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    #role     = forms.CharField(widget=forms.HiddenInput)   # candidates | companies

class CandidateSignupForm(forms.Form):
    firstname = forms.CharField(label="First name", max_length=100)
    lastname = forms.CharField(label="Last name", max_length=100)
    email = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirmpassword = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    resume = forms.FileField(label="Upload Resume")

class TimesheetForm(forms.ModelForm):
    class Meta:
        model = Timesheets
        fields = ['date', 'earn_code', 'start_time', 'end_time']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')

        if start_time and end_time:
            start = datetime.combine(datetime.today(), start_time)
            end = datetime.combine(datetime.today(), end_time)
            duration = (end - start).total_seconds() / 3600

            if duration < 0:
                raise forms.ValidationError("End time must be after start time.")

            cleaned_data['hours'] = round(duration, 2)

        return cleaned_data


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, label='Your Name')
    email = forms.EmailField(label='Your Email')
    message = forms.CharField(widget=forms.Textarea, label='Problem Description')



