from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin #Aqui importamos un mixis
from django.views import generic
from .models import Categoria

from django.urls import reverse_lazy

from .forms import CategoriaForm

"""docstring for CategoriaView"""
class CategoriaView(LoginRequiredMixin, generic.ListView):
	model = Categoria
	template_name = "inv/categoria_list.html"
	context_object_name = "obj"
	login_url = "bases:login"

"""docstring for CategoriaCreate"""
class CategoriaCreate(LoginRequiredMixin, generic.CreateView):
	model = Categoria
	template_name = "inv/categoria_form.html"
	context_object_name = "obj"
	login_url = "bases:login"
	form_class = CategoriaForm
	success_url = reverse_lazy("inv:categoria_list")

	def form_valid(self, form):
		form.instance.uc = self.request.user
		return super().form_valid(form)