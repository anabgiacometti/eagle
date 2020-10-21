from django import forms
from django.core.exceptions import ValidationError
from mongoengine import connect, disconnect
from .models import Departments, Functions, CostCenters, Companies, WareHouses
from eagle.static.eagle import constants

class CompaniesForm(forms.Form):

    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    company_type = forms.ChoiceField(label='Tipo de Empresa', required=True, error_messages={'required': 'Por favor, selecione uma opção'}, choices=(
        ('headoffice', 'Matriz'), 
        ('branch', 'Filial')
    ))
    company_headoffice = forms.ChoiceField(label='Matriz', required=False)
    cnpj = forms.CharField(label='CNPJ', max_length=20, error_messages={'required': 'Por favor, preencha este campo'})
    code = forms.CharField(label='Código', max_length=20, error_messages={'required': 'Por favor, preencha este campo'})
    ie = forms.CharField(label='IE', max_length=20, required=False)
    has_exemptiom_ie = forms.BooleanField(label='Isento de IE', required=False)
    bussiness_name = forms.CharField(label='Razão Social', max_length=255, error_messages={'required': 'Por favor, preencha este campo'})
    company_name = forms.CharField(label='Nome Fantasia', max_length=255, error_messages={'required': 'Por favor, preencha este campo'})
    company_tax_type = forms.ChoiceField(label='Regime Tributário', required=True, error_messages={'required': 'Por favor, selecione uma opção'}, choices=(
        ('lucro_real', 'Lucro Real'), 
        ('lucro_presumido', 'Lucro Presumido'),
        ('simples_nacional', 'Simples Nacional')
    ))
    post_code = forms.CharField(label='CEP', max_length=100, required=False)
    state = forms.ChoiceField(label='Estado', required=False, choices=constants.STATES)
    city = forms.CharField(label='Cidade', max_length=100, required=False)
    district = forms.CharField(label='Bairro', max_length=100, required=False)
    address = forms.CharField(label='Endereço', max_length=100, required=False)
    number = forms.CharField(label='Número', max_length=100, required=False)
    complement = forms.CharField(label='Complemento', max_length=100, required=False)

    def __init__(self, *args, **kwargs):
        super(CompaniesForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')
        company_list = Companies.objects.filter(company_type='headoffice').all()
        company_options = []

        for comp in company_list: 
            company_options.append((comp.id, comp.company_name))

        disconnect()
        self.fields['company_headoffice'].choices = company_options

    def clean(self):
        id = self.cleaned_data.get('id')
        code = self.cleaned_data.get('code')
        cnpj = self.cleaned_data.get('cnpj')
        ie = self.cleaned_data.get('ie')
        has_exemptiom_ie = self.cleaned_data.get('has_exemptiom_ie')
        company_type = self.cleaned_data.get('company_type')
        company_headoffice = self.cleaned_data.get('company_headoffice')

        #check for duplicates
        disconnect()
        connect('eagle')

        if not id:
            company = Companies.objects(cnpj=cnpj).first()
            code = Companies.objects(code=code).first()
        else: 
            company = Companies.objects.filter(cnpj=cnpj).filter(id__ne=id).first()
            code = Companies.objects.filter(code=code).filter(id__ne=id).first()

        disconnect()
        
        if company: 
            self.add_error('cnpj', 'Desculpe, este CNPJ já está cadastrado')

        if code: 
            self.add_error('code', 'Desculpe, este código já está cadastrado')

        #check for IE
        if not has_exemptiom_ie and not ie: 
            self.add_error('ie', 'Por favor, preencha este campo')

        #check for headoffice
        if company_type == 'branch' and not company_headoffice: 
            self.add_error('company_headoffice', 'Por favor, selecione uma opção')


#Centros de Custo
class CostCentersForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    # manager = StringField(max_length=)
    warehouses = forms.MultipleChoiceField(label='Depósitos')
    company = forms.ChoiceField(label='Empresa', error_messages={'required': 'Por favor, selecione uma opção'})
    code = forms.CharField(label='Código', max_length=20, error_messages={'required': 'Por favor, preencha este campo'})
    costcenter_type = forms.ChoiceField(label='Tipo de Centro de Custo', required=True, error_messages={'required': 'Por favor, selecione uma opção'}, choices=(
        ('production', 'Produção'), 
        ('sales', 'Vendas'),
        ('services', 'Serviços'),
    ))

    def __init__(self, *args, **kwargs):
        super(CostCentersForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')
        company_list = Companies.objects.all()
        warehouse_list = WareHouses.objects.all()
        company_options = []
        warehouse_options = []
        for comp in company_list: 
            company_options.append((str(comp.id), '{} - {}'.format(comp.code, comp.company_name)))
        for wh in warehouse_list: 
            warehouse_options.append((str(wh.id), wh.name))
        disconnect()
        
        self.fields['company'].choices = company_options
        self.fields['warehouses'].choices = warehouse_options
    
    def clean(self):
        id = self.cleaned_data.get('id')
        name = self.cleaned_data.get('name')
        code = self.cleaned_data.get('code')
        company = self.cleaned_data.get('company')
        type = self.cleaned_data.get('costcenter_type')

        disconnect()
        connect('eagle')

        if not id:
            name = CostCenters.objects(name=name).filter(company=company).filter(type=type).first()
            code = CostCenters.objects(code=code).filter(company=company).filter(type=type).first()
        else: 
            name = CostCenters.objects.filter(name=name).filter(company=company).filter(type=type).filter(id__ne=id).first()
            code = CostCenters.objects.filter(code=code).filter(company=company).filter(type=type).filter(id__ne=id).first()

        disconnect()

        if name: 
            self.add_error('name', 'Desculpe, este centro de custo já está cadastrado')

        if code: 
            self.add_error('code', 'Desculpe, este código já está cadastrado')

#Departamentos
class DepartmentsForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    # manager = StringField(max_length=)
    costcenters = forms.MultipleChoiceField(label='Centro de Custo', required=False)
    description = forms.CharField(label='Descrição', required=False)

    def __init__(self, *args, **kwargs):
        super(DepartmentsForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')
        cdc_list = CostCenters.objects.all()
        cdc_options = []

        for cdc in cdc_list: 
            cdc_options.append((str(cdc.id), '{}-{} - {}'.format(cdc.company.code, cdc.code, cdc.name)))

        disconnect()
        self.fields['costcenters'].choices = cdc_options

    def clean(self):
        name = self.cleaned_data.get('name')
        id = self.cleaned_data.get('id')

        disconnect()
        connect('eagle')

        if not id:
            department = Departments.objects(name=name).first()
        else: 
            department = Departments.objects.filter(name=name).filter(id__ne=id).first()

        disconnect()

        if department: 
            self.add_error('name', 'Desculpe, este Departamento já está cadastrado')

#Cargos
class FunctionsForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    salary = forms.DecimalField(label='Salário', widget=forms.TextInput(), error_messages={'required': 'Por favor, preencha este campo'}, localize=True)
    work_days = forms.MultipleChoiceField(label='Dias Trabalhados', required=False, widget=forms.CheckboxSelectMultiple(), 
        choices=(
            ('sunday', 'Domingo'), 
            ('monday', 'Segunda-Feira'),
            ('tuesday', 'Terça-Feira'),
            ('wednesday', 'Quarta-Feira'),
            ('thursday', 'Quinta-Feira'),
            ('friday', 'Sexta-Feira'),
            ('saturday', 'Sábado'),
        )
    )
    # workload = forms.CharField(label='Carga Horária', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    # flexible_schedule = forms.BooleanField(required=False)
    # entry_hour = forms.CharField(label='Horário de Entrada', max_length=100, required=False)
    # exit_hour = forms.CharField(label='Horário de Saída', max_length=100, required=False)
    # lunch_time = forms.CharField(label='Tempo de Almoço', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    level = forms.ChoiceField(label='Nível', required=True, error_messages={'required': 'Por favor, selecione uma opção'}, choices=(
        ('junior', 'Júnior'), 
        ('pleno', 'Pleno'),
        ('senior', 'Sênior'),
        ('expert', 'Especialista'),
        ('none', 'Não se Aplica')
    ))
    permissions = forms.MultipleChoiceField(label='Permissões', required=False, widget=forms.CheckboxSelectMultiple(), 
        choices=(
            ('make_sale', 'Realizar Vendas'), 
            ('list_sale', 'Visualizar Vendas'),
            ('cancel_sale', 'Cancelar Vendas'),
            ('edit_sale', 'Editar Vendas')
        )
    )
    departments = forms.MultipleChoiceField(label='Departamentos', required=False, widget=forms.CheckboxSelectMultiple())
    has_commission = forms.BooleanField(required=False)
    comission_percentage = forms.DecimalField(label='Percentual de Comissão', required=False, localize=True)
    comission_floor = forms.DecimalField(label='Teto de Comissão', required=False, localize=True)
    comission_ceil = forms.DecimalField(label='Piso de Comissão', required=False, localize=True)

    def __init__(self, *args, **kwargs):
        super(FunctionsForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')
        departments_list = Departments.objects.all().order_by('name')
        departments_options = []

        for dep in departments_list: 
            departments_options.append((str(dep.id), dep.name))

        disconnect()
        self.fields['departments'].choices = departments_options
   
    def clean(self):
        #check for duplicates
        #check fields
        #if not flexible_schedule then entry_hour and exit_hour 
        #if comissions then comission_percentage
        id = self.cleaned_data.get('id')
        name = self.cleaned_data.get('name')
        level = self.cleaned_data.get('level')
        # flexible_schedule = self.cleaned_data.get('flexible_schedule')
        # entry_hour = self.cleaned_data.get('entry_hour')
        # exit_hour = self.cleaned_data.get('exit_hour')
        has_commission = self.cleaned_data.get('has_commission')
        comission_percentage = self.cleaned_data.get('comission_percentage')

        disconnect()
        connect('eagle')

        if not id:
            function = Functions.objects.filter(name=name).filter(level=level).first()
        else: 
            function = Functions.objects.filter(name=name).filter(level=level).filter(id__ne=id).first()

        disconnect()

        if function: 
            self.add_error('name', 'Desculpe, este cargo já está cadastrado')
            self.add_error('level', 'Desculpe, este cargo já está cadastrado')

        # if not flexible_schedule: 
        #     if not entry_hour: 
        #         self.add_error('entry_hour', 'Por favor, preencha este campo')

        #     if not exit_hour: 
        #         self.add_error('exit_hour', 'Por favor, preencha este campo')

        if has_commission: 
            if not comission_percentage: 
                self.add_error('comission_percentage', 'Por favor, preencha este campo')
 
#Depósitos
class WareHousesForm(forms.Form):
    id = forms.CharField(widget=forms.HiddenInput(), required=False)
    name = forms.CharField(label='Nome', max_length=100, error_messages={'required': 'Por favor, preencha este campo'})
    permissions = forms.MultipleChoiceField(label='Centro de Custo', required=False, choices=(
            ('entry', 'Entrada'), 
            ('sale', 'Saída por Vendas'),
            ('removal', 'Saída por Baixa'),
            ('transfer', 'Saída por Transferência')
        ))

    def clean(self):
        name = self.cleaned_data.get('name')
        id = self.cleaned_data.get('id')

        disconnect()
        connect('eagle')

        if not id:
            warehouse = WareHouses.objects(name=name).first()
        else: 
            warehouse = WareHouses.objects.filter(name=name).filter(id__ne=id).first()

        disconnect()

        if warehouse: 
            self.add_error('name', 'Desculpe, este depósito já está cadastrado')


class CompaniesFilterForm(forms.Form):
    search = forms.CharField(label='Pesquise', required=False)
    company_type = forms.CharField(label='Tipoe de Empresa', required=False)
    company_tax_type = forms.CharField(label='Regime Tributário', required=False)
    is_active = forms.CharField(required=False)

class CostCentersFilterForm(forms.Form):
    search = forms.CharField(label='Pesquise', required=False)
    type = forms.CharField(required=False)
    company = forms.CharField(required=False)
    is_active = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(CostCentersFilterForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')
        company_list = Companies.objects.all()
        company_options = []

        for comp in company_list: 
            company_options.append((str(comp.id), '{} - {}'.format(comp.code, comp.company_name)))

        disconnect()
        self.fields['company'].choices = company_options

class DepartmentsFilterForm(forms.Form):
    search = forms.CharField(required=False)
    costcenter = forms.CharField(required=False)
    company = forms.CharField(required=False)
    is_active = forms.CharField(required=False)

    def __init__(self, *args, **kwargs):
        super(DepartmentsFilterForm, self).__init__(*args, **kwargs)
        disconnect()
        connect('eagle')
        cdc_list = CostCenters.objects.all().order_by('company.code')
        company_list = Companies.objects.all().order_by('company.code')
        cdc_options = []
        company_options = []

        for cdc in cdc_list: 
            cdc_options.append((str(cdc.id), '{}-{} - {}'.format(cdc.company.code, cdc.code, cdc.name)))

        for company in company_list: 
            company_options.append((str(company.id), '{} - {}'.format(company.code, company.company_name)))

        disconnect()
        self.fields['costcenter'].choices = cdc_options
        self.fields['company'].choices = company_options

class FunctionsFilterForm(forms.Form):
    search = forms.CharField(label='Pesquise', required=False)
    has_commission = forms.CharField(required=False)
    permission = forms.ChoiceField(required=False, choices=(
            ('make_sale', 'Realizar Vendas'), 
            ('list_sale', 'Visualizar Vendas'),
            ('cancel_sale', 'Cancelar Vendas'),
            ('edit_sale', 'Editar Vendas')
        ))
    level = forms.CharField(required=False)
    is_active = forms.CharField(required=False)

class WareHousesFilterForm(forms.Form):
    search = forms.CharField(label='Pesquise', required=False)
    has_commission = forms.CharField(required=False)
    permission = forms.ChoiceField(required=False, choices=(
            ('make_sale', 'Realizar Vendas'), 
            ('list_sale', 'Visualizar Vendas'),
            ('cancel_sale', 'Cancelar Vendas'),
            ('edit_sale', 'Editar Vendas')
        ))
    level = forms.CharField(required=False)
    is_active = forms.CharField(required=False)
