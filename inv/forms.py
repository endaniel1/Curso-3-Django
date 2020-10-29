from django import forms #clase para la creacion de formularios

from .models import Categoria #clase del modelo a utilizar

"""docstring for CategoriaForm"""
class CategoriaForm(forms.ModelForm):
	#aqui para modificar las propiedades
	class Meta:
		model = Categoria #decimos q modelo va utilizar
		fields =["descripcion", "estado"] #le cuales es el texto y nombre de lo campos
		labels = { #decimos q label va a utilizar cada uno aqui
			"descripcion" : "Descripcion de la categoria",
			"estado" : "Estado"
		}
		widget = { #aqui decimos q tipo de input va a ser
			"descripcion" : forms.TextInput
		}

		#Aqui al inicializar le decimos q datos vamos a cambiar
		def __init__(self, *args, **kwargs):
		    super().__init__(*args, **kwargs)

		    #En este caso iteramos cada elemento para actualizar en este caso la class de cada input
		    for field in self.fields:
		    	self.fields[field].widget.attrs.update({
		    		"class" : "form-control"
		    	})