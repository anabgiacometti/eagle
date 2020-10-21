from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from mongoengine import connect, disconnect
from authentication.views import get_logged
from django.contrib import messages
from mongoengine.queryset.visitor import Q
from .models import Functions
from .forms import FunctionsForm, FunctionsFilterForm


#Cargos

def function_list(request):
    template = 'configuration/function-list.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    filter = FunctionsFilterForm(request.GET)

    disconnect()
    connect('eagle')

    list = Functions.objects()
    
    disconnect()

    if filter.is_valid():
        search = filter.cleaned_data.get('search', None)
        has_commission = filter.cleaned_data.get('has_commission', None)
        level = filter.cleaned_data.get('level', None)
        permission = filter.cleaned_data.get('permission', None)
        is_active = filter.cleaned_data.get('is_active', None)

        if search: 
            list = list.filter(Q(name__icontains=search))
        if has_commission == 'yes': 
            list = list.filter(has_commission=True)
        elif has_commission == 'no':
            list = list.filter(has_commission=False)
        if level: 
            list = list.filter(level=level)
        elif permission:
            list = list.filter(permissions__icontains=permission)
        if is_active == 'yes': 
            list = list.filter(is_active=True)
        elif is_active == 'no':
            list = list.filter(is_active=False)

    context = { 'user_data': user_data, 'list': list.order_by('name'), 'form': filter }
    return render(request, template, context)
    

def function_detail(request, id=None):
    template = 'configuration/function-detail.html'
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    title = 'Novo Cargo'

    if request.method == 'POST': 
        form = FunctionsForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data.get('name')
            salary = form.cleaned_data.get('salary')
            work_days = form.cleaned_data.get('work_days')
            #workload = form.cleaned_data.get('workload')
            #flexible_schedule = form.cleaned_data.get('_flexible_schedule')
            #entry_hour = form.cleaned_data.get('_entry_hour')
            #exit_hour = form.cleaned_data.get('exit_hour')
            #lunch_time = form.cleaned_data.get('lunch_time')
            level = form.cleaned_data.get('level')
            permissions = form.cleaned_data.get('permissions')
            departments = form.cleaned_data.get('departments')
            has_commission = form.cleaned_data.get('has_commission')
            comission_percentage = form.cleaned_data.get('comission_percentage') if form.cleaned_data.get('comission_percentage') else None
            comission_floor = form.cleaned_data.get('comission_floor') if form.cleaned_data.get('comission_floor') else None
            comission_ceil = form.cleaned_data.get('comission_ceil') if form.cleaned_data.get('comission_ceil') else None
            
            disconnect()
            connect('eagle')

            if not form.cleaned_data.get('id'):
                function = Functions(
                    name =name,
                    salary =salary,
                    work_days =work_days,
                    # workload =workload,
                    # flexible_schedule =flexible_schedule,
                    # entry_hour =entry_hour,
                    # exit_hour =exit_hour,
                    # lunch_time =lunch_time,
                    level =level,
                    permissions =permissions,
                    has_commission =has_commission,
                    comission_percentage =comission_percentage,
                    comission_floor =comission_floor,
                    comission_ceil =comission_ceil,
                    departments=departments
                    )
                messages.success(request, 'O cargo <b>%s</b> foi cadastrado com sucesso!' % function.name)
                function.save()
                disconnect()
                return redirect('function-list')
            else:
                title = 'Editar Cargo'
                function = Functions.objects(id=form.cleaned_data.get('id')).first()
                function.name = name
                function.salary = salary
                function.work_days = work_days
                # function.workload =workload
                # function.flexible_schedule =flexible_schedule
                # function.entry_hour =entry_hour
                # function.exit_hour =exit_hour
                # function.lunch_time =lunch_time
                function.level = level
                function.permissions = permissions
                function.has_commission = has_commission
                function.comission_percentage = comission_percentage
                function.comission_ceil = comission_ceil
                function.comission_floor = comission_floor
                function.departments = departments
                function.save()
                messages.success(request, 'Dados atualizados!')
                disconnect()
                return redirect('function-detail', id=function.id)

    elif not id: 
        form = FunctionsForm(initial={'work_days': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday']})
    elif id: 
        disconnect()
        connect('eagle')
        function = Functions.objects(id=id).first()
        disconnect()
        function_instance = {
            'id': function.id,
            'name': function.name,
            'salary': function.salary,
            'work_days': function.work_days,
            # 'workload': function.workload,
            # 'flexible_schedule': function.flexible_schedule,
            # 'entry_hour': function.entry_hour,
            # 'exit_hour': function.exit_hour,
            # 'lunch_time': function.lunch_time,
            'level': function.level,
            'permissions': function.permissions,
            'has_commission': function.has_commission,
            'comission_percentage': function.comission_percentage,
            'comission_ceil': function.comission_ceil,
            'comission_floor': function.comission_floor,
            'departments': function.departments
            }
        form = FunctionsForm(initial=function_instance)
        title = 'Editar Cargo'

    
    context = { 'user_data': user_data, 'form': form, 'title': title }
    return render(request, template, context)


def function_deactivate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    func = Functions.objects(id=id).first()
    func.is_active = False
    func.save()
    disconnect()

    messages.warning(request, 'O cargo <b>%s</b> foi desativado.' % func.name)

    return redirect('function-list')

def function_activate(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    func = Functions.objects(id=id).first()
    func.is_active = True
    func.save()
    disconnect()

    messages.success(request, 'O cargo <b>%s</b> foi ativado.' % func.name)

    return redirect('function-list')


def function_delete(request, id):
    user_data = get_logged(request)

    if not user_data: 
        return redirect('login')

    disconnect()
    connect('eagle')
    func = Functions.objects(id=id).first()
    func.delete()
    disconnect()

    messages.error(request, 'O cargo <b>%s</b> foi excluído.' % func.name)

    return redirect('function-list')

def get_salary(request, id):
    disconnect()
    connect('eagle')
    depto = Functions.objects(id=id).first()
    disconnect()

    return JsonResponse(depto.salary, safe=False)


def search_functions(request, department):
    disconnect()
    connect('eagle')
    functions = Functions.objects().filter(departments__icontains=department)
    options = []
    for i in functions: 
        options.append({'id':str(i.id), 'name':'{} {}'.format(i.name, 'Junior' if i.level == 'junior' else 'Pleno' if i.level == 'pleno' else 'Senior' if i.level == 'senior' else 'Especialista' if i.level == 'expert' else '')})

    return JsonResponse(options, safe=False)
