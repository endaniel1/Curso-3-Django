from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin #Aqui importamos un mixis
from django.views import generic

"""Class for Home"""
#los Mixis siempre tiene q heredarce primero 
class Home(LoginRequiredMixin, generic.TemplateView):
	template_name = "bases/home.html" #indicamos aqui a template va a ir
	login_url = "bases:login" #Aqui le dicimos q el sino esta autenticado vaya a la vista del admin