from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin #Aqui importamos un mixis
from django.views import generic #Para la manipulacion de diferentes tipos de vistas

from django.urls import reverse_lazy #Clase para manitpulacion de url

from django.contrib.auth.decorators import login_required, permission_required

from .models import Proveedor, CompraEnc, CompraDet
from .forms import ProveedorForm, CompraEncForm

from bases.views import SinPrivilegios

from inv.models import Producto

from django.http import HttpResponse, JsonResponse
import json
import datetime
from django.db.models import Sum

"""docstring for MixinFormInvalid"""
class MixinFormInvalid:
	def form_invalid(self, form):
		response = super().form_invalid(form)
		if self.request.is_ajax():
			return JsonResponse(form.errors, status=400)
		else:
			return response


"""docstring for ProveedorView"""
class ProveedorView(LoginRequiredMixin, generic.ListView):
	model = Proveedor
	template_name = "cmp/proveedor_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for ProveedorCreate"""
class ProveedorCreate(LoginRequiredMixin, MixinFormInvalid, generic.CreateView):
	model = Proveedor
	template_name = "cmp/proveedor_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = ProveedorForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("cmp:proveedor_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for ProveedorUpdateView"""
class ProveedorUpdateView(LoginRequiredMixin, MixinFormInvalid, generic.UpdateView):
	model = Proveedor
	template_name = "cmp/proveedor_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = ProveedorForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("cmp:proveedor_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

def proveedorDeleteView(request, id):
	template_name = "cmp/inactivar_prv.html"
	contexto = {}
	prv = Proveedor.objects.filter(pk=id).first()

	if not prv:
		return HttpResponse("Proveedor no Existe " + str(id))
	
	if request.method == "GET":
		contexto = {"obj" : prv}

	if request.method == "POST":
		prv.estado = False
		prv.save()
		contexto = {"obj" : "OK"}
		return HttpResponse("Proveedor Inactivado")

	return render(request, template_name, contexto)

"""docstring for ComprasView"""
class ComprasView(SinPrivilegios, generic.ListView):
	permission_required = "cmp.view_comprasenc"
	model = CompraEnc
	template_name = "cmp/compras_list.html"
	context_object_name = "obj"

@login_required(login_url = "login")
@permission_required("cmp.view_comprasenc", login_url = "bases:sinprivilegios")
def CreateCompra(request, id = None):
	template_name = "cmp/compras.html"
	productos = Producto.objects.filter(estado = True)
	form_compras = {}
	contexto = {}

	if request.method == "GET":
		form_compras = CompraEncForm()
		compraEnc = CompraEnc.objects.filter(pk = id).first()

		if compraEnc:
			compraDet = CompraDet.objects.filter(compra = compraEnc)
			fecha_compra = datetime.date.isoformat(compraEnc.fecha_compra)
			fecha_factura = datetime.date.isoformat(compraEnc.fecha_factura)

			datos = {
				"proveedor" : compraEnc.proveedor,
				"fecha_compra" : fecha_compra,
				"fecha_factura" : fecha_factura,
				"observacion" : compraEnc.observacion,
				"no_factura" : compraEnc.no_factura,
				"sub_total" : compraEnc.sub_total,
				"descuento" : compraEnc.descuento,
				"total" : compraEnc.total,
			}
			form_compras = CompraEncForm(datos)

		else:
			compraDet = None

		contexto = {
			"productos" : productos,
			"compraEnc" : compraEnc,
			"CompraDet" : compraDet,
			"form_compras" : form_compras
		}

	if request.method == "POST":
		fecha_compra = request.POST.get("fecha_compra");
		observacion = request.POST.get("observacion");
		no_factura = request.POST.get("no_factura");
		fecha_factura = request.POST.get("fecha_factura");
		proveedor = request.POST.get("proveedor");
		sub_total = 0
		descuento = 0
		total = 0

		if not id: 
			proveedor = Proveedor.objects.get(pk=proveedor);

			enc = CompraEnc(
				fecha_compra = fecha_compra,
				observacion = observacion,
				no_factura = no_factura,
				fecha_factura = fecha_factura,
				proveedor = proveedor,
				uc = request.user,
			)

			if enc:
				enc.save()
				id = enc.id
		else: 
			enc = CompraEnc.objects.filter(pk=id).first()

			if enc:
				enc.fecha_compra = fecha_compra
				enc.observacion = observacion
				enc.no_factura = no_factura
				enc.fecha_factura = fecha_factura
				enc.um = request.user.id
				enc.save()

		if not id:
			return redirect("cmp:compras_list")

		producto = request.POST.get("id_producto")
		cantidad = request.POST.get("id_cantidad_detalle")
		precio = request.POST.get("id_precio_detalle")
		sub_total_detalle = request.POST.get("id_sub_total_detalle")
		descuento_detalle = request.POST.get("id_descuento_detalle")
		total_detalle = request.POST.get("id_total_detalle")
		
		prod = Producto.objects.get(pk=producto)

		det = CompraDet(
			compra = enc,
			producto = prod,
			cantidad = cantidad,
			precio_prv = precio,
			descuento = descuento_detalle,
			costo = 0,
			uc = request.user
		)

		if det:
			det.save()

			sub_total = CompraDet.objects.filter(compra = id).aggregate(Sum("sub_total"))
			descuento = CompraDet.objects.filter(compra = id).aggregate(Sum("descuento"))

			enc.sub_total = sub_total["sub_total__sum"]
			enc.descuento = descuento["descuento__sum"]
			enc.save()

		return redirect("cmp:compras_edit", id = id)

	return render(request, template_name, contexto)


"""docstring for CompraDetDelete"""
class CompraDetDelete(SinPrivilegios, generic.DeleteView):
	permission_required = "cmp.delete_comprasdet"
	model = CompraDet
	template_name = "cmp/compras_det_del.html"
	context_object_name = "obj"

	def get_success_url(self):
		compra_id = self.kwargs["compra_id"]
		return reverse_lazy("cmp:compras_edit", kwargs = {
			"id" : compra_id
		})