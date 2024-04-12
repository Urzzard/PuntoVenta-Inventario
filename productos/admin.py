from django.contrib import admin
from .models import TipoProducto, Producto, RegistroAuditoria

# Register your models here.

admin.site.register(TipoProducto)
admin.site.register(Producto)
admin.site.register(RegistroAuditoria)