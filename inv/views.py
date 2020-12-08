from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin #Aqui importamos un mixis
from django.views import generic #Para la manipulacion de diferentes tipos de vistas
from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto

from django.urls import reverse_lazy #Clase para manitpulacion de url

from .forms import CategoriaForm, SubCategoriaForm, MarcaForm, UMForm, ProductoForm #Clase form a utilizar

#Modulos para la utilizar y crear mensajes para enviarselo a las vistas desde django
from django.contrib import messages #para los mensajes de las vistas basada en funciones
from django.contrib.messages.views import SuccessMessageMixin #para los mensajes de vistas basada en clases

from bases.views import SinPrivilegios

"""docstring for CategoriaView"""
class CategoriaView(LoginRequiredMixin, PermissionRequiredMixin, generic.ListView):
	permission_required = "inv.view_categoria"
	model = Categoria
	template_name = "inv/categoria_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for CategoriaCreate"""
class CategoriaCreate(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
	model = Categoria
	template_name = "inv/categoria_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = CategoriaForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:categoria_list") #Y cuando sea success a q url va
	success_message = "Categoria Creada con Existo" # Para el mixins de los mensaje(clases basada en vista)

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for CategoriaUpdateView"""
class CategoriaUpdateView(SuccessMessageMixin, LoginRequiredMixin, generic.UpdateView):
	model = Categoria
	template_name = "inv/categoria_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = CategoriaForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:categoria_list") #Y cuando sea success a q url va
	success_message = "Categoria Actualizada" # Para el mixins de los mensaje(clases basada en vista)

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

"""docstring for CategoriaDeleteView"""
class CategoriaDeleteView(LoginRequiredMixin, generic.DeleteView):
	model = Categoria
	template_name = "inv/catalogos_Del.html"
	context_object_name = "obj"
	login_url = "bases:login"
	success_url = reverse_lazy("inv:categoria_list")

"""docstring for SubCategoriaView"""
class SubCategoriaView(LoginRequiredMixin, SinPrivilegios, generic.ListView):
	permission_required = "inv.view_subcategoria"
	model = SubCategoria
	template_name = "inv/subcategoria_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for SubCategoriaCreate"""
class SubCategoriaCreate(LoginRequiredMixin, PermissionRequiredMixin, generic.CreateView):
	permission_required = "inv.view_subcategoria"
	model = SubCategoria
	template_name = "inv/subcategoria_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = SubCategoriaForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:subcategoria_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for SubCategoriaUpdateView"""
class SubCategoriaUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = SubCategoria
	template_name = "inv/subcategoria_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = SubCategoriaForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:subcategoria_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

"""docstring for SubCategoriaDeleteView"""
class SubCategoriaDeleteView(LoginRequiredMixin, generic.DeleteView):
	model = SubCategoria
	template_name = "inv/catalogos_Del.html"
	context_object_name = "obj"
	login_url = "bases:login"
	success_url = reverse_lazy("inv:subcategoria_list")

"""docstring for MarcaView"""
class MarcaView(LoginRequiredMixin, SinPrivilegios, generic.ListView):
	permission_required = "inv.view_marca" #este metodo aqui q colocarlo porque lo tiene heredado de la class SinPrivilegios
	model = Marca
	template_name = "inv/marcas_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for MarcaCreate"""
class MarcaCreate(LoginRequiredMixin, generic.CreateView):
	model = Marca
	template_name = "inv/marca_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = MarcaForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:marca_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for MarcaUpdateView"""
class MarcaUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = Marca
	template_name = "inv/marca_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = MarcaForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:marca_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

def marca_inactivar(request, id):
	marca = Marca.objects.filter(pk=id).first()
	contexto = {}
	template_name = "inv/catalogos_Del.html"

	if not marca:

		return redirect("inv:marca_list")

	elif request.method == "GET":
		contexto = {"obj":marca}

	elif request.method == "POST":
		marca.estado =  False
		marca.save()
		messages.warning(request, "Marca Inactivada")
		return redirect("inv:marca_list")

	return render(request,template_name,contexto)

"""docstring for UMView"""
class UMView(LoginRequiredMixin, generic.ListView):
	model = UnidadMedida
	template_name = "inv/um_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for UMCreate"""
class UMCreate(LoginRequiredMixin, generic.CreateView):
	model = UnidadMedida
	template_name = "inv/um_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = UMForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:um_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for UMUpdateView"""
class UMUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = UnidadMedida
	template_name = "inv/um_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = UMForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:um_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

def um_inactivar(request, id):
	um = UnidadMedida.objects.filter(pk=id).first()
	contexto = {}
	template_name = "inv/catalogos_Del.html"

	if not um:

		return redirect("inv:um_list")

	elif request.method == "GET":
		contexto = {"obj":um}

	elif request.method == "POST":
		um.estado =  False
		um.save()
		return redirect("inv:um_list")

	return render(request,template_name,contexto)

"""docstring for Producto"""
class ProductoView(LoginRequiredMixin, generic.ListView):
	model = Producto
	template_name = "inv/producto_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for ProductoCreate"""
class ProductoCreate(LoginRequiredMixin, generic.CreateView):
	model = Producto
	template_name = "inv/producto_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = ProductoForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:producto_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)

"""docstring for ProductoUpdateView"""
class ProductoUpdateView(LoginRequiredMixin, generic.UpdateView):
	model = Producto
	template_name = "inv/producto_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = ProductoForm #Aqui le indicamos a q formulario va
	success_url = reverse_lazy("inv:producto_list") #Y cuando sea success a q url va

	#Reescribo el metodo de validacion
	def form_valid(self, form):
		form.instance.um = self.request.user.id
		return super().form_valid(form)

def producto_inactivar(request, id):
	producto = Producto.objects.filter(pk=id).first()
	contexto = {}
	template_name = "inv/catalogos_Del.html"

	if not producto:

		return redirect("inv:producto_list")

	elif request.method == "GET":
		contexto = {"obj":producto}

	elif request.method == "POST":
		producto.estado =  False
		producto.save()
		return redirect("inv:producto_list")

	return render(request,template_name,contexto)