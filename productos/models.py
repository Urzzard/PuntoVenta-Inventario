from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.

class TipoProducto(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='tipo_productos_images/', blank=False, null=False, default='default.jpg')

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField()
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    ptipo = models.ForeignKey(TipoProducto, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='producto_images/', blank= True, null=True, default='default.jpg')

    def __str__(self):
        return self.nombre + ' - ' + self.ptipo.nombre

#ESTO SIRVE PARA GUARDAR LOS NOMBRES DE LOS PRODUCTOS EN MAYUSCULA
@receiver(pre_save, sender=Producto)
def prodUpper(sender, instance, **kwargs):
    instance.nombre = instance.nombre.upper()
    
class RegistroProducto(models.Model):
     
     TIPO_REGISTROS = {
         ('Ingreso', 'Ingreso'),
         ('Salida', 'Salida'),
     }
     RAZON_REGISTROS = {
         ('Traslado', 'Traslado'),
         ('Compra', 'Compra'),
         ('Expiró', 'Expiró'),
     }
     rtipo = models.CharField(max_length=10, choices=TIPO_REGISTROS)
     rcantidad = models.IntegerField()
     rproducto = models.ForeignKey(Producto, on_delete=models.CASCADE)
     rrazon = models.CharField(max_length=20, choices=RAZON_REGISTROS)
     rusuario = models.ForeignKey(User, on_delete=models.CASCADE)
     rfecha = models.DateTimeField(auto_now_add=True)

     def __str__(self):
        return self.tipo + ' - ' + self.producto.nombre

class VentaGeneral(models.Model):
    TIPO_COMPROBANTES = {
        ('Boleta Electronica', 'Boleta Electronica'),
        ('Factura Electronica', 'Factura Electronica')
    }
    usuario  = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    tipo_comprobante = models.CharField(max_length=100, choices=TIPO_COMPROBANTES)
    fecha_hora = models.DateTimeField(auto_now_add=True)

class ProductoVenta(models.Model):
    venta = models.ForeignKey(VentaGeneral, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class RegistroAuditoria(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    accion = models.CharField(max_length=100)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario} - {self.accion} el {self.fecha}"


