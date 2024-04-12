document.addEventListener('DOMContentLoaded', function(){

    //TODO ESTO ES PARA EL BUSCADOR DE PRODUCTOS
    const todosproductos = document.querySelectorAll('.ltproductos')
    const pbuscador = document.getElementById('pbuscador');

    function buscadorProd(nombre){
        todosproductos.forEach(producto =>{
            const prodnombre = producto.querySelector('.crud-prod-nombre').textContent.toLowerCase();
            if(prodnombre.includes(nombre.toLowerCase())){
                producto.style.display = 'table-row';
            }else{
                producto.style.display = 'none';
            }
        })
    }

    pbuscador.addEventListener('input', function(){
        buscadorProd(this.value);
    })

    //PARA EL MENSAJE DE VALIDACION

    var mensaje = document.getElementById('mensajes-validacion')
    var eliminarbtn = document.querySelectorAll('#eliminarProducto')

    if(mensaje){
        mensaje.classList.remove('mensajeProducto')
        setTimeout(function() {
            mensaje.classList.add('mensajeProducto');
        }, 3000)
    }
    

    eliminarbtn.forEach(function(eliminar) {
        eliminar.addEventListener('click', function(event) {

            var confirmacion = confirm("¿ESTAS SEGURO DE ELIMINAR ESTE PRODUCTO?")

            if(confirmacion){
                
            }else{
                event.preventDefault();
            }
        })
    })

})