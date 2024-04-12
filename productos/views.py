from django.contrib.auth.decorators import login_required
from django.db.models import Sum, DateTimeField
from django.db.models.functions import TruncDate
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime
from django.shortcuts import get_object_or_404
import json
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .models import TipoProducto, Producto, RegistroProducto, VentaGeneral, ProductoVenta, RegistroAuditoria
from .forms import CrearNuevoTP, CrearNuevoProducto, ActualizarProducto, ActualizarTipoProducto, RegistroProductoForm, VentaGeneralForm, ProductoVentaForm


# Create your views here.

@login_required
def index(request):
    return render(request, 'index.html')


# ESTA VISTA NOS AYUDA A MANDAR INFORMACION DE BD AL FRONTEND PARA PODER UTILIZARLA

def api_productos(request):
    productos = list(Producto.objects.values())
    vgeneral = list(VentaGeneral.objects.values())
    pventa = list(ProductoVenta.objects.values())

    #PARA SACAR LAS VENTAS DIARIAS

    vxd = []
    ventapordia = {}

    for vg in vgeneral:
        fecha = vg['fecha_hora'].date()
        total = vg['total']

        if fecha not in ventapordia:
            ventapordia[fecha] = 0

        ventapordia[fecha] += total

    for fecha, total in ventapordia.items():
        vagrupado = {
            'fecha': fecha,
            'total': total
        }
        vxd.append(vagrupado)

    #PARA SACAR LOS PRODUCTOS MAS VENDIDOS

    pmv = []
    pvinfo = {}

    for pv in pventa:
        pvnombre = pv['nombre']
        pvcantidad = pv['cantidad']
        pvsubtotal = pv['subtotal']

        if pvnombre not in pvinfo:
            pvinfo[pvnombre] = {'cantidad': 0, 'total': 0}

        pvinfo[pvnombre]['cantidad'] += pvcantidad
        pvinfo[pvnombre]['total'] += pvsubtotal

    
    for pvnombre, pvdata in pvinfo.items():
        pmvagrupado = {
            'nombre': pvnombre,
            'cantidad': pvdata['cantidad'],
            'total': pvdata['total']
        }
        pmv.append(pmvagrupado)




    datos = {
            'p': productos,
            'vxd': vxd,
            'pmv': pmv
            
        }
        
    return JsonResponse(datos)



