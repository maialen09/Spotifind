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

function selectFirstBody() {
    const radiosBody = document.querySelectorAll('input[name="body_type"]');
    if (radiosBody.length > 0) {
        const firstRadio = radiosBody[0];
        firstRadio.checked = true;
        firstRadio.dataset.wasChecked = 'true';
        updateImage(firstRadio.dataset.category, firstRadio.id);
    }
}

function getSelectedButtons() {
    const categories = ['body_type', 'ojos', 'camisetas', 'bocas', 'pelos', 'pantalones', 'gafas', 'zapatillas', 'accesorios'];
    const selectedButtons = {};

    categories.forEach((category) => {
        const selectedRadio = document.querySelector(`input[name="${category}"]:checked`);

        if (selectedRadio) {
            // Verifica si la categoría ya existe en el objeto
            if (!selectedButtons[category]) {
                selectedButtons[category] = {}; // Crea un objeto para subcategorías si no existe
            }
            // Almacena el valor y el ID en la subcategoría
            selectedButtons[category][selectedRadio.value] = selectedRadio.id; 
        } else {
            selectedButtons[category] = {}; // Ningún botón seleccionado en esta categoría
        }
    });

    return selectedButtons;
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

        if (category === 'color cuerpo') {
            selectFirstBody();
        }
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

const radiosPantalones = document.querySelectorAll('input[name="pantalones"]');
radiosPantalones.forEach((radio) => {
    //radio.addEventListener('change', function() {
        //updateImage('ojos', this.id);
    //});
    if (radio.value == "faldas"){
        radio.dataset.category = 'faldas';
        radio.addEventListener('click', handleRadioClick);
    }

    else if (radio.value == "pantalon_corto"){
        radio.dataset.category = 'pantalon_corto';
        radio.addEventListener('click', handleRadioClick);
    }

    
    else{

        radio.dataset.category = 'pantalon_largo';
        radio.addEventListener('click', handleRadioClick);

    }

});

const radiosGafas = document.querySelectorAll('input[name="gafas"]');
radiosGafas.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('bocas', this.id);
    //});

    radio.dataset.category = 'gafas';
    radio.addEventListener('click', handleRadioClick);
});

const radiosZapatillas = document.querySelectorAll('input[name="zapatillas"]');
radiosZapatillas.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('bocas', this.id);
    //});

    radio.dataset.category = 'zapatillas';
    radio.addEventListener('click', handleRadioClick);
});

const radiosAccesorios = document.querySelectorAll('input[name="accesorios"]');
radiosAccesorios.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('bocas', this.id);
    //});

    radio.dataset.category = 'accesorios';
    radio.addEventListener('click', handleRadioClick);
});




function obtenerOpciones(){
    fetch('/api/opciones')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log('Opciones:', data);
        if (data.length == 0){
            console.log("Estoy entrando aqui")
            selectFirstBody();
        }
        else{
            data = data[0];
            Object.keys(data).forEach(category => {
            const selectedValue = data[category];  // Obtiene el valor seleccionado
            console.log("selectedValue:", selectedValue);
            console.log("category:", category);
            if (selectedValue) {
                if (category == "accesorio"){
                    category = "accesorios"
                    const accesorioRadio = document.querySelector(`input[name="accesorios"][value="${selectedValue}"]`);
                    accesorioRadio.checked = true;
                    updateImage(category, selectedValue);
                
                }

                else if (category == "boca"){
                    category = "bocas";
                    const bocasRadio = document.querySelector(`input[name="bocas"][value="${selectedValue}"]`);
                    bocasRadio.checked = true;
                    updateImage(category, selectedValue);
                }

                else if (category == "gafas"){
                    const gafasRadio = document.querySelector(`input[name="gafas"][value="${selectedValue}"]`);
                    gafasRadio.checked = true;
                    updateImage(category, selectedValue);
                }
                else if (category == "zapatillas"){

                    const zapatillasRadio = document.querySelector(`input[name="zapatillas"][value="${selectedValue}"]`);
                    zapatillasRadio.checked = true;
                    updateImage(category, selectedValue);
                }

                else if (category == "cuerpo_categoria"){
                    category = "color cuerpo";
                    const cuerpoRadio = document.querySelector(`input[name="body_type"][value="${selectedValue}"]`);
                    cuerpoRadio.checked = true;
                    updateImage(category, selectedValue);
                }

                else if (category == "ojos_categoria"){
                    category = "ojos"; 
                    colorOjos = data.ojos_color; 
                    const ojosRadio = document.querySelector(`input[name="ojos"][value="${colorOjos}"][id="${selectedValue}"]`);
                    ojosRadio.checked = true;
                    if (colorOjos == "aplastados"){colorOjos = "ojos_aplastados"}
                    else if (colorOjos == "medios"){colorOjos = "ojos_medios"}
                    else if (colorOjos == "redondos"){colorOjos = "ojos_redondos"}
                    updateImage(colorOjos, selectedValue);

                }

                else if (category == "camiseta_categoria"){
                
                    category = "camisetas";
                    colorCamiseta = data.camiseta_color;
                    console.log("colorCamiseta:", colorCamiseta);
                    const camisetaRadio = document.querySelector(`input[name="camisetas"][value="${colorCamiseta}"][id="${selectedValue}"]`);
                    camisetaRadio.checked = true;
                    if (colorCamiseta == "manga_corta"){colorCamiseta = "camiseta_manga_corta"}
                    else if (colorCamiseta == "sudadera"){colorCamiseta = "camiseta_sudaderas"}
                    else if (colorCamiseta == "tirantes"){colorCamiseta = "camiseta_tirantes"}
                    else if (colorCamiseta == "manga_larga"){colorCamiseta = "camiseta_mangas_largas"}
                    else if (colorCamiseta == "camisas"){colorCamiseta = "camiseta_camisa"}
                    updateImage(colorCamiseta, selectedValue);
                }

                else if (category == "pelo_categoria"){
                    category = "pelos";
                    const colorPelo = data.pelo_color;
                    const peloRadio = document.querySelector(`input[name="pelos"][value="${colorPelo}"][id="${selectedValue}"]`);
                    peloRadio.checked = true;
                    updateImage(colorPelo, selectedValue);
                    
                }

                else if (category == "pantalon_categoria"){
                    category = "pantalones";
                    const colorPantalon = data.pantalon_color;
                    const pantalonRadio = document.querySelector(`input[name="pantalones"][value="${colorPantalon}"][id="${selectedValue}"]`);
                    pantalonRadio.checked = true;
                    updateImage(colorPantalon, selectedValue);
                    
                }
               
            }
        });
        }
        // Aquí puedes procesar las opciones obtenidas
    })
    .catch(error => {
        console.error('Hubo un problema con la solicitud:', error);
    });
}




