from django.contrib import admin
from .models import *

# Register your models here.

class ClienteAdmin(admin.ModelAdmin):
	pass

class FacturaEncAdmin(admin.ModelAdmin):
	pass

class FacturaDetAdmin(admin.ModelAdmin):
	pass


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(FacturaEnc, FacturaEncAdmin)
admin.site.register(FacturaDet, FacturaDetAdmin)
