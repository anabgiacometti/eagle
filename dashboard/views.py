from django.shortcuts import render
from django.http import HttpResponse
#forms
from mongoengine import connect, disconnect
from authentication.views import get_logged

def home(request):
	template = 'home/home.html'
	user_data = get_logged(request)

	if not user_data: 
		return redirect('login')

	context = { 'user_data': user_data }
	return render(request, template, context)
	