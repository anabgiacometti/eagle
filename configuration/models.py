from django.db import models
from mongoengine import *

class Companies(Document):
    company_type = StringField(max_length=50, required=True)
    code = StringField(max_length=50, required=True)
    company_headoffice = ReferenceField('self', reverse_delete_rule=CASCADE, required=False)
    cnpj = StringField(max_length=20, required=True)
    ie = StringField(max_length=20, required=True)
    has_exemptiom_ie = BooleanField(default=False, required=True)
    bussiness_name = StringField(max_length=255, required=True)
    company_name = StringField(max_length=255, required=True)
    company_tax_type = StringField(max_length=20, required=True)
    post_code = StringField(max_length=10, required=False)
    state = StringField(max_length=255, required=False)
    city = StringField(max_length=255, required=False)
    district = StringField(max_length=255, required=False)
    address = StringField(max_length=255, required=False)
    number = StringField(max_length=255, required=False)
    complement = StringField(max_length=255, required=False)
    is_active = BooleanField(default=True, required=True)

class CostCenters(Document):
    name = StringField(max_length=200, required=True)
    type = StringField(max_length=50, required=True)
    code = StringField(max_length=9, required=True)
    is_active = BooleanField(default=True, required=True)
    warehouses = ListField()
    company = ReferenceField(Companies, reverse_delete_rule=CASCADE, required=True)

class Departments(Document):
    name = StringField(max_length=200, required=True)
    description = StringField(required=False)
    costcenters = ListField()
    is_active = BooleanField(default=True, required=True)

class Functions(Document):
    name = StringField(max_length=200, required=True)
    salary = DecimalField(required=True)
    work_days = ListField()
    # workload = StringField(max_length=10, required=True)
    # flexible_schedule = BooleanField(default=False, required=True)
    # entry_hour = StringField(max_length=10, required=False)
    # exit_hour = StringField(max_length=10, required=False)
    # lunch_time = StringField(max_length=10, required=False)
    level = StringField(max_length=50, required=True)
    permissions = ListField()
    departments = ListField()
    has_commission = BooleanField(default=False, required=True)
    comission_percentage = DecimalField(required=False)
    comission_floor = DecimalField(required=False)
    comission_ceil = DecimalField(required=False)
    is_active = BooleanField(default=True, required=True)

class WareHouses(Document):
    name = StringField(max_length=200, required=True)
    permissions = ListField()
    is_active = BooleanField(default=True, required=True)
    
