from django.db import models
from bases.models import ClassModelo

"""docstring for Categoria"""
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

"""docstring for SubCategoria"""
class SubCategoria(ClassModelo):
	categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
	descripcion = models.CharField(
		max_length = 100,
		help_text = "Descripcion de la Categoria"
	)

	def __str__(self):
		return "{} : {}".format(self.categoria.descripcion, self.descripcion)

	def save(self):
		self.descripcion = self.descripcion.upper()
		super(SubCategoria, self).save()

	class Meta:
		verbose_name_plural = 'Categorias'
		unique_together = ("categoria", "descripcion")#Aqui creamos un unique compuesto

"""docstring for Marca"""
class Marca(ClassModelo):
	descripcion = models.CharField(
		max_length = 255,
		help_text = "Descripcion de Marca",
		unique = True
	)

	def __str__(self):
		return "{}".format(self.descripcion)

	def save(self):
		self.descripcion = self.descripcion.upper()
		super(Marca, self).save()
		
	class Meta:
		verbose_name_plural = "Marca"

"""docstring for UnidadMedida"""
class UnidadMedida(ClassModelo):
	descripcion = models.CharField(
		max_length = 100,
		help_text = "Descripcion de Unidad Medida",
		unique = True
	)

	def __str__(self):
		return "{}".format(self.descripcion)

	def save(self):
		self.descripcion = self.descripcion.upper()
		super(UnidadMedida, self).save()
		
	class Meta:
		verbose_name_plural = "Unidades de Medidas"

"""docstring for Producto"""
class Producto(ClassModelo):
	codigo = models.CharField(
		max_length = 20,
		unique = True
	)
	codigo_barra = models.CharField(max_length =  50)
	descripcion = models.CharField(max_length = 200)
	precio = models.FloatField(default = 0)
	existencia = models.IntegerField(default = 0)
	ultima_compra = models.DateField(null = True, blank = True)

	marca = models.ForeignKey(Marca, on_delete= models.CASCADE)
	unidad_medida = models.ForeignKey(UnidadMedida, on_delete = models.CASCADE)
	categoria = models.ForeignKey(Categoria, on_delete = models.CASCADE)
	sub_categoria = models.ForeignKey(SubCategoria, on_delete = models.CASCADE)

	def __str__(self):
		return "{}".format(self.descripcion)

	def save(self):
		self.descripcion = self.descripcion.upper()
		super(Producto, self).save()
		
	class Meta:
		verbose_name_plural = "Productos"
		unique_together = ("codigo", "codigo_barra")