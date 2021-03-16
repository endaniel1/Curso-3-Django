from django.contrib import admin
from .models import *

# Register your models here.

class ProveedorAdmin(admin.ModelAdmin):
	pass

class CompraEncAdmin(admin.ModelAdmin):
	pass

class CompraDetAdmin(admin.ModelAdmin):
	pass


admin.site.register(Proveedor, ProveedorAdmin)
admin.site.register(CompraEnc, CompraEncAdmin)
admin.site.register(CompraDet, CompraDetAdmin)