document.addEventListener('DOMContentLoaded', () => {
    // llamar al método para cargar las opciones del personaje que estaba cargado en la base de datos 
    obtenerOpciones();

   
    document.getElementById('guardar').addEventListener('click', () => {

        const images = document.querySelectorAll('.image-container img');
        if (images.length === 0) {
            console.error('No se encontraron imágenes.');
            return;
        }

        const canvas = document.getElementById('combinedCanvas');
        const ctx = canvas.getContext('2d');

        // Esperar a que todas las imágenes estén cargadas
        let firstImage = images[0];

        if (!firstImage.complete) {
            console.error('La primera imagen no está cargada.');
            return;
        }

        const width = firstImage.naturalWidth;
        const height = firstImage.naturalHeight;
        canvas.width = width;
        canvas.height = height;

        // Dibujar todas las imágenes en el canvas
        images.forEach(image => {
            if (image.complete && image.naturalWidth !== 0 && image.naturalHeight !== 0) {
                ctx.drawImage(image, 0, 0, width, height);
            } else {
                console.warn('Una imagen no está completamente cargada o no tiene dimensiones válidas.');
            }
        });

        const dataURL = canvas.toDataURL('image/png');
        const base64Data = dataURL.replace(/^data:image\/(png|jpg);base64,/, '');

        fetch('/guardar_imagen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ imagen: base64Data }),
        })
        .then(response => response.json())
        .then(data => console.log('Imagen guardada correctamente', data))
        .catch(error => console.error('Error al guardar la imagen:', error));

        const resultContainer = document.getElementById('result-container');
        resultContainer.innerHTML = '';  
        const combinedImage = new Image();
        combinedImage.src = dataURL;
        resultContainer.appendChild(combinedImage);


        const opciones = getSelectedButtons();
        console.log("Las opciones que se reciben:",opciones)
        fetch('/guardar-opciones', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json', // Indica que envías datos JSON
            },
            body: JSON.stringify(opciones) // Convierte el objeto JS a JSON para enviarlo
        })
      
    
    });

    document.getElementById('continuar').addEventListener('click', () => {

        // Antes de pasar a mapa comprobar si el usuario tiene una imagen guardada  
        fetch('/obtener-imagen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'found') {
                // Si se encuentra la imagen, redirigir a /mapa
                window.location.href = "/mapa";
            } else if (data.status === 'not_found') {
                console.log("Entro aqui")
                // si no hay imagen añadir el cuerpo que se ha generado
                
                const images = document.querySelectorAll('.image-container img');
        if (images.length === 0) {
            console.error('No se encontraron imágenes.');
            return;
        }

        const canvas = document.getElementById('combinedCanvas');
        const ctx = canvas.getContext('2d');

        // Esperar a que todas las imágenes estén cargadas
        let firstImage = images[0];

        if (!firstImage.complete) {
            console.error('La primera imagen no está cargada.');
            return;
        }

        const width = firstImage.naturalWidth;
        const height = firstImage.naturalHeight;
        canvas.width = width;
        canvas.height = height;

        // Dibujar todas las imágenes en el canvas
        images.forEach(image => {
            if (image.complete && image.naturalWidth !== 0 && image.naturalHeight !== 0) {
                ctx.drawImage(image, 0, 0, width, height);
            } else {
                console.warn('Una imagen no está completamente cargada o no tiene dimensiones válidas.');
            }
        });

        const dataURL = canvas.toDataURL('image/png');
        const base64Data = dataURL.replace(/^data:image\/(png|jpg);base64,/, '');

        fetch('/guardar_imagen', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ imagen: base64Data }),
        })
        .then(response => response.json())
        .then(data => {console.log('Imagen guardada correctamente', data);
        window.location.href = "/mapa";})
        .catch(error => console.error('Error al guardar la imagen:', error));

        const resultContainer = document.getElementById('result-container');
        resultContainer.innerHTML = '';  
        const combinedImage = new Image();
        combinedImage.src = dataURL;
        resultContainer.appendChild(combinedImage);

        
            } 
        })
        .catch(error => {
            console.error('Error:', error);
        });
    
       
    
       
    });

    document.getElementById('reestablecer').addEventListener('click', () => { 

        categories = ["body_type", "ojos", "gafas", "bocas", "camisetas", "pelos", "zapatillas", "accesorios", "pantalones"]

        
        categories.forEach((category) => {
            const radioButtons = document.querySelectorAll(`input[name="${category}"]`);
            radioButtons.forEach((radio) => {
                radio.checked = false;  // Desmarcar el radio
                radio.dataset.wasChecked = 'false';  // Reiniciar el estado
                updateImage(radio.dataset.category, null);  // Eliminar la imagen
            });
        });

        selectFirstBody();




    });
    
});
