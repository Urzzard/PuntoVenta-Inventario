document.addEventListener("DOMContentLoaded", function(){

    //VALIDACION DE ELIMINACION

    var mensaje = document.getElementById('mensajes-validacion')
    var eliminarbtn = document.querySelectorAll('#eliminarRegistro')

    if(mensaje){
        mensaje.classList.remove('mensajeRegistro')
        setTimeout(function() {
            mensaje.classList.add('mensajeRegistro');
        }, 3000)
    }

    eliminarbtn.forEach(function(eliminar) {
        eliminar.addEventListener('click', function(event) {

            var confirmacion = confirm("¿ESTAS SEGURO DE ELIMINAR ESTE REGISTRO DE PRODUCTO?")

            if(confirmacion){
                
            }else{
                event.preventDefault();
            }
        })
    })

})