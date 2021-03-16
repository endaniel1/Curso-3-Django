from django.db import models
from bases.models import ClassModelo, ClassModelo2
from inv.models import Producto

#Para Utilizacion de Signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

# Create your models here.

"""docstring for Cliente"""
class Cliente(ClassModelo):
	NAT = "Natural"
	JUR = "Juridica"
	TIPO_CLIENTE = [
		(NAT, "Natural"),
		(JUR, "Juridica"),
	]
	nombres = models.CharField(max_length = 100)
	apellidos = models.CharField(max_length = 100)
	telefono = models.CharField(
		max_length = 20, 
		null=True,
		blank=True
	)
	tipo = models.CharField(
		max_length = 10,
		choices = TIPO_CLIENTE,
		default = NAT
	)

	def __str__(self):
		return "{} {}".format(self.apellidos, self.nombres)

	def save(self):
		self.nombres = self.nombres.upper()
		self.apellidos = self.apellidos.upper()
		super(Cliente, self).save()

	class Meta:
		verbose_name = 'Clientes'

class FacturaEnc(ClassModelo2):
	cliente = models.ForeignKey(Cliente, on_delete = models.CASCADE)
	fecha = models.DateTimeField(auto_now_add = True)
	sub_total = models.FloatField(default = 0)
	descuento = models.FloatField(default = 0)
	total = models.FloatField(default = 0)

	def __str__(self):
		return "{}".format(self.id)

	def save(self):
		self.total = self.sub_total - self.descuento
		super(FacturaEnc, self).save()

	class Meta:
		verbose_name_plural = "Encabezado de Facturas"
		verbose_name = "Encabezado Factura"
		permissions = [
			("sup_caja_facturaenc", "Permisos de Supervisor de Caja Encabezado")
		]

class FacturaDet(ClassModelo2):
	factura = models.ForeignKey(FacturaEnc, on_delete = models.CASCADE)
	producto = models.ForeignKey(Producto, on_delete = models.CASCADE)
	cantidad = models.BigIntegerField(default = 0)
	precio = models.FloatField(default = 0)
	sub_total = models.FloatField(default = 0)
	descuento = models.FloatField(default = 0)
	total = models.FloatField(default = 0)

	def __str__(self):
		return "{}".format(self.producto)

	def save(self):
		self.sub_total = float(float(int(self.cantidad)) * float(self.precio))
		self.total = self.sub_total - float(self.descuento)
		super(FacturaDet, self).save()

	class Meta:
		verbose_name_plural = "Detalles de Facturas"
		verbose_name = "Detalle Factura"
		permissions = [
			("sup_caja_facturadet", "Permisos de Supervisor de Caja Detalle")
		]

@receiver(post_save, sender = FacturaDet)
def detalleFacSave(sender, instance, **kwargs):
	factura_id = instance.factura.id
	producto_id = instance.producto.id

	encabezado = FacturaEnc.objects.get(pk = factura_id)

	if encabezado:
		sub_total = FacturaDet.objects.filter(factura = factura_id).aggregate(sub_total = Sum("sub_total")).get("sub_total", 0.00)

		descuento = FacturaDet.objects.filter(factura = factura_id).aggregate(sub_total = Sum("descuento")).get("descuento", 0.00)

		encabezado.sub_total = sub_total
		encabezado.descuento = descuento
		encabezado.save()

	prod = Producto.objects.filter(pk = producto_id).first()
	if prod:
		cantidad = int(prod.existencia) - int(instance.cantidad)
		prod.existencia = cantidad
		prod.save()