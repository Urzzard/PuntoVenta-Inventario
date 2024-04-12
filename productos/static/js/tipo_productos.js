document.addEventListener("DOMContentLoaded", function(){
    var mensaje = document.getElementById('mensajes-validacion')
    var eliminarbtn = document.querySelectorAll('#eliminarTipo')

    if(mensaje){
        mensaje.classList.remove('mensajeTipo')
        setTimeout(function() {
            mensaje.classList.add('mensajeTipo');
        }, 3000)
    }
    

    eliminarbtn.forEach(function(eliminar) {
        eliminar.addEventListener('click', function(event) {

            var confirmacion = confirm("¿ESTAS SEGURO DE ELIMINAR ESTE TIPO DE PRODUCTO?")

            if(confirmacion){
                
            }else{
                event.preventDefault();
            }
        })
    })

    

    
})