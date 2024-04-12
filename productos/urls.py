from django.urls import path
from . import views

urlpatterns = [
    path('', views.iniciar_sesion, name="login"),
    path('home/', views.index, name="index"),
    path('api/', views.api_productos, name="api_productos"),
    path('productos/', views.MCProductos, name="productos"),
    path('tipo_productos/', views.MCTipoProductos, name="tipo_productos"),
    path('registro_productos/', views.CRUDRegistro, name="crud_registro_productos"),
    path('productos/punto_venta/', views.puntoVenta, name="punto_venta"),
    path('resumen_ventas/', views.resumenVentas, name="ventas")
]