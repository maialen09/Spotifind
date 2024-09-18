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

// los radio button no gestionan el quitar el click asi que hay que hacerlo manualmente 
function handleRadioClick(event){

    if (this.dataset.wasChecked == 'true'){
        this.checked = false;
        this.dataset.wasChecked = 'false';
        updateImage(this.dataset.category, null);
    }
    else{
        this.checked = true; 
        this.dataset.wasChecked = 'true'; 
        updateImage(this.dataset.category, this.id);
    }

    const radioButtons = document.querySelectorAll(`input[name="${this.name}"]`);
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

const radiosGafas = document.querySelectorAll('input[name="gafas"]');
radiosGafas.forEach((radio) => {
    //radio.addEventListener('change', function() {
        
      //  if (this.value == "cuadradas"){
            
        //    updateImage('gafas_rectangulares', this.id);
       // }
        //else{
          //  updateImage('gafas_redondas', this.id);
        //}
        
    //});

    if (radio.value == "cuadradas"){
        radio.dataset.category = 'gafas_rectangulares';
        radio.addEventListener('click', handleRadioClick);
    }

    else{
        radio.dataset.category = 'gafas_redondas';
        radio.addEventListener('click', handleRadioClick);
    }
});

const radiosOjos = document.querySelectorAll('input[name="ojos"]');
radiosOjos.forEach((radio) => {
    //radio.addEventListener('change', function() {
        //updateImage('ojos', this.id);
    //});
    radio.dataset.category = 'ojos';
    radio.addEventListener('click', handleRadioClick);
});

const radiosVestidos = document.querySelectorAll('input[name="vestidos"]');
radiosVestidos.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('vestidos', this.id);
    //});

    radio.dataset.category = 'vestidos';
    radio.addEventListener('click', handleRadioClick);
});

const radiosBocas = document.querySelectorAll('input[name="bocas"]');
radiosBocas.forEach((radio) => {
    //radio.addEventListener('change', function() {
      //  updateImage('bocas', this.id);
    //});

    radio.dataset.category = 'bocas';
    radio.addEventListener('click', handleRadioClick);
});