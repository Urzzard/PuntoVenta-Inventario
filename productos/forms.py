from django import forms
from .models import TipoProducto, Producto, RegistroProducto, VentaGeneral, ProductoVenta

class CrearNuevoTP(forms.Form):
    nombre = forms.CharField(label="Tipo de Producto", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    imagen = forms.ImageField(label="Imagen", widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))

class CrearNuevoProducto(forms.Form):
    nombre = forms.CharField(label="Nombre del Producto", max_length=150, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ptipo = forms.ModelChoiceField(queryset=TipoProducto.objects.all(), label="Tipo de Producto", widget=forms.Select(attrs={'class': 'form-control'}))
    cantidad = forms.IntegerField(label="Cantidad", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    precio = forms.DecimalField(label="Precio", widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    descripcion = forms.CharField(label="Descripcion del Producto", widget=forms.Textarea(attrs={'class': 'form-control', 'rows':3}))
    imagen = forms.ImageField(label="Imagen", widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'}))


class ActualizarProducto(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'cantidad', 'precio', 'ptipo','imagen']

class ActualizarTipoProducto(forms.ModelForm):
    class Meta:
        model = TipoProducto
        fields = ['nombre', 'imagen']

class RegistroProductoForm(forms.ModelForm):
    class Meta:
        model = RegistroProducto
        fields = ['rtipo', 'rcantidad', 'rproducto', 'rrazon']
        labels = {
            'rtipo': 'Tipo de Registro',
            'rcantidad': 'Cantidad',
            'rproducto': 'Producto',
            'rrazon': 'Razón del Registro'
        }
        widgets ={
            'rtipo': forms.Select(attrs={'class': 'form-control'}),
            'rcantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'rproducto': forms.Select(attrs={'class': 'form-control'}),
            'rrazon': forms.Select(attrs={'class': 'form-control'}),
        }

class VentaGeneralForm(forms.ModelForm):
    class Meta:
        model = VentaGeneral
        fields = ['usuario', 'tipo_comprobante']
        labels = {
            'tipo_comprobante': 'Tipo de Comprobante'
        }
        widgets = {
            'tipo_comprobante': forms.Select(attrs={'class': 'form-control'})
        }

class ProductoVentaForm(forms.ModelForm):
    class Meta:
        model = ProductoVenta
        fields = ['nombre', 'precio', 'cantidad', 'subtotal']