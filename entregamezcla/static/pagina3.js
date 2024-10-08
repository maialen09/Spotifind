function filtrarUsuarios() {
    // Obtener el valor del campo de búsqueda y pasarlo a minúsculas
    var input = document.getElementById('buscador');
    var filter = input.value.toLowerCase();
    
    // Obtener todos los botones con los nombres de usuarios
    var botones = document.getElementsByTagName('button');

    // Recorrer los botones y mostrar u ocultar según el filtro
    for (var i = 0; i < botones.length; i++) {
        var texto = botones[i].textContent || botones[i].innerText;
        if (texto.toLowerCase().indexOf(filter) > -1) {
            botones[i].style.display = "";
        } else {
            botones[i].style.display = "none";
        }
    }
}

function mostrarMenu(event, usuario) {
    // Obtener el menú
    var menu = document.getElementById('menu-opciones');
    
    // Mostrar el menú
    menu.style.display = 'block';
    
    // Posicionarlo según la posición del clic
    menu.style.top = event.clientY + 'px';
    menu.style.left = event.clientX + 'px';
    
    // Pasar el nombre del usuario al menú (para acciones futuras)
    menu.setAttribute('data-usuario', usuario);
}

// Función para ocultar el menú
function ocultarMenu() {
    document.getElementById('menu-opciones').style.display = 'none';
}

// Función para manejar las acciones del menú
function ejecutarAccion(accion) {

    var usuario = document.getElementById('menu-opciones').getAttribute('data-usuario');

    if (accion == "Eliminar usuario"){
        if (confirm('¿Estás seguro de que deseas eliminar al usuario ' + usuario + '?')) {
            // Hacer una solicitud POST al servidor para eliminar el usuario
            fetch('/eliminar_usuario', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ user_id: usuario })  // Enviar el nombre de usuario al servidor
            })
            .then(response => response.json())
            .then(data => {
                alert(data.message);  // Mostrar el mensaje del servidor
                // Opción: recargar la página o actualizar la lista de usuarios
                window.location.reload();  // Recargar la página después de eliminar el usuario
            })
            .catch(error => console.error('Error:', error));
        }
     else {
        alert('Acción "' + accion + '" ejecutada para el usuario: ' + usuario);
    }


    }
    else if (accion == "Ver personaje"){

        // Ver las opciones que tiene cargadas el usuario y poder cambiarlas????

    }
    else if (accion == "Ver 10 últimas canciones" ){

    }

    ocultarMenu();
}


window.onclick = function(event) {
    if (!event.target.matches('.menu-btn')) {
        ocultarMenu();
    }
}