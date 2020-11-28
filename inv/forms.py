from django import forms #clase para la creacion de formularios

from .models import Categoria, SubCategoria, Marca, UnidadMedida, Producto #clase del modelo a utilizar

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
			"descripcion" : forms.TextInput()
		}

		#Aqui al inicializar le decimos q datos vamos a cambiar
		def __init__(self, *args, **kwargs):
		    super().__init__(*args, **kwargs)

		    #En este caso iteramos cada elemento para actualizar en este caso la class de cada input
		    for field in self.fields:
		    	self.fields[field].widget.attrs.update({
		    		"class" : "form-control"
		    	})

"""docstring for SubCategoriaForm"""
class SubCategoriaForm(forms.ModelForm):
	categoria = forms.ModelChoiceField(
		queryset = Categoria.objects.filter(estado=True).order_by("descripcion")
	)
	#aqui para modificar las propiedades
	class Meta:
		model = SubCategoria #decimos q modelo va utilizar
		fields = ["categoria","descripcion", "estado"] #le cuales es el texto y nombre de lo campos
		labels = { #decimos q label va a utilizar cada uno aqui
			"descripcion" : "Sub Categorias",
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
		    self.fields["categoria"].empty_label = "Selecione Categoria"

"""docstring for MarcaForm"""
class MarcaForm(forms.ModelForm):
	#aqui para modificar las propiedades
	class Meta:
		model = Marca
		fields = ["descripcion", "estado"] #le cuales es el texto y nombre de lo campos
		labels = { #decimos q label va a utilizar cada uno aqui
			"descripcion" : "Descripcion de Marca",
			"estado" : "Estado"
		}
		widget = { #aqui decimos q tipo de input va a ser
			"descripcion" : forms.TextInput()
		}
	#Aqui al inicializar le decimos q datos vamos a cambiar
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		#En este caso iteramos cada elemento para actualizar en este caso la class de cada input
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				"class" : "form-control"
			})

"""docstring for UMForm"""
class UMForm(forms.ModelForm):
	#aqui para modificar las propiedades
	class Meta:
		model = UnidadMedida
		fields = ["descripcion", "estado"] #le cuales es el texto y nombre de lo campos
		labels = { #decimos q label va a utilizar cada uno aqui
			"descripcion" : "Descripcion de Marca",
			"estado" : "Estado"
		}
		widget = { #aqui decimos q tipo de input va a ser
			"descripcion" : forms.TextInput()
		}
	#Aqui al inicializar le decimos q datos vamos a cambiar
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		#En este caso iteramos cada elemento para actualizar en este caso la class de cada input
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				"class" : "form-control"
			})

"""docstring for ProductoForm"""
class ProductoForm(forms.ModelForm):
	class Meta:
		model = Producto
		fields = [
			"codigo",
			"codigo_barra",
			"descripcion", 
			"estado",
			"precio",
			"existencia", 
			"ultima_compra", 
			"marca", 
			"sub_categoria", 
			"unidad_medida"
		]
		exclude = ["um", "fm", "uc", "fc"] #Aqui excluimos algunos campos de no queremos q muestre
		widget = { #aqui decimos q tipo de input va a ser
			"descripcion" : forms.TextInput()
		}
		
	#Aqui al inicializar le decimos q datos vamos a cambiar
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		#En este caso iteramos cada elemento para actualizar en este caso la class de cada input
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				"class" : "form-control"
			})
		self.fields["ultima_compra"].widget.attrs["readonly"] = True
		self.fields["existencia"].widget.attrs["readonly"] = True