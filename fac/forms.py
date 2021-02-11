from django import forms

from .models import Cliente

"""docstring for ClienteForm"""
class ClienteForm(forms.ModelForm):
	class Meta:
		model = Cliente
		fields = [
			"nombres", "apellidos", "tipo", "telefono", "estado"
		]
		exclude = [
			"um", "fm", "uc", "fc"
		]

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		for field in self.fields:
			self.fields[field].widget.attrs.update({
				"class" : "form-control"
			})