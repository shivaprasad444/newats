from django import forms

class LoginForm(forms.Form):
    email    = forms.EmailField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    role     = forms.CharField(widget=forms.HiddenInput)   # candidates | companies
