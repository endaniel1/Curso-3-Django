from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin #Aqui importamos un mixis
from django.views import generic #Para la manipulacion de diferentes tipos de vistas

from django.contrib.messages.views import SuccessMessageMixin # Para el mensaje success
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, permission_required
from django.http import HttpResponse
from datetime import datetime

from bases.views import SinPrivilegios

from .models import Cliente, FacturaEnc, FacturaDet
from .forms import ClienteForm
from inv.views import ProductoView

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
	encabezado = {
		"fecha" : datetime.today()
	}
	detalle = {}
	clientes = Cliente.objects.filter(estado = True)
	contexto = {
		"enc" : encabezado,
		"det" : detalle,
		"clientes" : clientes
	}
	return render(request, template_name, contexto)


class FacProductoView(ProductoView):
	template_name = "fac/buscar_producto.html"
