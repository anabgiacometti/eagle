from django.shortcuts import render, redirect
from django.http import HttpResponse
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import Employees
from .forms import EmployeesForm, FilterForm
from configuration.models import Companies, CostCenters, Departments, Functions


#TODO
'''
FILTROS DE FUNCIONÁRIOS - FILTROS COMUNS E FILTROS ESPECIFICOS
ADICIONAR BOTÃO PARA MOSTRAR/OCULTAR OS FILTROS ESPECIFICOS
CASO FILTRO ESPECIFICO ATIVO, MANTER EXIBIDO
'''

def list(request):
    template = 'employees/list.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    filter = FilterForm(request.GET)

    disconnect()
    connect('eagle')

    list = Employees.objects()
    list_with_ref_data = []

    if filter.is_valid():
        search = filter.cleaned_data.get('search', None)
        # is_admin = filter.cleaned_data.get('is_admin', None)
        # is_active = filter.cleaned_data.get('is_active', None)

        if search: 
            list = list.filter(Q(full_name__icontains=search))
        # if is_admin == 'yes': 
        #     list = list.filter(is_admin=True)
        # elif is_admin == 'no':
        #     list = list.filter(is_admin=False)
        # if is_active == 'yes': 
        #     list = list.filter(is_active=True)
        # elif is_active == 'no':
        #     list = list.filter(is_active=False)

    for emp in list: 
        list_with_ref_data.append({'id':emp.id, 'full_name':emp.full_name, 'cpf':emp.cpf, 'costcenter':'{}-{}'.format(emp.costcenter.company.code, emp.costcenter.code), 
            'department': emp.department.name, 'function': '{} {}'
            .format(emp.function.name, 'Junior' if emp.function.level == 'junior' else 'Pleno' if emp.function.level == 'pleno' else 'Senior' if emp.function.level == 'senior' 
        else 'Especialista' if emp.function.level == 'expert' else ''), 'situation': 'Aguardando Admissão' if emp.situation == 'waiting_admission' else 'Contrato Ativo' if emp.situation == 'employeed' 
            else 'Em Férias' if emp.situation == 'vacation' else 'Desligado' if emp.situation == 'dismissed' else '' })

    disconnect()

    context = { 'user_data': user_data, 'list': list_with_ref_data, 'form': filter }
    return render(request, template, context)


