from django import forms

from .models import Proveedor

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