from django.shortcuts import render, redirect
from django.http import HttpResponse
#forms
from .forms import LoginForm
from users.models import Users
from mongoengine import connect, disconnect
from django.contrib import messages

def index(request):
    template = 'login/login.html'
    form = LoginForm()  
    
    if request.method == 'POST': 
        form = LoginForm(request.POST)

        if form.is_valid():
            _username = form.cleaned_data.get('username')
            disconnect()
            connect('eagle')
            user = Users.objects(username=_username).first()
            disconnect()

            if user.is_active: 
                request.session['username'] = user.username
                request.session['permissions'] = user.permissions
                request.session['admin'] = user.is_admin
                return redirect('home')
            else: 
                messages.warning(request, 'Por favor, entre em contato com o gestor de sua área.')

    context = { 'login': True, 'form': form }
    return render(request, template, context)

def get_logged(request):
    if 'username' in request.session: 
        username = request.session.get('username')
        permissions = request.session.get('permissions')
        is_admin = request.session.get('admin')
        return {'username': username, 'permissions': permissions, 'is_admin': is_admin}
    else:
        return False
