from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin #Aqui importamos un mixis
from django.views import generic

"""Class for SinPrivilegios"""
class SinPrivilegios(LoginRequiredMixin, PermissionRequiredMixin):
	login_url = "bases:login"
	raise_exception =  False #Estao para q no se ponga la pantalla en blanco o no marque el error
	redirect_field_name = "redirecto_to" #aqui para qu acepte redireciones

	#aqui sobreescribomos el metodo q hace para cuando no tiene permiso el usuario
	def handle_no_permission(self):
		from django.contrib.auth.models import AnonymousUser #aqui para saber cual es user autenticado
		
		if not self.request.user == AnonymousUser():
			self.login_url = "bases:sin_privilegios" #sobreescribimos, para donde vamos a ir 
		
		#Despues se hace una redireccion para donde se va a ir
		return HttpResponseRedirect(reverse_lazy(self.login_url))

#los Mixis siempre tiene q heredarce primero 
"""Class for Home"""
class Home(LoginRequiredMixin, generic.TemplateView):
	template_name = "bases/home.html" #indicamos aqui a template va a ir
	login_url = "bases:login" #Aqui le dicimos q el sino esta autenticado vaya a la vista del admin

"""docstring for HomeSinPrivilegios"""
class HomeSinPrivilegios(generic.TemplateView):
	template_name = "bases/sin_privilegios.html"