
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import Companies
from .forms import CompaniesForm, CompaniesFilterForm

def company_list(request):
    template = 'configuration/company-list.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    filter = CompaniesFilterForm(request.GET)

    disconnect()
    connect('eagle')

    list = Companies.objects().all()
    
    disconnect()

    if filter.is_valid():
        search = filter.cleaned_data.get('search', None)
        is_active = filter.cleaned_data.get('is_active', None)
        company_type = filter.cleaned_data.get('company_type', None)
        company_tax_type = filter.cleaned_data.get('company_tax_type', None)

        if search:
            search_cnpj = '' 
            for i, x in enumerate(search): 
                print(i)
                if i < 2: 
                    search_cnpj += x
                elif i == 2: 
                    search_cnpj += '.' + x
                elif i < 5: 
                    search_cnpj += x
                elif i == 5:
                    search_cnpj += '.' + x
                elif i < 8: 
                    search_cnpj += x
                elif i == 8: 
                    search_cnpj += '/' + x
                elif i < 12:
                    search_cnpj += x
                elif i == 12:
                    search_cnpj += '-' + x
                else: 
                    search_cnpj += x

            print(search_cnpj)

            list = list.filter(Q(code__icontains=search) | Q(company_name__icontains=search) | Q(cnpj__icontains=search)| Q(cnpj__icontains=search_cnpj) | Q(ie__icontains=search) | Q(bussiness_name__icontains=search))
        if is_active == 'yes': 
            list = list.filter(is_active=True)
        elif is_active == 'no':
            list = list.filter(is_active=False)
        if company_type != 'all' and company_type:
            list = list.filter(company_type=company_type)
        if company_tax_type != 'all' and company_tax_type:
            list = list.filter(company_tax_type=company_tax_type)

    context = { 'user_data': user_data, 'list': list, 'form': filter }
    return render(request, template, context)
    

def company_detail(request, id=None):
    template = 'configuration/company-detail.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    title = 'Nova Empresa'

    if request.method == 'POST': 
        form = CompaniesForm(request.POST)

        if form.is_valid():
            company_type = form.cleaned_data.get('company_type')
            company_headoffice = form.cleaned_data.get('company_headoffice')
            cnpj = form.cleaned_data.get('cnpj')
            ie = form.cleaned_data.get('ie')
            has_exemptiom_ie = form.cleaned_data.get('has_exemptiom_ie')
            bussiness_name = form.cleaned_data.get('bussiness_name')
            company_name = form.cleaned_data.get('company_name')
            company_tax_type = form.cleaned_data.get('company_tax_type')
            post_code = form.cleaned_data.get('post_code')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            district = form.cleaned_data.get('district')
            address = form.cleaned_data.get('address')
            number = form.cleaned_data.get('number')
            complement = form.cleaned_data.get('complement')
            code = form.cleaned_data.get('code')
            
            disconnect()
            connect('eagle')

            if not form.cleaned_data.get('id'):
                company = Companies(
                    company_type = company_type,
                    company_headoffice = company_headoffice if company_headoffice != '' else None,
                    cnpj = cnpj,
                    ie = ie,
                    has_exemptiom_ie = has_exemptiom_ie,
                    bussiness_name = bussiness_name,
                    company_name = company_name,
                    company_tax_type = company_tax_type,
                    post_code = post_code,
                    state = state,
                    city = city,
                    district = district,
                    address = address,
                    number = number,
                    complement = complement,
                    code = code
                    )
                messages.success(request, 'A empresa <b>%s</b> foi cadastrada com sucesso!' % company.company_name)
                company.save()
                disconnect()
                return redirect('company-list')
            else:
                title = 'Editar Empresa'
                company = Companies.objects(id=form.cleaned_data.get('id')).first()
                if company_headoffice != '':
                    company_headoffice = Companies.objects(id=form.cleaned_data.get('company_headoffice')).first()
                else: 
                    company_headoffice = None
                company.company_type = company_type
                company.company_headoffice = company_headoffice if company_headoffice else None
                company.cnpj = cnpj
                company.ie = ie
                company.has_exemptiom_ie = has_exemptiom_ie
                company.bussiness_name = bussiness_name
                company.company_name = company_name
                company.company_tax_type = company_tax_type
                company.post_code = post_code
                company.state = state
                company.city = city
                company.district = district
                company.address = address
                company.number = number
                company.complement = complement
                company.code = code
                company.save()
                messages.success(request, 'Dados atualizados!')
                disconnect()
                return redirect('company-detail', id=company.id)

    elif not id: 
        form = CompaniesForm()
    elif id: 
        disconnect()
        connect('eagle')
        company = Companies.objects(id=id).first()
        company_instance = {
            'id': id,
            'company_type': company.company_type,
            'company_headoffice': company.company_headoffice,
            'cnpj': company.cnpj,
            'ie': company.ie,
            'has_exemptiom_ie': company.has_exemptiom_ie,
            'bussiness_name': company.bussiness_name,
            'company_name': company.company_name,
            'company_tax_type': company.company_tax_type,
            'post_code': company.post_code,
            'state': company.state,
            'city': company.city,
            'district': company.district,
            'address': company.address,
            'number': company.number,
            'complement': company.complement, 
            'code': company.code
            }
        disconnect()
        form = CompaniesForm(initial=company_instance)
        title = 'Editar Empresa'
    
    context = { 'user_data': user_data, 'form': form, 'title': title }
    return render(request, template, context)


def company_deactivate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    company = Companies.objects(id=id).first()
    company.is_active = False
    company.save()
    disconnect()

    messages.warning(request, 'A empresa <b>%s</b> foi desativada.' % company.company_name)

    return redirect('company-list')

def company_activate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    company = Companies.objects(id=id).first()
    company.is_active = True
    company.save()
    disconnect()

    messages.success(request, 'A empresa <b>%s</b> foi ativada.' % company.company_name)

    return redirect('company-list')


def company_delete(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    company = Companies.objects(id=id).first()
    company.delete()
    disconnect()

    messages.error(request, 'A empresa <b>%s</b> foi excluída.' % company.company_name)

    return redirect('company-list')


def company_search(request, id):    
    disconnect()
    connect('eagle')
    list = Companies.objects(id=id)
    options = []
    for i in list: 
        options.append({'id':str(i.id), 'code':i.code})
    disconnect()
    return JsonResponse(options, safe=False)