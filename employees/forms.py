from django import forms
from django.core.exceptions import ValidationError
from mongoengine import connect, disconnect
from mongoengine.queryset.visitor import Q
from eagle.static.eagle import constants
from configuration.models import Companies, Departments, Functions, CostCenters
from .models import Employees

class EmployeesForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)

    #funcionario
    full_name = forms.CharField(label='Nome Completo', max_length=100, error_messages={'required': 'Por favor, preencha este campo'}, required=True)
    cpf = forms.CharField(label='CPF', max_length=100, error_messages={'required': 'Por favor, preencha este campo'}, required=True)
    rg = forms.CharField(label='RG', max_length=100, error_messages={'required': 'Por favor, preencha este campo'}, required=True)
    pis = forms.CharField(label='PIS', max_length=100, required=False)
    ctps = forms.CharField(label='CTPS', max_length=100, required=False)
    birthdate = forms.DateField(label='Data de Nascimento', required=True, error_messages={'required': 'Por favor, preencha este campo'}, localize=True)
    phone_number = forms.CharField(label='Telefone Residencial', max_length=100, error_messages={'required': 'Por favor, preencha este campo'}, required=False)
    cellphone_number = forms.CharField(label='Telefone Celular', max_length=100, error_messages={'required': 'Por favor, preencha este campo'}, required=False)
    email = forms.EmailField(label='E-mail', max_length=200, required=True, error_messages={'required': 'Por favor, preencha este campo', 'invalid': 'Por favor, preencha um e-mail válido'})
    #endereço
    post_code = forms.CharField(label='CEP', max_length=100, required=False)
    state = forms.ChoiceField(label='Estado', required=False, choices=constants.STATES)
    city = forms.CharField(label='Cidade', max_length=100, required=False)
    district = forms.CharField(label='Bairro', max_length=100, required=False)
    address = forms.CharField(label='Endereço', max_length=100, required=False)
    number = forms.CharField(label='Número', max_length=100, required=False)
    complement = forms.CharField(label='Complemento', max_length=100, required=False)
    
    #dados bancários
    bank = forms.ChoiceField(label='Estado', required=False, choices=constants.BANKS)
    agency = forms.CharField(label='Agência', required=False)
    account = forms.CharField(label='Conta', required=False)
    account_type = forms.ChoiceField(label='Tipo de Conta', required=False, choices=(('corrente', 'Corrente'), ('poupanca', 'Poupança')))
    
    #empresa
    contract = forms.ChoiceField(label='Contrato', error_messages={'required': 'Por favor, selecione uma opção'}, choices=(
        ('clt', 'CLT'), 
        ('temporary', 'Temporário'),
        ('undefined', 'Indefinido')
    ))
    situation = forms.ChoiceField(label='Situação', error_messages={'required': 'Por favor, selecione uma opção'}, choices=(
        ('waiting_admission', 'Aguardando Admissão'), 
        ('employeed', 'Contrato Ativo'),
        ('vacation', 'Em Férias'),
        ('dismissed', 'Desligado'),
    ))
    payment_type = forms.ChoiceField(label='Tipo de Pagamento', error_messages={'required': 'Por favor, selecione uma opção'}, choices=(('hour', 'Horista'), ('day', 'Diarista'), ('month', 'Mensalista')))
    company = forms.ChoiceField(label='Empresa', error_messages={'required': 'Por favor, selecione uma opção'})
    costcenter = forms.ChoiceField(label='Centro de Custo', error_messages={'required': 'Por favor, selecione uma opção'})
    department = forms.ChoiceField(label='Departamento', error_messages={'required': 'Por favor, selecione uma opção'})
    function = forms.CharField(label='Cargo', error_messages={'required': 'Por favor, selecione uma opção'})
    admission_date = forms.DateField(label='Data de Admissão', required=True, error_messages={'required': 'Por favor, preencha este campo'})
    experience_end_date = forms.DateField(label='Término da Experiencia', required=False)
    resignation_date = forms.DateField(label='Data de Desligamento', required=False)
    resignation_reason = forms.CharField(label='Motivo de Desligamento', required=False)
    last_salary = forms.FloatField(label='Salário', error_messages={'required': 'Por favor, preencha este campo'}, localize=True)

    # is_manager = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super(EmployeesForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')

        initial_arguments = kwargs.get('initial', None)
        initial_data = args[0] if args else None

        if initial_arguments:
            company = initial_arguments.get('company', None)
            costcenter = initial_arguments.get('costcenter', None)
            department = initial_arguments.get('department', None)
        elif initial_data: 
            company = args[0].get('company', None)
            costcenter = args[0].get('costcenter', None)
            department = args[0].get('department', None)
        else:
            company = None
            costcenter = None
            department = None
            
        company_list = Companies.objects.all()
        company_options = []
        function_options = []
        costcenter_options = []
        department_options = []

        if company:
            costcenter_list = CostCenters.objects.filter(company=company).all()
        else: 
            costcenter_list = CostCenters.objects.all()

        if costcenter:
            department_list = Departments.objects.filter(costcenters__icontains=costcenter)
        else: 
            department_list = Departments.objects.all()

        if department:
            function_list = Functions.objects.filter(departments__icontains=department)
        else: 
            function_list = Functions.objects.all()


        for comp in company_list: 
            company_options.append((str(comp.id), comp.company_name))

        for cdc in costcenter_list: 
            costcenter_options.append((str(cdc.id), cdc.name))
        
        for dep in department_list: 
            department_options.append((str(dep.id), dep.name))

        for fun in function_list: 
            function_options.append((str(fun.id), "{} {}".format(fun.name, 'Junior' if fun.level == 'junior' else 'Pleno' if fun.level == 'pleno' else 'Senior' if fun.level == 'senior' else 'Especialista' if fun.level == 'expert' else '')))

        disconnect()
        self.fields['company'].choices = company_options
        self.fields['costcenter'].choices = costcenter_options
        self.fields['department'].choices = department_options
        self.fields['function'].choices = function_options


    def clean(self):
        id = self.cleaned_data.get('id')
        cpf = self.cleaned_data.get('cpf')
        rg = self.cleaned_data.get('rg')
        pis = self.cleaned_data.get('pis')
        ctps = self.cleaned_data.get('ctps')

        disconnect()
        connect('eagle')

        if not id:
            emp_cpf = Employees.objects.filter(cpf=cpf).first()
            emp_rg = Employees.objects.filter(rg=rg).first()
            emp_pis = Employees.objects.filter(pis=pis).first()
            emp_ctps = Employees.objects.filter(ctps=ctps).first()
        else: 
            emp_cpf = Employees.objects.filter(cpf=cpf).filter(id__ne=id).first()
            emp_rg = Employees.objects.filter(rg=rg).filter(id__ne=id).first()
            emp_pis = Employees.objects.filter(pis=pis).filter(id__ne=id).first()
            emp_ctps = Employees.objects.filter(ctps=ctps).filter(id__ne=id).first()

        if emp_cpf: 
            self.add_error('cpf', 'Desculpe, este funcionário já está cadastrado')
        if emp_rg: 
            self.add_error('rg', 'Desculpe, este funcionário já está cadastrado')
        if emp_pis and pis != '': 
            self.add_error('pis', 'Desculpe, este funcionário já está cadastrado')
        if emp_ctps and ctps != '': 
            self.add_error('ctps', 'Desculpe, este funcionário já está cadastrado')

        disconnect()

