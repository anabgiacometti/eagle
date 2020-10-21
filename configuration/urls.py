from django.urls import path

from . import companies, departments, functions, costcenters, warehouses

urlpatterns = [
    #Empresas
    path('company/list/', companies.company_list, name='company-list'),
    path('company/detail/', companies.company_detail, name='company-detail'),
    path('company/detail/<id>', companies.company_detail, name='company-detail'),
    path('company/deactivate/<id>', companies.company_deactivate, name='company-deactivate'),
    path('company/activate/<id>', companies.company_activate, name='company-activate'),
    path('company/delete/<id>', companies.company_delete, name='company-delete'),
    path('company/search/<id>', companies.company_search, name='company-search'),
	#Centros de Custo
    path('costcenter/list/', costcenters.costcenter_list, name='costcenter-list'),
    path('costcenter/detail/', costcenters.costcenter_detail, name='costcenter-detail'),
    path('costcenter/detail/<id>', costcenters.costcenter_detail, name='costcenter-detail'),
    path('costcenter/deactivate/<id>', costcenters.costcenter_deactivate, name='costcenter-deactivate'),
    path('costcenter/activate/<id>', costcenters.costcenter_activate, name='costcenter-activate'),
    path('costcenter/delete/<id>', costcenters.costcenter_delete, name='costcenter-delete'),
    path('costcenter/search/<company>', costcenters.costcenter_search, name='costcenter-search'),
    #Departamentos
    path('department/list/', departments.department_list, name='department-list'),
    path('department/detail/', departments.department_detail, name='department-detail'),
    path('department/detail/<id>', departments.department_detail, name='department-detail'),
    path('department/deactivate/<id>', departments.department_deactivate, name='department-deactivate'),
    path('department/activate/<id>', departments.department_activate, name='department-activate'),
    path('department/delete/<id>', departments.department_delete, name='department-delete'),
    path('department/search/<costcenter>', departments.department_search, name='department-search'),
    #Cargos
    path('function/list/', functions.function_list, name='function-list'),
    path('function/detail/', functions.function_detail, name='function-detail'),
    path('function/detail/<id>', functions.function_detail, name='function-detail'),
    path('function/deactivate/<id>', functions.function_deactivate, name='function-deactivate'),
    path('function/activate/<id>', functions.function_activate, name='function-activate'),
    path('function/delete/<id>', functions.function_delete, name='function-delete'),
    path('function/get-salary/<id>', functions.get_salary, name='function-get-salary'),
    path('function/search/<department>', functions.search_functions, name='function-search'),
    #Depósitios
    path('warehouse/list/', warehouses.warehouse_list, name='warehouse-list'),
    path('warehouse/detail/', warehouses.warehouse_detail, name='warehouse-detail'),
    path('warehouse/detail/<id>', warehouses.warehouse_detail, name='warehouse-detail'),
    path('warehouse/deactivate/<id>', warehouses.warehouse_deactivate, name='warehouse-deactivate'),
    path('warehouse/activate/<id>', warehouses.warehouse_activate, name='warehouse-activate'),
    path('warehouse/delete/<id>', warehouses.warehouse_delete, name='warehouse-delete'),
]