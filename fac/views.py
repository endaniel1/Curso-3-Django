from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin #Aqui importamos un mixis
from django.views import generic #Para la manipulacion de diferentes tipos de vistas

from django.contrib.messages.views import SuccessMessageMixin # Para el mensaje success
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime

from django.contrib import messages

from django.contrib.auth import authenticate

from bases.views import SinPrivilegios

from .models import Cliente, FacturaEnc, FacturaDet
from .forms import ClienteForm
from inv.views import ProductoView
from inv.models import Producto

# Create your views here.

"""docstring for ClienteView"""
class ClienteView(SinPrivilegios, generic.ListView):
	model = Cliente
	template_name = "fac/cliente_list.html"
	context_object_name = "obj"
	permission_required = "fac.view_cliente"

"""docstring for ViewBaseCreate"""
class ViewBaseCreate(SuccessMessageMixin, SinPrivilegios, generic.CreateView):
	context_object_name ="obj"
	success_message = "Registro Agregado Correctamente!"

	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for ViewBaseEdit"""
class ViewBaseEdit(SuccessMessageMixin, SinPrivilegios, generic.UpdateView):
	context_object_name ="obj"
	success_message = "Registro Actualizado Correctamente!"

	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

"""docstring for ClienteCreate"""
class ClienteCreate(ViewBaseCreate):
	model = Cliente
	template_name = "fac/cliente_form.html"
	form_class = ClienteForm
	success_url = reverse_lazy("fac:cliente_list")
	permission_required = "fac.add_cliente"

"""docstring for ClienteUpdate"""
class ClienteUpdate(ViewBaseEdit):
	model = Cliente
	template_name = "fac/cliente_form.html"
	form_class = ClienteForm
	success_url = reverse_lazy("fac:cliente_list")
	permission_required = "fac.change_cliente"

@login_required(login_url = "/login/")
@permission_required("fac.change_cliente", login_url = "/login/")
def clienteDelete(request, id):
	cliente = Cliente.objects.filter(pk = id).first()

	if request.method == "POST":
		if cliente:			
			cliente.estado = not cliente.estado
			cliente.save()

			return HttpResponse("OK")
		else:
			return HttpResponse("FAIL")

	return HttpResponse("FAIL")


class FacturaView(SinPrivilegios, generic.ListView):
	model = FacturaEnc
	template_name = "fac/factura_list.html"
	context_object_name = "obj"
	permission_required = "fac.view_facturaenc"


@login_required(login_url = "/login/")
@permission_required("fac.change_facturaenc", login_url = "bases:sin_privilegios")
def facturas(request, id=None):
	template_name = "fac/facturas.html"

	detalle = {}
	clientes = Cliente.objects.filter(estado = True)

	if request.method == "GET":
		enc = FacturaEnc.objects.filter(pk=id).first()

		if not enc:
			encabezado = {
				"id" : 0,
				"fecha" : datetime.today(),
				"cliente" : 0,
				"sub_total" : 0.00,
				"total" : 0.00,
				"descuento": 0.00
			}

			detalle = None
		else:
			encabezado = {
				"id" : enc.id,
				"fecha" : enc.fecha,
				"cliente" : enc.cliente,
				"sub_total" : enc.sub_total,
				"total" : enc.total,
				"descuento": enc.descuento
			}

			detalle = FacturaDet.objects.filter(factura=enc)

		contexto = {
			"enc" : encabezado,
			"obj" : detalle,
			"clientes" : clientes
		}

	if request.method == "POST":
		cliente = request.POST.get("enc_cliente")
		fecha = request.POST.get("fecha")
		cli = Cliente.objects.get(pk=cliente)

		if not id:
			print("No existe id va a creat nuevo")
			print(cli)
			enc = FacturaEnc(
				cliente=cli,
				fecha=fecha,
			)
			print(enc)

			if enc:
				enc.save()
				id = enc.id
		elif id:			
			print("si existe va A filtrar")
			enc = FacturaEnc.objects.filter(pk = id).first()
			if enc:
				enc.cliente = cli
				enc.save()
		else:			
			print("No Tiene nada")
			messages.error(request, "No Se pudo Detectar el Nùmero de la Factura")
			return redirect("fac:factura_list")

		codigo = request.POST.get("codigo")
		cantidad = request.POST.get("cantidad")
		precio = request.POST.get("precio")
		sub_total = request.POST.get("sub_total_detalle")
		descuento = request.POST.get("descuento_detalle")
		total = request.POST.get("total_detalle")
		
		producto = Producto.objects.get(codigo=codigo)
		detalle = FacturaDet(
			factura = enc,
			producto = producto,
			cantidad = cantidad,
			precio = precio,
			sub_total = sub_total,
			descuento = descuento,
			total = total
		)

		if detalle:
			detalle.save()
			print("guardado con FacEnc")
			

		return redirect("fac:factura_edit", id = id)
	
	return render(request, template_name, contexto)


class FacProductoView(ProductoView):
	template_name = "fac/buscar_producto.html"

def borrarDetalleFactura(request, id = None):
	template_name = "fac/facturas_borrar_detalle.html"

	det = FacturaDet.objects.get(pk = id)

	if request.method == "GET":
		contexto = {
			"id" : id,
			"det" : det
		}
	if request.method == "POST":
		user = request.POST.get("usuario")
		pas = request.POST.get("password")

		usuario = authenticate(username = user, password = pas)
		if not usuario:
			return HttpResponse("Usuario o Clave Incorrecta!")

		if not usuario.is_active:
			return HttpResponse("Usuario Inactivo!")

		if usuario.is_superuser or usuario.has_perm("fac.sup_caja_facturadet"):
			det.id = None
			det.cantidad = (-1 * det.cantidad)
			det.sub_total = (-1 * det.sub_total)
			det.total = (-1 * det.total)
			det.descuento = (-1 * det.descuento)
			det.save()

			return HttpResponse("OK")

		return HttpResponse("Usuario No Autorizado!")

	return render(request,template_name,contexto)