def iniciar_sesion(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            RegistroAuditoria.objects.create(usuario=request.user,accion=f'Inicio sesion')
            return redirect('index')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos!!')
    return render(request, 'login.html')

@login_required
def MCTipoProductos(request):

    #Para guiarnos en el ordenamiento
    orden = request.GET.get('orden', 'nombre')
    #para establecer el ordenamiento
    modo = request.GET.get('modo', 'asc')

    if modo == 'asc':
        sig_modo = 'desc'
    else:
        sig_modo = 'asc'

    if request.method == 'GET':
        if orden in ['id', 'nombre']:
            if modo == 'asc':
                tproductos = TipoProducto.objects.all().order_by(orden)
            else:
                tproductos = TipoProducto.objects.all().order_by('-' + orden)
        else:
            tproductos = TipoProducto.objects.all().order_by('nombre')
        return render(request, 'productos/tipo_productos.html', {
            'formTP': CrearNuevoTP(),
            'tp': tproductos,
            'orden': orden,
            'sig_modo': sig_modo
        })
    
    elif request.method=='POST':
        if 'elimiarTipoProducto' in request.POST:
            tpid = request.POST['elimiarTipoProducto']
            TipoProducto.objects.filter(id=tpid).delete()
            RegistroAuditoria.objects.create(usuario=request.user,accion=f'Eliminó el Tipo de producto : {tproductos.nombre}')
            messages.success(request, '¡Tipo de Producto eliminado correctamente!')


        elif 'editarTipoProducto' in request.POST:
            etpid = request.POST['editarTipoProducto']
            etp = TipoProducto.objects.get(id=etpid)
            etpform = ActualizarTipoProducto(request.POST, instance=etp)
            #Y si todo esta en orden lo guarda
            if etpform.is_valid():
                etpform.save()
                RegistroAuditoria.objects.create(usuario=request.user,accion=f'Editó el Tipo de producto : {tproductos.nombre}')
                messages.success(request, '¡Tipo de Producto editado correctamente!')

        else:
            tpform =CrearNuevoTP(request.POST, request.FILES)
            if tpform.is_valid():
                TipoProducto.objects.create(
                    nombre = request.POST['nombre'],
                    imagen = request.FILES['imagen']
                )
                RegistroAuditoria.objects.create(usuario=request.user,accion=f'Creó el Tipo de producto : {tproductos.nombre}')
                messages.success(request, 'Tipo de Producto creado correctamente!!')
            else:
                print(tpform.errors)
        return redirect('tipo_productos')
    
@login_required
def MCProductos(request):
    #Para listar los tipos de productos
    tipos = TipoProducto.objects.all()

    #Para guiarnos en el ordenamiento
    orden = request.GET.get('orden', 'nombre')

    #para establecer el ordenamiento
    modo = request.GET.get('modo', 'asc')

    #Validacion de ordenamiento
    if modo == 'asc':
        sig_modo = 'desc'
    else:
        sig_modo = 'asc'

    #Esta validacion sirve para mostrar los elementos de acuerdo al metodo
    if request.method == 'GET':
        
        if orden in ['id', 'nombre', 'ptipo', 'descripcion', 'precio', 'cantidad']:
            if modo == 'asc':
                productos = Producto.objects.all().order_by(orden)
            else:
                productos = Producto.objects.all().order_by('-' + orden)
        else:
            productos = Producto.objects.all().order_by('nombre')
        return render(request, 'productos/productos.html', {
            'formP': CrearNuevoProducto(),
            'p': productos,
            'tipos': tipos,
            'orden': orden,
            'sig_modo': sig_modo
        })

    #Si es diferente este eliminara, editara o guardara
    elif request.method=='POST':
        #Esta validacion es para eliminar
        if 'elimninarProducto' in request.POST:
            pid = request.POST['elimninarProducto']
            Producto.objects.filter(id=pid).delete()
            RegistroAuditoria.objects.create(usuario=request.user,accion=f'Eliminó el Producto : {productos.nombre}')
            messages.success(request, '¡Producto eliminado correctamente!')
        
        #Esta validacion es para editar
        elif 'editarProducto' in request.POST:
            epid = request.POST['editarProducto']
            ep = Producto.objects.get(id=epid)
            eform = ActualizarProducto(request.POST, instance=ep)
            #Y si todo esta en orden lo guarda
            if eform.is_valid():
                eform.save()
                RegistroAuditoria.objects.create(usuario=request.user,accion=f'Editó el Producto : {productos.nombre}')
                messages.success(request, '¡Producto editado correctamente!')

        #De lo contrario en el que la accion sea diferente guarda datos
        else:
            form = CrearNuevoProducto(request.POST, request.FILES)
            if form.is_valid():
                Producto.objects.create(
                    nombre = request.POST['nombre'],
                    descripcion = request.POST['descripcion'],
                    cantidad = request.POST['cantidad'],
                    precio = request.POST['precio'],
                    ptipo_id = request.POST['ptipo'],
                    imagen = request.FILES['imagen']
                )
                RegistroAuditoria.objects.create(usuario=request.user,accion=f'Creó el Producto : {productos.nombre}')
                messages.success(request, '¡Producto creado correctamente!')
        return redirect('productos')


@login_required
def CRUDRegistro(request):

    orden = request.GET.get('orden', 'nombre')
    modo = request.GET.get('modo', 'asc')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    #Validacion de ordenamiento
    if modo == 'asc':
        sig_modo = 'desc'
    else:
        sig_modo = 'asc'

    if request.method == 'GET':

        pregistro = RegistroProducto.objects.all()
        if fecha_inicio and fecha_fin:
            fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
            fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))
            pregistro = pregistro.filter(rfecha__range=[fecha_inicio, fecha_fin])

        if orden in ['id', 'rproducto', 'rtipo', 'rcantidad', 'rusuario', 'rfecha']:
            if modo == 'asc':
                pregistro = pregistro.order_by(orden)
            else:
                pregistro = pregistro.order_by('-' + orden)
        else:
            pregistro = pregistro.order_by('rfecha')
        rform = RegistroProductoForm()
    elif request.method == 'POST':
        if 'eliminarRegistro' in request.POST:
            rpid = request.POST['eliminarRegistro']
            RegistroProducto.objects.filter(id=rpid).delete()
            RegistroAuditoria.objects.create(usuario=request.user,accion=f'Elimino el Registro: {rpid}')
            messages.success(request, '¡Registro eliminado correctamente!')
        else:
            rform = RegistroProductoForm(request.POST)
            if rform.is_valid():
                pregistro = rform.save(commit=False)
                RegistroAuditoria.objects.create(usuario=request.user,accion=f'Creó el Registro de: {pregistro.rproducto} dando {pregistro.rtipo} de {pregistro.rcantidad} unidades')
                messages.success(request, '¡Registro creado correctamente!')

                if pregistro.rtipo == 'Ingreso':
                    pregistro.rproducto.cantidad += pregistro.rcantidad
                elif pregistro.rtipo == 'Salida':
                    pregistro.rproducto.cantidad -= pregistro.rcantidad
                    if pregistro.rproducto.cantidad < 0:
                        return redirect('crud_registro_productos')

                pregistro.rproducto.save()
                pregistro.rusuario = request.user
                pregistro.save()

        return redirect('crud_registro_productos')

    return render(request, 'productos/registro_productos.html',{
        'pregistro': pregistro,
        'rform': rform,
        'orden': orden,
        'sig_modo': sig_modo,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })
    
