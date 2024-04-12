document.addEventListener('DOMContentLoaded', function() {

    fetch('/api',{method: 'GET'})
    .then(respuesta => respuesta.json())
    .then(data =>{
        datos = data;

        const productos = datos.p;
        const vxd = datos.vxd;
        const pmv = data.pmv

        //PARA PRODUCTOS QUE TENGAN MENOR CANTIDAD

        const pnombreMIN = [];
        const pcantidadMIN = [];

        productos.forEach(producto => {
            if(producto.cantidad < 10){
                pnombreMIN.push(producto.nombre)
                pcantidadMIN.push(producto.cantidad)
            }
            
        })

        var grafico1 = document.getElementById('pstock').getContext('2d');
        var dg1 = new Chart(grafico1, {
            type: 'bar',
            data: {
                labels: pnombreMIN,
                datasets: [{
                    label: 'Stock de Productos',
                    data: pcantidadMIN,
                    backgroundColor: ['rgba(255, 99, 132, 0.2)'],
                    borderColor: ['rgba(255, 99, 132, 1)'],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


        // PARA TOTAL DE VENTAS X DIA

        const fventa = [];
        const tventa = [];

        vxd.forEach(venta => {
            fventa.push(venta.fecha)
            tventa.push(venta.total)
        })


        var grafico2 = document.getElementById('ventapordia').getContext('2d');
        var dg2 = new Chart(grafico2, {
            type: 'line',
            data: {
                labels: fventa,
                datasets: [{
                    label: 'Total de ventas en soles',
                    data: tventa,
                    backgroundColor: ['rgba(99, 255, 107, 0.2)'],
                    borderColor: ['rgba(16, 58, 18, 0.2)'],
                    borderWidth: 1
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });


        // PRODUCTO CON MAS VENTAS

        const vnombre = [];
        const vcantidad = [];
        const vtotal = [];

        pmv.sort((a,b) => b.cantidad - a.cantidad).slice(0,5).forEach(pventa => {

            vnombre.push(pventa.nombre)
            vcantidad.push(pventa.cantidad)
            vtotal.push(pventa.total)
            
        })

        var grafico3 = document.getElementById('pmayorventas').getContext('2d');
        var dg3 = new Chart(grafico3, {
            type: 'bar',
            data: {
                labels: vnombre,
                datasets: [{
                    label: 'Unidades vendidas',
                    data: vcantidad,
                    backgroundColor: ['rgba(99, 193, 255, 0.2)'],
                    borderColor: ['rgba(0, 67, 112, 0.486)'],
                    borderWidth: 1
                }]
            },
            options: {
                maintainAspectRatio: true,
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                var label = context.dataset.label || '';
                                if (label) {
                                    label += ': ';
                                }
                                if (context.parsed.y !== null) {
                                    label += context.parsed.y;
                                    var vtotalValue = vtotal[context.dataIndex];
                                    if (vtotalValue !== undefined) {
                                        label += ' (Total: S/.' + vtotalValue + ')';
                                    }
                                }
                                return label;
                            }
                        }
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });

        if (window.innerWidth < 600) {
            dg1.options.plugins.legend.display = false;
        }

    })

});