def detail(request, id=None):
    template = 'employees/detail.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    title = 'Novo Funcionário'

    if request.method == 'POST': 
        form = EmployeesForm(request.POST)

        if form.is_valid():
            full_name = form.cleaned_data.get('full_name')
            cpf = form.cleaned_data.get('cpf')
            rg = form.cleaned_data.get('rg')
            pis = form.cleaned_data.get('pis')
            ctps = form.cleaned_data.get('ctps')
            birthdate = form.cleaned_data.get('birthdate')
            phone_number = form.cleaned_data.get('phone_number')
            cellphone_number = form.cleaned_data.get('cellphone_number')
            email = form.cleaned_data.get('email')
            post_code = form.cleaned_data.get('post_code')
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            district = form.cleaned_data.get('district')
            address = form.cleaned_data.get('address')
            number = form.cleaned_data.get('number')
            complement = form.cleaned_data.get('complement')
            bank = form.cleaned_data.get('bank')
            agency = form.cleaned_data.get('agency')
            account = form.cleaned_data.get('account')
            account_type = form.cleaned_data.get('account_type')
            contract = form.cleaned_data.get('contract')
            situation = form.cleaned_data.get('situation')
            payment_type = form.cleaned_data.get('payment_type')
            company = form.cleaned_data.get('company')
            costcenter = form.cleaned_data.get('costcenter')
            department = form.cleaned_data.get('department')
            function = form.cleaned_data.get('function')
            admission_date = form.cleaned_data.get('admission_date')
            experience_end_date = form.cleaned_data.get('experience_end_date')
            resignation_date = form.cleaned_data.get('resignation_date')
            resignation_reason = form.cleaned_data.get('resignation_reason')
            last_salary = form.cleaned_data.get('last_salary')
            
            disconnect()
            connect('eagle')

            if not form.cleaned_data.get('id'):
                emp = Employees(
                    full_name = full_name,
                    cpf = cpf,
                    rg = rg,
                    pis = pis,
                    ctps = ctps,
                    birthdate = birthdate,
                    phone_number = phone_number,
                    cellphone_number = cellphone_number,
                    email = email,
                    post_code = post_code,
                    state = state,
                    city = city,
                    district = district,
                    address = address,
                    number = number,
                    complement = complement,
                    bank = bank,
                    agency = agency,
                    account = account,
                    account_type = account_type,
                    contract = contract,
                    situation = situation,
                    payment_type = payment_type,
                    company = company,
                    costcenter = costcenter,
                    department = department,
                    function = function,
                    admission_date = admission_date,
                    experience_end_date = experience_end_date,
                    resignation_date = resignation_date,
                    resignation_reason = resignation_reason,
                    last_salary = last_salary,
                    )
                messages.success(request, 'O funcionário <b>%s</b> foi cadastrado com sucesso!' % emp.full_name)
                emp.save()
                disconnect()
                return redirect('employee-list')
            else:
                title = 'Editar Funcionário'
                emp = Employees.objects(id=form.cleaned_data.get('id')).first()                
                emp.full_name = full_name
                emp.cpf = cpf
                emp.rg = rg
                emp.pis = pis
                emp.ctps = ctps
                emp.birthdate = birthdate
                emp.phone_number = phone_number
                emp.cellphone_number = cellphone_number
                emp.email = email
                emp.post_code = post_code
                emp.state = state
                emp.city = city
                emp.district = district
                emp.address = address
                emp.number = number
                emp.complement = complement
                emp.bank = bank
                emp.agency = agency
                emp.account = account
                emp.account_type = account_type
                emp.contract = contract
                emp.situation = situation
                emp.payment_type = payment_type
                emp.company = Companies.objects(id=company).first()
                emp.costcenter = CostCenters.objects(id=costcenter).first()
                emp.department = Departments.objects(id=department).first()
                emp.function = Functions.objects(id=function).first()
                emp.admission_date = admission_date
                emp.experience_end_date = experience_end_date
                emp.resignation_date = resignation_date
                emp.resignation_reason = resignation_reason
                emp.last_salary = last_salary 
               
                messages.success(request, 'Dados atualizados!')
                emp.save()
                disconnect()
                return redirect('employee-detail', id=emp.id)

    elif not id: 
        form = EmployeesForm()
    elif id: 
        disconnect()
        connect('eagle')
        emp = Employees.objects(id=id).first()
        emp_instance = {
            'id': emp.id,
            'full_name': emp.full_name,
            'cpf': emp.cpf,
            'rg': emp.rg,
            'pis': emp.pis,
            'ctps': emp.ctps,
            'birthdate': emp.birthdate.strftime('%d/%m/%Y'),
            'phone_number': emp.phone_number,
            'cellphone_number': emp.cellphone_number,
            'email': emp.email,
            'post_code': emp.post_code,
            'state': emp.state,
            'city': emp.city,
            'district': emp.district,
            'address': emp.address,
            'number': emp.number,
            'complement': emp.complement,
            'bank': emp.bank,
            'agency': emp.agency,
            'account': emp.account,
            'account_type': emp.account_type,
            'contract': emp.contract,
            'situation': emp.situation,
            'payment_type': emp.payment_type,
            'company': str(emp.company.id),
            'costcenter': str(emp.costcenter.id),
            'department': str(emp.department.id),
            'function': str(emp.function.id),
            'admission_date': emp.admission_date.strftime('%d/%m/%Y'),
            'experience_end_date': emp.experience_end_date.strftime('%d/%m/%Y'),
            'resignation_date': emp.resignation_date, #.strftime('%d/%m/%Y'),
            'resignation_reason': emp.resignation_reason,
            'last_salary': emp.last_salary,
        }

        disconnect()
        form = EmployeesForm(initial=emp_instance)
        title = 'Editar Funcionário'

    
    context = { 'user_data': user_data, 'form': form, 'title': title }
    return render(request, template, context)

def delete(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    emp = Employees.objects(id=id).first()
    emp.delete()
    disconnect()

    messages.error(request, 'O funcionário <b>%s</b> foi excluído.' % emp.full_name)

    return redirect('employee-list')
