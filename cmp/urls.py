from django.urls import path, include

from . import views, reports

urlpatterns = [	
	path("proveedores/", views.ProveedorView.as_view(), name = "proveedor_list"),
	path("proveedores/create", views.ProveedorCreate.as_view(), name = "proveedor_create"),
	path("proveedores/edit/<int:pk>", views.ProveedorUpdateView.as_view(), name = "proveedor_edit"),
	path("proveedores/inactivar/<int:id>", views.proveedorDeleteView, name = "proveedor_inactivar"),

	path("compras/", views.ComprasView.as_view(), name = "compras_list"),
	path("compras/create", views.CreateCompra, name = "compras_create"),
	path("compras/edit/<int:id>", views.CreateCompra, name = "compras_edit"),
	path("compras/<int:compra_id>/delete/<int:pk>", views.CompraDetDelete.as_view(), name = "compras_delete"),

	path("compras/lists", reports.reporte_compras, name="compras_print_all"),
	path("compras/<int:compra_id>/imprimir", reports.imprimir_compra, name="compras_print_one"),
]