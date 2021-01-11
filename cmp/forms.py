from django import forms

from .models import Proveedor, CompraEnc

"""docstring for ProveedorForm"""
class ProveedorForm(forms.ModelForm):
	email = forms.EmailField(max_length=254)

	class Meta:
		model = Proveedor
		exclude = ["um", "fm", "uc", "fc"]
		widget = {
			"descripcion" : forms.TextInput()
		}
		
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				"class" : "form-control"
			})

"""docstring for CompraEncForm"""
class CompraEncForm(forms.ModelForm):
	fecha_compra = forms.DateInput()
	fecha_factura = forms.DateInput()

	class Meta:
		model = CompraEnc
		fields = [
			"proveedor", "fecha_compra", "observacion",
			"no_factura", "fecha_factura", "sub_total",
			"descuento", "total"
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				"class" : "form-control"
			})

		self.fields["fecha_compra"].widget.attrs["readonly"] = True
		self.fields["fecha_factura"].widget.attrs["readonly"] = True
		self.fields["sub_total"].widget.attrs["readonly"] = True
		self.fields["descuento"].widget.attrs["readonly"] = True
		self.fields["total"].widget.attrs["readonly"] = True