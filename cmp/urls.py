from django.urls import path, include

from . import views

urlpatterns = [	
	path("proveedores/", views.ProveedorView.as_view(), name = "proveedor_list"),
	path("proveedores/create", views.ProveedorCreate.as_view(), name = "proveedor_create"),
	path("proveedores/edit/<int:pk>", views.ProveedorUpdateView.as_view(), name = "proveedor_edit"),
	path("proveedores/inactivar/<int:id>", views.proveedorDeleteView, name = "proveedor_inactivar"),

	path("compras/", views.ComprasView.as_view(), name = "compras_list"),
	path("compras/create", views.CreateCompra, name = "compras_create"),
	path("compras/edit/<int:id>", views.CreateCompra, name = "compras_edit"),
]