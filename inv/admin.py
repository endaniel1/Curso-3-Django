from django.contrib import admin
from .models import *
# Register your models here.

class CategoriaAdmin(admin.ModelAdmin):
	pass

class SubCategoriaAdmin(admin.ModelAdmin):
	pass

class MarcaAdmin(admin.ModelAdmin):
	pass

class UnidadMedidaAdmin(admin.ModelAdmin):
	pass	

class ProductoAdmin(admin.ModelAdmin):
	pass

admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(SubCategoria, SubCategoriaAdmin)
admin.site.register(Marca, MarcaAdmin)
admin.site.register(UnidadMedida, UnidadMedidaAdmin)
admin.site.register(Producto, ProductoAdmin)