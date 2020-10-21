from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.hashers import make_password, check_password
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import Users
from .forms import UserForm, FilterForm

def list(request):
	template = 'users/list.html'
	user_data = get_logged(request)

	if not user_data: 
		return redirect('login')

	filter = FilterForm(request.GET)

	disconnect()
	connect('eagle')

	list = Users.objects()
	
	disconnect()

	if filter.is_valid():
		search = filter.cleaned_data.get('search', None)
		is_admin = filter.cleaned_data.get('is_admin', None)
		is_active = filter.cleaned_data.get('is_active', None)

		if search: 
			list = list.filter(Q(username__icontains=search) | Q(full_name__icontains=search) | Q(email__icontains=search))
		if is_admin == 'yes': 
			list = list.filter(is_admin=True)
		elif is_admin == 'no':
			list = list.filter(is_admin=False)
		if is_active == 'yes': 
			list = list.filter(is_active=True)
		elif is_active == 'no':
			list = list.filter(is_active=False)
	
	context = { 'user_data': user_data, 'list': list, 'form': filter }
	return render(request, template, context)



def detail(request, id=None):
	template = 'users/details.html'
	user_data = get_logged(request)

	if not user_data: 
		return redirect('login')

	title = 'Novo Usuário'

	if request.method == 'POST': 
		form = UserForm(request.POST)

		if form.is_valid():
			_username = form.cleaned_data.get('username')
			_full_name = form.cleaned_data.get('full_name')
			_email = form.cleaned_data.get('email')
			_permissions = form.cleaned_data.get('permissions')
			_is_admin = form.cleaned_data.get('is_admin')

			disconnect()
			connect('eagle')

			if not form.cleaned_data.get('id'):
				user = Users(
					username = _username,
					full_name = _full_name,
					email = _email, 
					is_admin = _is_admin, 
					permissions = _permissions, 
					password = make_password('temporary')
					)
				messages.success(request, 'O usuário <b>%s</b> foi cadastrado com sucesso!' % user.full_name)
				user.save()
				disconnect()
				return redirect('user-list')
			else:
				title = 'Editar Usuário'
				user = Users.objects(id=form.cleaned_data.get('id')).first()
				user.username = _username
				user.full_name = _full_name
				user.email = _email
				user.permissions = _permissions
				user.is_admin = _is_admin
				messages.success(request, 'Dados atualizados!')
				user.save()
				disconnect()
				return redirect('user-detail', id=user.id)

	elif not id: 
		form = UserForm()
	elif id: 
		disconnect()
		connect('eagle')
		user = Users.objects(id=id).first()
		disconnect()
		user_instance = {'id': user.id, 'username': user.username, 'full_name': user.full_name, 'permissions': user.permissions, 'email':user.email, 'is_admin': user.is_admin}
		form = UserForm(initial=user_instance)
		title = 'Editar Usuário'

	
	context = { 'user_data': user_data, 'form': form, 'title': title }
	return render(request, template, context)


def deactivate(request, id):
	user_data = get_logged(request)

	if not user_data: 
		return redirect('login')

	disconnect()
	connect('eagle')
	user = Users.objects(id=id).first()
	user.is_active = False
	user.save()
	disconnect()

	messages.warning(request, 'O usuário <b>%s</b> foi desativado.' % user.full_name)

	return redirect('user-list')

def activate(request, id):
	user_data = get_logged(request)

	if not user_data: 
		return redirect('login')

	disconnect()
	connect('eagle')
	user = Users.objects(id=id).first()
	user.is_active = True
	user.save()
	disconnect()

	messages.success(request, 'O usuário <b>%s</b> foi ativado.' % user.full_name)

	return redirect('user-list')


def delete(request, id):
	user_data = get_logged(request)

	if not user_data: 
		return redirect('login')

	disconnect()
	connect('eagle')
	user = Users.objects(id=id).first()
	user.delete()
	disconnect()

	messages.error(request, 'O usuário <b>%s</b> foi excluído.' % user.full_name)

	return redirect('user-list')