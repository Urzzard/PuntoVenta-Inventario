document.addEventListener('DOMContentLoaded', function(){
    var menu = document.getElementById('m-navegacion')
    var btn = document.querySelector('.menu-toggle')

    btn.addEventListener('click',() =>{
        setTimeout(function() {
            menu.classList.toggle('m-navegacion-visible');
        }, 100)
        
        btn.querySelector('span').classList.toggle('bi-list')
        btn.querySelector('span').classList.toggle('bi-x')
    })
})