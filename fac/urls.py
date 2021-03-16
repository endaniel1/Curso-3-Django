from django.urls import path, include

from . import views
from .reports import imprimirFacturaRecibo, imprimirFacturaList

urlpatterns = [	
	path("clientes/", views.ClienteView.as_view(), name = "cliente_list"),
	path("clientes/create", views.ClienteCreate.as_view(), name = "cliente_create"),
	path("clientes/edit/<int:pk>", views.ClienteUpdate.as_view(), name = "cliente_edit"),
	path("clientes/inactivar/<int:id>", views.clienteDelete, name = "cliente_inactivar"),

	path("facturas/", views.FacturaView.as_view(), name = "factura_list"),
	path("facturas/create", views.facturas, name = "factura_create"),
	path("facturas/edit/<int:id>", views.facturas, name = "factura_edit"),
	path("facturas/buscar_producto", views.FacProductoView.as_view(), name = "factura_producto"),
	path("facturas/borrar_detalle/<int:id>", views.borrarDetalleFactura, name = "factura_delete"),
	
	path("facturas/imprimir/<int:id>", imprimirFacturaRecibo, name = "factura_imprimir1"),
	
	path("facturas/imprimir_all/<str:f1>/<str:f2>", imprimirFacturaList, name = "facturas_imprimir_all"),

]