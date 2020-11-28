from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin #Aqui importamos un mixis
from django.views import generic #Para la manipulacion de diferentes tipos de vistas

from django.urls import reverse_lazy #Clase para manitpulacion de url

from .models import Proveedor
from .forms import ProveedorForm

from django.http import HttpResponse
import json

"""docstring for ProveedorView"""
class ProveedorView(LoginRequiredMixin, generic.ListView):
	model = Proveedor
	template_name = "cmp/proveedor_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for ProveedorCreate"""
class ProveedorCreate(LoginRequiredMixin, generic.CreateView):
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
class ProveedorUpdateView(LoginRequiredMixin, generic.UpdateView):
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
