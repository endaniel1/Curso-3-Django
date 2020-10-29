from django.urls import path

from .views import CategoriaView, CategoriaCreate

urlpatterns = [
	path("categorias/", CategoriaView.as_view(), name = "categoria_list"),
	path("categorias/create", CategoriaCreate.as_view(), name = "categoria_create")
]