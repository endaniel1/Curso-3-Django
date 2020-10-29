from django.db import models
from bases.models import ClassModelo

# Create your models here.

"""docstring for Categorias"""
class Categoria(ClassModelo):
	descripcion = models.CharField(
		max_length = 100,
		help_text = 'Descripcion de la Categoria',
		unique = True
	)

	def __str__(self):
		return "{}".format(self.descripcion)

	def save(self):
		self.descripcion = self.descripcion.upper()
		super(Categoria, self).save()

	class Meta:
		verbose_name_plural = 'Categorias'
