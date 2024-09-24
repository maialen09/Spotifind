// Función para cambiar la imagen según la categoría
function updateImage(category, selectedColor) {
        const image = document.getElementById(`${category}-image`);
        // gestionar el borrar la imagen cuando se deselecciona
        if (selectedColor == null){
            image.src = '';
        }

        else{

        image.src = `../static/images/${category}/${selectedColor}.png`; 
        }
}

function handleRadioClick(event) {
    const category = this.dataset.category;

    // Obtener todos los radio buttons que comparten el mismo name
    const radioButtons = document.querySelectorAll(`input[name="${this.name}"]`);

    // Eliminar las imágenes de todos los radio buttons del mismo name
    radioButtons.forEach((radio) => {
        updateImage(radio.dataset.category, null);
    });

    // Si ya estaba seleccionado, deseleccionarlo y no mostrar ninguna imagen
    if (this.dataset.wasChecked === 'true') {
        this.checked = false;
        this.dataset.wasChecked = 'false';
    } 
    // Si no estaba seleccionado, marcar este radio y mostrar la nueva imagen
    else {
        this.checked = true;
        this.dataset.wasChecked = 'true';
        updateImage(this.dataset.category, this.id);  // Mostrar la imagen del radio seleccionado
    }

    // Asegurarse de que los otros radios de la misma categoría estén desmarcados
    radioButtons.forEach((radio) => {
        if (radio !== this) {
            radio.dataset.wasChecked = 'false';
        }
    });
}


// Manejo de cambios para cada categoría
const radiosBody = document.querySelectorAll('input[name="body_type"]');
radiosBody.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('color cuerpo', this.id);
    //});
    radio.dataset.category = 'color cuerpo';
    radio.addEventListener('click', handleRadioClick);
});

const radiosOjos = document.querySelectorAll('input[name="ojos"]');
radiosOjos.forEach((radio) => {
    //radio.addEventListener('change', function() {
        
      //  if (this.value == "cuadradas"){
            
        //    updateImage('gafas_rectangulares', this.id);
       // }
        //else{
          //  updateImage('gafas_redondas', this.id);
        //}
        
    //});

    if (radio.value == "medios"){
        radio.dataset.category = 'ojos_medios';
        radio.addEventListener('click', handleRadioClick);
    }

    else if (radio.value == "redondos"){
        radio.dataset.category = 'ojos_redondos';
        radio.addEventListener('click', handleRadioClick);
    }

    else{
        radio.dataset.category = 'ojos_aplastados';
        radio.addEventListener('click', handleRadioClick);
    }
});

const radiosCamisetas = document.querySelectorAll('input[name="camisetas"]');
radiosCamisetas.forEach((radio) => {
    //radio.addEventListener('change', function() {
        //updateImage('ojos', this.id);
    //});
    if (radio.value == "manga_corta"){
        radio.dataset.category = 'camiseta_manga_corta';
        radio.addEventListener('click', handleRadioClick);
    }

    else if (radio.value == "tirantes"){
        radio.dataset.category = 'camiseta_tirantes';
        radio.addEventListener('click', handleRadioClick);
    }

    else if (radio.value == "sudadera"){
        radio.dataset.category = 'camiseta_sudaderas';
        radio.addEventListener('click', handleRadioClick);

    }
    else if (radio.value == "manga_larga"){

        radio.dataset.category = 'camiseta_mangas_largas';
        radio.addEventListener('click', handleRadioClick);

    }
    else{

        radio.dataset.category = 'camiseta_camisa';
        radio.addEventListener('click', handleRadioClick);

    }

});



const radiosBocas = document.querySelectorAll('input[name="bocas"]');
radiosBocas.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('bocas', this.id);
    //});

    radio.dataset.category = 'bocas';
    radio.addEventListener('click', handleRadioClick);
});

const radiosPelos = document.querySelectorAll('input[name="pelos"]');
radiosPelos.forEach((radio) => {
    //radio.addEventListener('change', function() {
        //updateImage('ojos', this.id);
    //});
    if (radio.value == "melena1"){
        radio.dataset.category = 'melena1';
        radio.addEventListener('click', handleRadioClick);
    }

    else if (radio.value == "pelo_corto1"){
        radio.dataset.category = 'pelo_corto1';
        radio.addEventListener('click', handleRadioClick);
    }

    else if (radio.value == "melena2"){
        radio.dataset.category = 'melena2';
        radio.addEventListener('click', handleRadioClick);

    }
    else if (radio.value == "pelo_corto2"){

        radio.dataset.category = 'pelo_corto2';
        radio.addEventListener('click', handleRadioClick);

    }
    else if (radio.value == "cresta"){

        radio.dataset.category = 'cresta';
        radio.addEventListener('click', handleRadioClick);

    }
    else if (radio.value == "pelo_corto3"){

        radio.dataset.category = 'pelo_corto3';
        radio.addEventListener('click', handleRadioClick);

    }
    else{

        radio.dataset.category = 'rapado';
        radio.addEventListener('click', handleRadioClick);

    }

});



document.addEventListener('DOMContentLoaded', () => {
document.getElementById('guardar').addEventListener('click', () => {

    const images = document.querySelectorAll('.image-container img');
    const canvas = document.getElementById('combinedCanvas');
    const ctx = canvas.getContext('2d');
    
    // Asegúrate de ajustar el tamaño del canvas al tamaño de las imágenes
    const width = images[0].naturalWidth;
    const height = images[0].naturalHeight;
    canvas.width = width;
    canvas.height = height;

    // Dibujar todas las imágenes en el canvas
    images.forEach(image => {
        if (image.src) { // Solo dibujamos si la imagen tiene una fuente
            ctx.drawImage(image, 0, 0, width, height);
        }
    });

    // Convertir el canvas a una imagen y mostrarla en la pantalla
    const resultContainer = document.getElementById('result-container');
    const dataURL = canvas.toDataURL('image/png');

    // Crear una nueva imagen con el resultado
    const combinedImage = new Image();
    combinedImage.src = dataURL;

    const base64Data = dataURL.replace(/^data:image\/(png|jpg);base64,/, '');

    fetch('/guardar_imagen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            imagen: base64Data,
        }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Imagen guardada correctamente', data);
    })
    .catch(error => {
        console.error('Error al guardar la imagen:', error);
    });

    
    // Limpiar el contenedor anterior y mostrar la nueva imagen
    resultContainer.innerHTML = '';  // Limpiar cualquier imagen anterior
    resultContainer.appendChild(combinedImage); 


    
});

});
