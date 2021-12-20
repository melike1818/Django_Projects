from django import forms

class registerForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    username = forms.CharField(label='username', max_length=100)
