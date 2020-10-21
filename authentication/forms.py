from django import forms
from django.core.exceptions import ValidationError
from mongoengine import connect, disconnect
from django.contrib.auth.hashers import make_password, check_password
from users.models import Users

class LoginForm(forms.Form):
    username = forms.CharField(label='Nome de Usuário', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    password = forms.CharField(label='Senha', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})

    def clean(self):
        _username = self.cleaned_data.get('username')
        _password = self.cleaned_data.get('password')
        print(_password)

        disconnect()
        connect('eagle')

        user = Users.objects(username=_username).first()
        
        disconnect()

        if not user and _username: 
            self.add_error('username', 'Desculpe, este nome de usuário não foi encontrado')
        elif user and _password and not check_password(_password, user.password):
            self.add_error('password', 'Por favor, verifique sua senha')

