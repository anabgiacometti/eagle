from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import Departments, CostCenters
from .forms import DepartmentsForm, DepartmentsFilterForm


#Departamentos 

def department_list(request):
    template = 'configuration/department-list.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    filter = DepartmentsFilterForm(request.GET)

    disconnect()
    connect('eagle')

    list = Departments.objects()
    

    if filter.is_valid():
        search = filter.cleaned_data.get('search', None)
        # company = filter.cleaned_data.get('company', None)
        costcenters = filter.cleaned_data.get('costcenters', None)
        is_active = filter.cleaned_data.get('is_active', None)

        if search: 
            list = list.filter(Q(name__icontains=search))
        # if company and company != 'all': 
        #     list = list.filter(Departments.costcenters.company==company)
        if costcenters and costcenters != 'all': 
            list = list.filter(Q(costcenters=costcenters))
        if is_active == 'yes': 
            list = list.filter(is_active=True)
        elif is_active == 'no':
            list = list.filter(is_active=False)

    disconnect()

    context = { 'user_data': user_data, 'list': list, 'form': filter }
    return render(request, template, context)
    

def department_detail(request, id=None):
    template = 'configuration/department-detail.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    title = 'Novo Departamento'

    if request.method == 'POST': 
        form = DepartmentsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            costcenters = form.cleaned_data.get('costcenters')
            description = form.cleaned_data.get('description')
            
            disconnect()
            connect('eagle')

            if not form.cleaned_data.get('id'):
                depto = Departments(
                    name = name,
                    costcenters = costcenters,
                    description = description
                    )
                messages.success(request, 'O departamento <b>%s</b> foi cadastrado com sucesso!' % depto.name)
                depto.save()
                disconnect()
                return redirect('department-list')
            else:
                title = 'Editar Departamento'
                depto = Departments.objects(id=form.cleaned_data.get('id')).first()
                depto.name = name
                depto.costcenters = costcenters
                depto.description = description
                messages.success(request, 'Dados atualizados!')
                depto.save()
                disconnect()
                return redirect('department-detail', id=depto.id)

    elif not id: 
        form = DepartmentsForm()
    elif id: 
        disconnect()
        connect('eagle')
        depto = Departments.objects(id=id).first()
        depto_instance = {'id': depto.id, 'name': depto.name, 'costcenters':depto.costcenters, 'description': depto.description}
        disconnect()
        form = DepartmentsForm(initial=depto_instance)
        title = 'Editar Departamento'

    
    context = { 'user_data': user_data, 'form': form, 'title': title }
    return render(request, template, context)


def department_deactivate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    depto = Departments.objects(id=id).first()
    depto.is_active = False
    depto.save()
    disconnect()

    messages.warning(request, 'O departamento <b>%s</b> foi desativado.' % depto.name)

    return redirect('department-list')

def department_activate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    depto = Departments.objects(id=id).first()
    depto.is_active = True
    depto.save()
    disconnect()

    messages.success(request, 'O departamento <b>%s</b> foi ativado.' % depto.name)

    return redirect('department-list')


def department_delete(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    depto = Departments.objects(id=id).first()
    depto.delete()
    disconnect()

    messages.error(request, 'O departamento <b>%s</b> foi excluído.' % depto.name)

    return redirect('department-list')


def department_search(request, costcenter):    
    connect(db='eagle', alias='default')
    list = Departments.objects(costcenters__icontains=costcenter)
    options = []
    for i in list: 
        options.append({'id':str(i.id), 'name':i.name})
    disconnect()
    return JsonResponse(options, safe=False)