from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import WareHouses, CostCenters
from .forms import WareHousesForm, WareHousesFilterForm


#Depósitos 

def warehouse_list(request):
    template = 'configuration/warehouse/list.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    filter = WareHousesFilterForm(request.GET)

    disconnect()
    connect('eagle')

    list = WareHouses.objects()    

    if filter.is_valid():
        search = filter.cleaned_data.get('search', None)
        is_active = filter.cleaned_data.get('is_active', None)

        if search: 
            list = list.filter(Q(name__icontains=search))
        if is_active == 'yes': 
            list = list.filter(is_active=True)
        elif is_active == 'no':
            list = list.filter(is_active=False)

    disconnect()

    context = { 'user_data': user_data, 'list': list, 'form': filter }
    return render(request, template, context)
    

def warehouse_detail(request, id=None):
    template = 'configuration/warehouse/detail.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    title = 'Novo Depósito'

    if request.method == 'POST': 
        form = WareHousesForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            permissions = form.cleaned_data.get('permissions')
            
            disconnect()
            connect('eagle')

            if not form.cleaned_data.get('id'):
                dep = WareHouses(
                    name = name,
                    permissions = permissions,
                    )
                messages.success(request, 'O depósito <b>%s</b> foi cadastrado com sucesso!' % dep.name)
                dep.save()
                disconnect()
                return redirect('warehouse-list')
            else:
                title = 'Editar Depósito'
                dep = WareHouses.objects(id=form.cleaned_data.get('id')).first()
                dep.name = name
                dep.permissions = permissions
                messages.success(request, 'Dados atualizados!')
                dep.save()
                disconnect()
                return redirect('warehouse-detail', id=dep.id)

    elif not id: 
        form = WareHousesForm()
    elif id: 
        disconnect()
        connect('eagle')
        dep = WareHouses.objects(id=id).first()
        dep_instance = {'id': dep.id, 'name': dep.name, 'permissions':dep.permissions}
        disconnect()
        form = WareHousesForm(initial=dep_instance)
        title = 'Editar Depósito'

    
    context = { 'user_data': user_data, 'form': form, 'title': title }
    return render(request, template, context)


def warehouse_deactivate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    depto = WareHouses.objects(id=id).first()
    depto.is_active = False
    depto.save()
    disconnect()

    messages.warning(request, 'O depósito <b>%s</b> foi desativado.' % depto.name)

    return redirect('warehouse-list')

def warehouse_activate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    depto = WareHouses.objects(id=id).first()
    depto.is_active = True
    depto.save()
    disconnect()

    messages.success(request, 'O depósito <b>%s</b> foi ativado.' % depto.name)

    return redirect('warehouse-list')


def warehouse_delete(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    depto = WareHouses.objects(id=id).first()
    depto.delete()
    disconnect()

    messages.error(request, 'O depósito <b>%s</b> foi excluído.' % depto.name)

    return redirect('warehouse-list')


def warehouse_search(request, costcenter):    
    connect(db='eagle', alias='default')
    list = WareHouses.objects(costcenters__icontains=costcenter)
    options = []
    for i in list: 
        options.append({'id':str(i.id), 'name':i.name})
    disconnect()
    return JsonResponse(options, safe=False)