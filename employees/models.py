from django.db import models
from mongoengine import *
from configuration.models import Functions, Departments, Companies, CostCenters

# Create your models here.

class Employees(Document):
	#funcionario
    full_name = StringField(max_length=500, required=True)
    cpf = StringField(max_length=20, required=True)
    rg = StringField(max_length=20, required=True)
    pis = StringField(max_length=50, required=True)
    ctps = StringField(max_length=50, required=True)
    birthdate = DateTimeField(required=True, localize=True)
    phone_number = StringField(max_length=50, required=True)
    cellphone_number = StringField(max_length=50, required=True)
    email = EmailField(max_length=200, required=True)

    post_code = StringField(max_length=10, required=False)
    state = StringField(max_length=255, required=False)
    city = StringField(max_length=255, required=False)
    district = StringField(max_length=255, required=False)
    address = StringField(max_length=255, required=False)
    number = StringField(max_length=255, required=False)
    complement = StringField(max_length=255, required=False)
    
    bank = StringField(max_length=255, required=False)
    agency = StringField(max_length=50, required=False)
    account = StringField(max_length=50, required=False)
    account_type = StringField(max_length=50, required=False)
    
    contract = StringField(max_length=50, required=False)
    situation = StringField(max_length=50, required=False)
    payment_type = StringField(max_length=50, required=False)
    company = ReferenceField(Companies, reverse_delete_rule=CASCADE, required=True)
    costcenter = ReferenceField(CostCenters, reverse_delete_rule=CASCADE, required=True)
    department = ReferenceField(Departments, reverse_delete_rule=CASCADE, required=True)
    function = ReferenceField(Functions, reverse_delete_rule=CASCADE, required=True) 
    admission_date = DateTimeField(required=True)
    experience_end_date = DateTimeField(required=False)
    resignation_date = DateTimeField(required=False)
    resignation_reason = StringField(max_length=2000, required=False)
    last_salary = DecimalField(required=False)

    # is_manager = BooleanField(required=True, deafult=False)

    # is_active = BooleanField(required=True, default=True)