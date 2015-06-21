from django import forms

class ProfileUser(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'login'}))
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'enter the password'}))
    retype_pass = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':' enter the password again'}))
