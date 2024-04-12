document.addEventListener("DOMContentLoaded", function(){
    var mensaje = document.getElementById('mensajes-validacion')
    var eliminarbtn = document.querySelectorAll('#elimninarVenta')

    if(mensaje){
        mensaje.classList.remove('mensajeVenta')
        setTimeout(function() {
            mensaje.classList.add('mensajeVenta');
        }, 3000)
    }
    

    eliminarbtn.forEach(function(eliminar) {
        eliminar.addEventListener('click', function(event) {

            var confirmacion = confirm("¿ESTAS SEGURO DE ELIMINAR ESTA VENTA?")

            if(confirmacion){
                
            }else{
                event.preventDefault();
            }
        })
    })

    
})
