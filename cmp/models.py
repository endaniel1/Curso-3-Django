from django.db import models

from bases.models import ClassModelo
# Create your models here.

"""docstring for Proveedor"""
class Proveedor(ClassModelo):
	descripcion = models.CharField(
		max_length=100,
		unique=True
	)
	direccion = models.CharField(
		max_length=250,
		null=True,
		blank=True
	)
	contacto = models.CharField(
		max_length=10,
	)
	telefono = models.CharField(
		max_length=10,
		null=True,
		blank=True
	)
	email =  models.EmailField(
		null=True,
		blank=True
	)

	def __str__(self):
		return "{}".format(self.descripcion)

	def save(self):
		self.descripcion = self.descripcion.upper()
		super(Proveedor, self).save()

	class Meta:
		verbose_name='Proveedores'