@csrf_exempt
def puntoVenta(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        jtotal = data['total']
        jtipo_comprobante = data['tipo_comprobante']

        venta_general = VentaGeneral.objects.create(
            usuario = request.user,
            total = jtotal,
            tipo_comprobante = jtipo_comprobante
        )

        for productos in data['productos']:

            prod = get_object_or_404(Producto, nombre = productos['nombre'])
            cantidad_vendida = productos['cantidad']
            prod.cantidad -= cantidad_vendida
            prod.save()

            producto_venta = ProductoVenta.objects.create(
                venta = venta_general,
                nombre = productos['nombre'],
                precio = productos['precio'],
                cantidad = productos['cantidad'],
                subtotal = productos['subtotal']
            )
        return redirect('punto_venta')

    tproducto = TipoProducto.objects.all()
    producto = Producto.objects.all()

    return render(request, 'productos/punto_venta.html',{
        'formVG': VentaGeneralForm,
        'tproducto': tproducto,
        'producto': producto,
    })

def resumenVentas(request):
    ventaGeneral = VentaGeneral.objects.all()
    productoVenta = ProductoVenta.objects.all()
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')

    if fecha_inicio and fecha_fin:
            fecha_inicio = timezone.make_aware(datetime.strptime(fecha_inicio, '%Y-%m-%dT%H:%M'))
            fecha_fin = timezone.make_aware(datetime.strptime(fecha_fin, '%Y-%m-%dT%H:%M'))
            ventaGeneral = ventaGeneral.filter(fecha_hora__range=[fecha_inicio, fecha_fin])

    if request.method == 'POST':
        if 'elimninarVenta' in request.POST:
            vpid = request.POST['elimninarVenta']
            veliminada = VentaGeneral.objects.get(id=vpid)
            totalveliminada = veliminada.total
            veliminada.delete()
            RegistroAuditoria.objects.create(usuario=request.user,accion=f'Elimino la venta: {vpid} con un total de S/. {totalveliminada}')
            messages.success(request, '¡Venta eliminada correctamente!')
        
        return redirect('ventas')

    return render(request, 'productos/ventas.html',{
        'vg': ventaGeneral,
        'pv': productoVenta,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    })

