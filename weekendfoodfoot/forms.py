# forms.py

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nom d’utilisateur',
            'email': 'Adresse email',
            'password1': 'Mot de passe',
            'password2': 'Confirmation du mot de passe',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # Notez le changement ici, utilisez super() au lieu de super(MyUserCreationForm, self)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})