class FilterForm(forms.Form):
    search = forms.CharField(label='Pesquise', required=False)
    empresa = forms.CharField(label='Empresa', required=False)
    contract = forms.CharField(label='Contrato', required=False)
    situation = forms.CharField(label='Situação', required=False)
    payment_type = forms.CharField(label='Tipo de Pagamento', required=False)
    costcenter = forms.CharField(label='Centro de Custo', required=False)
    department = forms.CharField(label='Departamento', required=False)
    function = forms.CharField(label='Função', required=False)

    # def __init__(self, *args, **kwargs):
    #     super(FilterForm, self).__init__(*args, **kwargs)
    #     disconnect()
    #     connect('eagle')

    #     company_list = Companies.objects.all()
    #     costcenter_list = CostCenters.objects.all()
    #     department_list = Departments.objects.all()
    #     function_list = Functions.objects.all()
    #     company_options = []
    #     costcenter_options = []
    #     department_options = []
    #     function_options = []

    #     for comp in company_list: 
    #         company_options.append((str(comp.id), comp.company_name))

    #     for cdc in costcenter_list: 
    #         costcenter_options.append((str(cdc.id), cdc.name))

    #     for dep in department_list: 
    #         department_options.append((str(cdc.id), cdc.company_name))

    #     for fun in function_list: 
    #         function_options.append((str(fun.id), fun.company_name))

    #     disconnect()
    #     self.fields['contract'].choices = (('clt', 'CLT'),('temporary', 'Temporário'),('undefined', 'Indefinido'))
    #     self.fields['situation'].choices = (('waiting_admission', 'Aguardando Admissão'),('employeed', 'Contrato Ativo'),('vacation', 'Em Férias'),('dismissed', 'Desligado'))
    #     self.fields['payment_type'].choices = (('hour', 'Horista'), ('day', 'Diarista'), ('month', 'Mensalista'))
    #     self.fields['company'].choices = company_options
    #     self.fields['costcenter'].choices = costcenter_options
    #     self.fields['department'].choices = department_options
    #     self.fields['function'].choices = department_options
