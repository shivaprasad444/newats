from django import forms
from django.db import models

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



