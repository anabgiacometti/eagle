from django.db import models
from mongoengine import *

class Users(Document):
	username = StringField(max_length=200, required=True)
	password = StringField(max_length=200, required=True)
	is_active = BooleanField(default=True, required=True)
	is_admin = BooleanField(default=False, required=True)
	email = EmailField(max_length=200, required=True)
	permissions = ListField()
	full_name = StringField(max_length=500, required=True)

	# meta = {'db_alias': 'eagle', 'collection': 'users'}