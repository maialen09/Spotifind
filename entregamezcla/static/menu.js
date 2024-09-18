document.getElementById('personalizacion-link').addEventListener('click', function(event) {
        event.preventDefault(); // Prevenir la acción por defecto del enlace
        // Enviar el formulario oculto
        document.getElementById('personalizacion-form').submit();
    });