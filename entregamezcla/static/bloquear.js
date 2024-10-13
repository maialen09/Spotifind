function bloquear(user_id){

    fetch('/bloquear_usuario', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ bloqueado_id: user_id })  // Enviar el nombre de usuario al servidor
    })
    .then(response => response.json())
    .then(data => {
        window.location.reload();  // Recargar la página después de eliminar el usuario
    })
    .catch(error => console.error('Error:', error));

}

function volverAlPerfil(){
    window.location.href = `/opciones`;

}