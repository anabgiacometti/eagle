from django import forms
from django.core.exceptions import ValidationError
from mongoengine import connect, disconnect
from users.models import Users

class UserForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    username = forms.CharField(label='Nome de Usuário', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    full_name = forms.CharField(label='Nome Completo', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    email = forms.EmailField(label='E-mail', max_length=100, error_messages={'required': 'Por favor, preencha este campo', 'invalid': 'Por favor, preencha um e-mail válido'})
    is_admin = forms.BooleanField(required=False)
    permissions = forms.MultipleChoiceField(label='Permissões', required=False, widget=forms.CheckboxSelectMultiple(), 
        choices=(
            ('users', 'Usuários'), 
            ('companies', 'Empresas'),
            ('costcenters', 'Centros de Custo'),
            ('departments', 'Departamentos'),
            ('functions', 'Cargos'),
            ('employees', 'Funcionários'),
            ('warehouses', 'Depósitos'),
        )
    )

    def clean(self):
        _username = self.cleaned_data.get('username')
        _email = self.cleaned_data.get('email')
        _id = self.cleaned_data.get('id')

        disconnect()
        connect('eagle')

        if not _id:
            user_username = Users.objects(username=_username).first()
            user_email = Users.objects(email=_email).first()
        else: 
            user_username = Users.objects.filter(username=_username).filter(id__ne=_id).first()
            user_email = Users.objects.filter(email=_email).filter(id__ne=_id).first()

        disconnect()

        if user_username: 
            self.add_error('username', 'Desculpe, este nome de usuário já está cadastrado')
        if user_email: 
            self.add_error('email', 'Desculpe, este e-mail já está cadastrado')

class FilterForm(forms.Form):
    search = forms.CharField(label='Pesquise', required=False)
    is_active = forms.CharField(required=False)
    is_admin = forms.CharField(required=False)
