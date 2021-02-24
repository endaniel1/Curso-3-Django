from django.shortcuts import render

#Para el manejo de la api a utilizar de rest framework
from rest_framework.views import APIView #Para la utilizacion y manejo de vista
from rest_framework.response import Response #Para la utilizacion y respuesta

from django.shortcuts import get_object_or_404 #Para cuando de un error mandar un 404
from .serializers import ProductoSerializer #Para usar para la serializacion
from inv.models import Producto

from django.db.models import Q #Para hacer dos condicional a un objeto de una variable a pasar

# Create your views here.

"""docstring for ProductoList"""
class ProductoList(APIView):
	#Sobreescribimos el metodo Get de Nuestra clases APIView
	def get(self, request):
		prod = Producto.objects.all()
		#Serializamos los datos q bien y lo cargamos en formato de un Json con la clase data
		data = ProductoSerializer(prod, many = True).data

		return Response(data) #retornamos los datos a nuestra vista 


"""docstring for ProductoDetalle"""
class ProductoDetalle(APIView):
	def get(self, request, codigo):
		#comprobamos con la clase Q si coincide dos valores
		#con get_object_or_404() vemos si el resultado da un error para mandar un 404
		prod = get_object_or_404(Producto, Q(codigo = codigo)|Q(codigo_barra = codigo))
		data = ProductoSerializer(prod).data

		return Response(data) #retornamos los datos a nuestra vista 