from django.db import models

from bases.models import ClassModelo

from inv.models import Producto

#Para Utilizacion de Signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

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

"""docstring for CompraEnc"""
class CompraEnc(ClassModelo):
	fecha_compra = models.DateField(null = True, blank = True)
	observacion = models.TextField(null =  True, blank = True)
	no_factura = models.CharField(max_length = 100)
	fecha_factura = models.DateField()
	sub_total = models.FloatField(default = 0)
	descuento = models.FloatField(default = 0)
	total = models.FloatField(default = 0)

	proveedor = models.ForeignKey(Proveedor, on_delete = models.CASCADE)

	def __str__(self):
		return "{}".format(self.observacion)

	def save(self):
		self.observacion = self.observacion.upper()
		self.total = self.sub_total + self.descuento
		super(CompraEnc, self).save()

	class Meta:
		verbose_name_plural = "Encabezado de las Compras"
		verbose_name = "Encabezado de Compra"

"""docstring for CompraDet"""
class CompraDet(ClassModelo):
	compra = models.ForeignKey(CompraEnc, on_delete = models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
	cantidad = models.BigIntegerField(default = 0)
	precio_prv = models.FloatField(default = 0)
	sub_total = models.FloatField(default = 0)
	descuento = models.FloatField(default = 0)
	total = models.FloatField(default = 0)
	costo = models.FloatField(default = 0)

	def __str__(self):
		return "{}".format(self.producto)

	def save(self):
		self.sub_total = float(float(int(self.cantidad)) * float(self.precio_prv))
		self.total = self.sub_total - float(self.descuento)
		super(CompraDet, self).save()

	class Meta:
		verbose_name_plural = "Detalles de las Compras"
		verbose_name = "Detalle Compra"


@receiver(post_delete, sender= CompraDet)
def detalleCompraDel(sender, instance, **kwargs):
	id_producto = instance.producto.id
	id_compra = instance.compra.id

	enc = CompraEnc.objects.filter(pk = id_compra).first()

	if enc:
		sub_total = CompraDet.objects.filter(compra = id_compra).aggregate(Sum("sub_total"))
		descuento = CompraDet.objects.filter(compra = id_compra).aggregate(Sum("descuento"))
		enc.sub_total = sub_total["sub_total__sum"] #Aqui ay q hacer un operador ternario porque cuando se None da un errorr
		enc.descuento = descuento["descuento__sum"] #Aqui ay q hacer un operador ternario porque cuando se None da un errorr

		enc.save()

	prod = Producto.objects.filter(pk = id_producto).first()
	if prod:
		cantidad = int(prod.existencia) - int(instance.cantidad)
		prod.existencia = cantidad
		prod.save()


@receiver(post_save, sender = CompraDet)
def detalleCompraSave(sender, instance, **kwargs):
	id_producto = instance.producto.id
	fecha_compra = instance.compra.fecha_compra

	prod = Producto.objects.filter(pk = id_producto).first()
	if prod:
		cantidad = int(prod.existencia) + int(instance.cantidad)
		prod.existencia = cantidad
		prod.ultima_compra = fecha_compra
		prod.save()