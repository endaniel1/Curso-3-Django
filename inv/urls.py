from django.urls import path

from . import views

urlpatterns = [
	path("categorias/", views.CategoriaView.as_view(), name = "categoria_list"),
	path("categorias/create", views.CategoriaCreate.as_view(), name = "categoria_create"),
	path("categorias/edit/<int:pk>", views.CategoriaUpdateView.as_view(), name = "categoria_edit"),
	path("categorias/delete/<int:pk>", views.CategoriaDeleteView.as_view(), name = "categoria_delete"),

	path("subcategorias/", views.SubCategoriaView.as_view(), name = "subcategoria_list"),
	path("subcategorias/create", views.SubCategoriaCreate.as_view(), name = "subcategoria_create"),
	path("subcategorias/edit/<int:pk>", views.SubCategoriaUpdateView.as_view(), name = "subcategoria_edit"),
	path("subcategorias/delete/<int:pk>", views.SubCategoriaDeleteView.as_view(), name = "subcategoria_delete"),

	path("marcas/", views.MarcaView.as_view(), name = "marca_list"),
	path("marcas/create", views.MarcaCreate.as_view(), name = "marca_create"),
	path("marcas/edit/<int:pk>", views.MarcaUpdateView.as_view(), name = "marca_edit"),
	path("marcas/inactivar/<int:id>", views.marca_inactivar, name = "marca_inactivar"),

	path("um/", views.UMView.as_view(), name = "um_list"),
	path("um/create", views.UMCreate.as_view(), name = "um_create"),
	path("um/edit/<int:pk>", views.UMUpdateView.as_view(), name = "um_edit"),
	path("um/inactivar/<int:id>", views.um_inactivar, name = "um_inactivar"),

	path("producto/", views.ProductoView.as_view(), name = "producto_list"),
	path("producto/create", views.ProductoCreate.as_view(), name = "producto_create"),
	path("producto/edit/<int:pk>", views.ProductoUpdateView.as_view(), name = "producto_edit"),
	path("producto/inactivar/<int:id>", views.producto_inactivar, name = "producto_inactivar"),

]