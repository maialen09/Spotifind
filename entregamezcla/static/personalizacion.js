// personalizacion.js

// Lista de imágenes y sus enlaces correspondientes
const characters = [

    {
        link: "https://pokemondb.net/pokedex/grafaiai", 
        image: "https://img.pokemondb.net/sprites/scarlet-violet/normal/grafaiai.png",
        alt:"Grafaiai"
        
    }
    ,
    { 
        link: "https://pokemondb.net/pokedex/tandemaus",
        image: "https://img.pokemondb.net/sprites/scarlet-violet/normal/tandemaus.png",
        alt: "Tandemaus"
    },
    { 
        link: "https://pokemondb.net/pokedex/finizenu",
        image: "https://img.pokemondb.net/sprites/scarlet-violet/normal/finizen.png",
        alt: "Finizen"
    },
    { 
        link: "https://pokemondb.net/pokedex/capsakid",
        image: "https://img.pokemondb.net/sprites/scarlet-violet/normal/capsakid.png",
        alt: "Capsakid"
    }
    
];

let currentIndex = 0;

// Elementos del DOM
const prevButton = document.getElementById('prev');
const nextButton = document.getElementById('next');
const characterLink = document.getElementById('character-link');
const characterImage = document.getElementById('character-image');
const aleatorioButton = document.getElementById('aleatorio');
const guardarButton = document.getElementById('guardar');

// Función para actualizar la imagen y el enlace
function updateCharacter(index) {
    characterLink.href = characters[index].link;
    characterImage.src = characters[index].image;
    characterImage.alt = characters[index].alt;
}

// Event listeners para los botones
prevButton.addEventListener('click', () => {
    currentIndex = (currentIndex - 1 + characters.length) % characters.length;
    updateCharacter(currentIndex);
});

nextButton.addEventListener('click', () => {
    currentIndex = (currentIndex + 1) % characters.length;
    updateCharacter(currentIndex);
});


// Al pulsar guardar la imagen , que se guarde en la base de datos , para ese usuario. 
guardarButton.addEventListener('click', () => {

    // aqui lo que hay que hacer será obtener la foto que ha pulsado y guardarla en la base de datos donde el nombre de usuario de spotify
    const src = characterImage.getAttribute('src');

    console.log(src);

    var unicoParagraph = document.getElementById("unico-paragraph");

    var texto = unicoParagraph.textContent;

    var unico = texto.replace("Id unico: ", "").trim();


    fetch('/insertar_imagen', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ unico, src }),
    })
    .then(response => response.json())
    .then(data => {
        console.log('Success:', data);
    })
    .catch((error) => {
        console.error('Error:', error);
    });



});

// Inicializar con la primera imagen
updateCharacter(currentIndex);

