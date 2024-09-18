document.addEventListener("DOMContentLoaded", function() {
    const socket = io.connect('http://' + window.location.hostname + ':' + window.location.port);
    const songsList = document.getElementById('lista');

    socket.on('new_song', function(data) {
        const li = document.createElement('li');
        li.textContent = `${data.usuario} está escuchando ${data.track} de ${data.artist}`;
        songsList.appendChild(li);
    });

    function sendNewSong(song) {
        socket.emit('new_song', song);
    }
});