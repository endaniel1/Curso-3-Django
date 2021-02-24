#Importamos el archivo para el manejo de la Api A consumir nuestra aplicacion o app
from rest_framework import serializers

from inv.models import Producto

"""docstring for ProductoSerializer"""
class ProductoSerializer(serializers.ModelSerializer):
	
	class Meta:
		model = Producto
		fields = "__all__"