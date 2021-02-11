from django.urls import path, include

from . import views

urlpatterns = [	
	path("clientes/", views.ClienteView.as_view(), name = "cliente_list"),
	path("clientes/create", views.ClienteCreate.as_view(), name = "cliente_create"),
	path("clientes/edit/<int:pk>", views.ClienteUpdate.as_view(), name = "cliente_edit"),
	path("clientes/inactivar/<int:id>", views.clienteDelete, name = "cliente_inactivar"),

	path("facturas/", views.FacturaView.as_view(), name = "factura_list"),
	path("facturas/create", views.facturas, name = "factura_create"),
]