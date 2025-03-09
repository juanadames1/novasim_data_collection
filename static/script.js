let tipoEntrada = '';

document.querySelectorAll('.input-type-button').forEach(button => {
    button.addEventListener('click', function() {
        tipoEntrada = this.getAttribute('data-type');
        document.getElementById('mensaje').textContent = `Tipo de entrada seleccionado: ${tipoEntrada}`;
        document.querySelectorAll('.input-type-button').forEach(btn => btn.classList.remove('selected'));
        this.classList.add('selected');
    });
});

function registrar(accion) {
    if (!tipoEntrada) {
        document.getElementById('mensaje').textContent = 'Seleccione el tipo de entrada primero.';
        return;
    }


    const botones = document.querySelectorAll('.action-button');
    botones.forEach(btn => btn.classList.remove('highlight'));  
    document.getElementById(`btn-${accion}`).classList.add('highlight'); 

    if (accion === 'entrada') {
        setTimeout(() => {
            botones.forEach(btn => btn.classList.remove('highlight'));
        }, 1000);  // El resaltado desaparecerá después de 1 segundo
    }

    fetch('/registrar_tiempo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ tipo_entrada: tipoEntrada, accion: accion })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('mensaje').textContent = data.mensaje;
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('mensaje').textContent = 'Error al registrar el tiempo.';
    });
}