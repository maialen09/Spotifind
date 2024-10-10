function ejecutarAccion(accion) {


    if (accion == "Cambiar nombre de usuario"){
        fetch('/get_username')
        .then(response => response.json())  
        .then(data => {
            const username = data.username;
            window.location.href = `/cambiar_usuario?username=${username}`;

        })
        .catch(error => console.error('Error al obtener el nombre de usuario:', error));


    }
    else if (accion == "Bloquear a un usuario"){

        // Habría que cargar todos los chats que tiene el usuario y que pueda elegir cual eliminar 
        // Eliminar el chat solo para mi o para el otro usuario tambien 

        window.location.href=`/bloquear`;

    }
    else if (accion == "Desbloquear a un usuario"){

        window.location.href=`/desbloquear`;




    }

    ocultarMenu();
}

