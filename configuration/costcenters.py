from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import CostCenters, Companies
from .forms import CostCentersForm, CostCentersFilterForm

#Centro de Custos 

def costcenter_list(request):
    template = 'configuration/costcenter-list.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    filter = CostCentersFilterForm(request.GET)

    disconnect()
    connect('eagle')

    list = CostCenters.objects()

    if filter.is_valid():
        search = filter.cleaned_data.get('search', None)
        company = filter.cleaned_data.get('company', None)
        type = filter.cleaned_data.get('type', None)
        is_active = filter.cleaned_data.get('is_active', None)

        if search: 
            list = list.filter(Q(name__icontains=search))
        if company and company != 'all': 
            list = list.filter(Q(company=company))
        if type and type != 'all': 
            list = list.filter(Q(type=type))
        if is_active == 'yes': 
            list = list.filter(is_active=True)
        elif is_active == 'no':
            list = list.filter(is_active=False)

    list_with_ref_data = []

    for cdc in list.order_by('+name'): 
        list_with_ref_data.append({'id':cdc.id, 'name':cdc.name, 'manager':'ninguem ainda', 
            'code':'{}-{}'.format(cdc.company.code, cdc.code), 
            'is_active':cdc.is_active, 'type':cdc.type})

    disconnect()

    context = { 'user_data': user_data, 'list': list_with_ref_data, 'form': filter }
    return render(request, template, context)
    

def costcenter_detail(request, id=None):
    template = 'configuration/costcenter-detail.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    title = 'Novo Centro de Custo'

    if request.method == 'POST': 
        form = CostCentersForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            company = form.cleaned_data.get('company')
            costcenter_type = form.cleaned_data.get('costcenter_type')
            code = form.cleaned_data.get('code')
            warehouses = form.cleaned_data.get('warehouses')
            
            disconnect()
            connect('eagle')

            if not form.cleaned_data.get('id'):
                cdc = CostCenters(
                    name = name,
                    company = company, 
                    type = costcenter_type,
                    code = code,
                    warehouses = warehouses
                    )
                messages.success(request, 'O centro de custo <b>%s</b> foi cadastrado com sucesso!' % cdc.name)
                cdc.save()
                disconnect()
                return redirect('costcenter-list')
            else:
                title = 'Editar Centro de Custo'
                cdc = CostCenters.objects(id=form.cleaned_data.get('id')).first()
                cdc.name = name
                cdc.code = code
                company = Companies.objects(id=company).first()
                cdc.company = company
                cdc.warehouses = warehouses
                cdc.type = costcenter_type
                messages.success(request, 'Dados atualizados!')
                cdc.save()
                disconnect()
                return redirect('costcenter-detail', id=cdc.id)

    elif not id: 
        form = CostCentersForm()
    elif id: 
        disconnect()
        connect('eagle')
        cdc = CostCenters.objects(id=id).first()
        cdc_instance = {'id': cdc.id, 'name': cdc.name, 'company': str(cdc.company.id), 'code': cdc.code, 'costcenter_type': cdc.type,'warehouses': cdc.warehouses}
        form = CostCentersForm(initial=cdc_instance)
        disconnect()
        title = 'Editar Centro de Custo'

    
    context = { 'user_data': user_data, 'form': form, 'title': title }
    return render(request, template, context)


def costcenter_deactivate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    cdc = CostCenters.objects(id=id).first()
    cdc.is_active = False
    cdc.save()
    disconnect()

    messages.warning(request, 'O centro de custo <b>%s</b> foi desativado.' % cdc.name)

    return redirect('costcenter-list')

def costcenter_activate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    cdc = CostCenters.objects(id=id).first()
    cdc.is_active = True
    cdc.save()
    disconnect()

    messages.success(request, 'O centro de custo <b>%s</b> foi ativado.' % cdc.name)

    return redirect('costcenter-list')


def costcenter_delete(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    cdc = CostCenters.objects(id=id).first()
    cdc.delete()
    disconnect()

    messages.error(request, 'O centro de custo <b>%s</b> foi excluído.' % cdc.name)

    return redirect('costcenter-list')


def costcenter_search(request, company):    
    disconnect()
    connect('eagle')
    list = CostCenters.objects(company=company)
    options = []
    for i in list: 
        options.append({'id':str(i.id), 'name':i.name, 'code':i.code})
    disconnect()
    return JsonResponse(options, safe=False)