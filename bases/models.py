from django.db import models
from django.contrib.auth.models import User

from django_userforeignkey.models.fields import UserForeignKey
# Create your models here.

"""docstring for ClassModelo"""
class ClassModelo(models.Model):

	estado = models.BooleanField(default = True)
	fc = models.DateTimeField(auto_now_add = True) #Se coloca una unica vez con auto_now_add
	fm = models.DateTimeField(auto_now = True) #Se coloa siempre y cuanda se modifique con auto_now
	uc = models.ForeignKey(User, on_delete = models.CASCADE) #para la relacion de uno a muchos
	um = models.IntegerField(blank = True, null = True)

	class Meta:
		abstract = True #Aqui le decimos a django q no lo tome en cuenta al momento de hacer la migraciones

"""docstring for ClassModelo2"""
class ClassModelo2(models.Model):

	estado = models.BooleanField(default = True)
	fc = models.DateTimeField(auto_now_add = True) #Se coloca una unica vez con auto_now_add
	fm = models.DateTimeField(auto_now = True) #Se coloa siempre y cuanda se modifique con auto_now
	# uc = models.ForeignKey(User, on_delete = models.CASCADE) 
	# um = models.IntegerField(blank = True, null = True)
	uc = UserForeignKey(auto_user_add =  True, related_name = '+') 
	um = UserForeignKey(auto_user =  True, related_name = '+') 

	class Meta:
		abstract = True #Aqui le decimos a django q no lo tome en cuenta al momento de hacer la migraciones

