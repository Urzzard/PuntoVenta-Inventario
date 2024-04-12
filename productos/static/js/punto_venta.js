//PARA EL LISTADO
document.addEventListener("DOMContentLoaded", function() {
    const tipoProductos = document.querySelectorAll('.tipo-producto');
    const productos = document.querySelectorAll('.producto');
    const buscador = document.getElementById('buscador');

    //PARA EL FILTRO POR NOMBRES DE PRODUCTO

    function filtrarProductos(texto){
        productos.forEach(producto =>{
            const pnombre = producto.querySelector('.p-nombre').textContent.toLowerCase();
            if(pnombre.includes(texto.toLowerCase())){
                producto.style.display = 'block';
            }else{
                producto.style.display = 'none';
            }
        }); 
    }


    buscador.addEventListener('input', function(){
        filtrarProductos(this.value);
    })


    //PARA EL FILTRO POR TIPOS DE PRODUCTOS

    tipoProductos.forEach(tipo => {
        tipo.addEventListener('click', () => {
            const tipoId = tipo.dataset.tipoId;
            
            productos.forEach(producto => {
                if (tipoId === 'todos' || tipo.dataset.tipoId === 'todos') {
                    producto.style.display = 'block';
                }else{
                    if( producto.dataset.tipoId === tipoId){
                        producto.style.display = 'block';
                    }else{
                        producto.style.display = 'none';
                    }
                }
            });
        });
    });




    //PARA EL LISTADO DE PRODUCTOS

    let ventas = [];
    

    const plista = document.querySelector('.productos-lista')
    const listaVenta = document.querySelector('.table tbody')
    const vplista = document.querySelector('.v-lista')
    const totalRow = document.querySelector('.lpt-total');

    accion()

    function accion(){
        plista.addEventListener('click', agregarproducto);
        vplista.addEventListener('click', eliminarProducto);
    }

    function agregarproducto(e){
        e.preventDefault();

        if(e.target.closest('.producto')){
            const productoseleccionado = e.target.closest('.producto');
            console.log('agregando producto')
            leerproductos(productoseleccionado)
        }
    }

    function leerproductos(plista){
        const infoProducto = {
            imagen: plista.querySelector('img').src,
            nombre: plista.querySelector('.p-nombre').textContent,
            precio: plista.querySelector('.pp').textContent,
            id: plista.dataset.id,
            cantidad: 1
        }

        const existe = ventas.some( producto => producto.id === infoProducto.id)

        if(existe){
            ventas = ventas.map(producto =>{
                if(producto.id === infoProducto.id){
                    producto.cantidad++;
                    return producto;
                }else{
                    return producto;
                }
            });
        }else{
            ventas.push(infoProducto);
        }

        console.log(ventas);

        listaHTML()
    }

    function listaHTML(){

        limpiarRepetido()

        let total = 0;

        ventas.forEach( producto =>{
            const { imagen, nombre, precio, cantidad, id } = producto
            const subtotal = precio*cantidad;
            producto.subtotal = subtotal
            total += subtotal;

            const row = document.createElement('tr');
            row.innerHTML = `
            <td>
                <img src="${imagen}">
            </td>
            <td>
                ${nombre}
            </td>
            <td>
                ${precio}
            </td>
            <td>
                ${cantidad}
            </td>
            <td>
                S/.${subtotal}
            </td>
            <td>
                <a href="#" class="borrar-producto" data-id="${id}"> x </a>
            </td>                
            `;

            listaVenta.appendChild(row);

        })
        totalRow.textContent = total.toFixed(2);
        document.getElementById('total').value = total.toFixed(2);
    }


    function limpiarRepetido(){
        while(listaVenta.firstChild){
            listaVenta.removeChild(listaVenta.firstChild);
        }
    }

    function eliminarProducto(e){
        if(e.target.classList.contains('borrar-producto')){
            const borrarxId = e.target.getAttribute('data-id');
            ventas = ventas.filter(producto => producto.id !== borrarxId);
            listaHTML();
        }
    }


    //FUNCION PARA GUARDAR LA VENTA

    function guardarVenta(event){
        event.preventDefault();

        if(ventas.length === 0){
            mostrarMensajes('No se agregaron productos!!', 'error');
            return;
        }else{
            const datos = {
                total: totalRow.textContent,
                tipo_comprobante: document.getElementById('id_tipo_comprobante').value,
                productos: ventas
            };
    
            console.log(datos)
    
            fetch('/productos/punto_venta/',{
                method: 'POST',
                headers:{
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(datos)
            })
            .then(respuesta => {
                if(respuesta.ok){
                    mostrarMensajes('La venta se realizó satisfactoriamente.', 'success');
                    location.reload();
                }else{
                    console.error('Error al guardar la venta');
                }
            })
            .catch(error =>{
                console.error('Error al procesar la solicitud: ', error);
            });
        }

        

    }

    document.getElementById('venta-formulario').addEventListener('submit', guardarVenta)

    /*MENSAJES DE VALIDACION PARA EL PUNTO DE VENTA*/

    function mostrarMensajes(mensaje, tipo){
        const mensajeTexto = document.getElementById('mensaje-contenido');
        mensajeTexto.textContent = mensaje;
        const cajamsg = document.getElementById('mensaje');

        cajamsg.classList.remove('success', 'error');

        if(tipo === 'error'){
            cajamsg.classList.add('alert', 'alert-danger');
        }else if(tipo === 'success')
            cajamsg.classList.add('alert', 'alert-success');
            sessionStorage.setItem('exito', 'mostrado');

        cajamsg.classList.remove('msg-ocultar');
        
        setTimeout(function() {
            if(!sessionStorage.getItem('recargarPagina')){
                cajamsg.classList.add('msg-ocultar');
            }
            
        }, 3000);
        
    }

    window.onload = function(){
        if(sessionStorage.getItem('exito')){
            mostrarMensajes('La venta se realizó satisfactoriamente.', 'success');
            sessionStorage.removeItem('exito')
        }
    }


});


