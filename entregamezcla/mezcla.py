from collections import defaultdict
import eventlet
eventlet.monkey_patch()

from flask import Flask, render_template, redirect, request, session, url_for , jsonify
from flask_oauthlib.client import OAuth
from flask_session import Session
from faker import Faker
import spotipy
import mysql.connector
import requests
import json
import base64
from spotipy.oauth2 import SpotifyOAuth
from flask_socketio import SocketIO, emit, join_room, leave_room

app = Flask(__name__)
# Configuración de la clave secreta
app.secret_key = 'mi_clave_secreta_super_segura'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
socketio = SocketIO(app)

##active_songs = []
connected_users = set()
chat_conexions = {}
## por cada connected user quiero que haya un diccionario donde se almacene que cancion esta escuchando esa persona
personas = []
imagenes = [] 
message_history = {}
pending_messages = {}

tokens = {}

active_chats = {}
chats = defaultdict(list) 

CLIENT_ID = '78050eff52214768b3b663c4ed5ca7d1'
CLIENT_SECRET = '93ac17d42d3441ada7cfd98345ef5c42'
REDIRECT_URI = 'http://34.76.63.35/callback'


# Configuración de la base de datos
db_config = {
    'user': 'mai',
    'password': 'calavera',
    'host': 'db',
    'database': 'SpotifusNueva',
    'port': '3306'
}

def insertar_usuarios(num_users):
    fake = Faker()
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        for _ in range(int(num_users)):
            nombre = fake.name()
            contrasena = fake.password()
            query = "INSERT INTO Usuarios(nombre, contrasena) VALUES (%s, %s)"
            cursor.execute(query, (nombre, contrasena))
        conn.commit()

def get_usuarios():
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "SELECT nombre, ruta_imagen FROM Usuarios"
        cursor.execute(query)
        users = cursor.fetchall()
    return users

# Funciones para manipular usuarios en la base de datos

## insertar un nuevo usuario en la base de datos
def insertar_usuario(nombre, contrasena, imagen):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        # Verificar si el usuario ya existe
        query = "SELECT COUNT(*) FROM Usuarios WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        count = cursor.fetchone()[0]
        # Si el usuario no existe, insertarlo
        if count == 0:
            if (imagen == ""):
                imagen = "https://img.pokemondb.net/sprites/bank/normal/tangela.png"
                query = "INSERT INTO Usuarios(nombre, contrasena, ruta_imagen) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, contrasena, imagen))
                conn.commit()

##eliminar los usuarios que están añadidos en la base de datos
def eliminar_usuarios():
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM Usuarios"
        cursor.execute(query)
        conn.commit()

## insertar la imagen que se ha elegido en la ventana de personalizacion
def insertar_imagen(nombre_usuario, imagen):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "UPDATE Usuarios SET ruta_imagen = %s WHERE nombre = %s"
        cursor.execute(query, (imagen, nombre_usuario))
        conn.commit()

## método que devuelve la imagen asociada al usuario 
def obtener_imagen(id):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "SELECT ruta_imagen FROM Usuarios WHERE nombre = %s"
        cursor.execute(query,(id,))
        imagen = cursor.fetchall()
    return imagen

## método para insertar los mensajes en la base de datos  
def insertar_mensaje(room_name, username, message):
    with mysql.connector.connect(**db_config) as conn: 
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensajes (room_name, username, message) VALUES (%s, %s, %s)", (room_name, username, message))
        conn.commit()

## método para obtener los mensajes de la room de dos usuarios 
def cargar_mensajes(room_name):
    with mysql.connector.connect(**db_config) as conn: 
        cursor = conn.cursor()
        cursor.execute("SELECT username, message FROM mensajes WHERE room_name = %s", (room_name,))
        mensajes = cursor.fetchall()
    return mensajes 

def obtener_rooms(user_id):
    with mysql.connector.connect(**db_config) as conn: 
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT room_name FROM mensajes WHERE room_name LIKE %s", (f"%{user_id}%",))
        rooms = cursor.fetchall()
    return rooms


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/menu')
def menu():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    scope = 'user-read-currently-playing user-read-playback-state user-top-read user-library-read'
    auth_url = 'https://accounts.spotify.com/authorize'
    response_type = 'code'
    
    auth_request_url = f'{auth_url}?client_id={CLIENT_ID}&response_type={response_type}&redirect_uri={REDIRECT_URI}&scope={scope}'
    return redirect(auth_request_url)

@app.route('/callback')
def callback():
    code = request.args.get('code')
    token_url = 'https://accounts.spotify.com/api/token'
    
    headers = {
        'Authorization': 'Basic ' + base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode()
    }
    data = {
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': REDIRECT_URI
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    response_data = response.json()
    
    session['access_token'] = response_data['access_token']
    return redirect(url_for('profile'))


@app.route('/profile')
def profile():
    access_token = session.get('access_token')
    if not access_token:
        return redirect(url_for('login'))
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    
    # Obtener información del usuario
    profile_url2 = 'https://api.spotify.com/v1/me'
    response2 = requests.get(profile_url2, headers=headers)
    response_data2 = response2.json()
    
    # Guardar información del usuario
    insertar_usuario(response_data2['id'], "contraseña", "")
    
    unico = response_data2['id']
    tokens[unico] = session.get('access_token')
    usuario = response_data2['display_name']

    session['id'] = unico
    session['usuario'] = usuario
    
    # Inicializar variables para track y artist
    track = None
    artist = None
    
    # Verificar la canción actual
    profile_url = 'https://api.spotify.com/v1/me/player/currently-playing'
    response = requests.get(profile_url, headers=headers)
    
    try:
        response_data = response.json()
        app.logger.debug(f'Response JSON: {response_data}')
    except json.JSONDecodeError as e:
        app.logger.error(f'Error decoding JSON: {e}')
        app.logger.debug(f'Response content: {response.text}')
        return render_template('menu.html', track=None, artist=None, error="Failed to decode response")
    
    if response.status_code != 204 and 'item' in response_data:
        track = response_data['item']['name']
        artist = response_data['item']['artists'][0]['name']
    else:
        # Si no hay canción en reproducción, verifique el estado de reproducción
        state_url = 'https://api.spotify.com/v1/me/player'
        state_response = requests.get(state_url, headers=headers)
        
        try:
            state_data = state_response.json()
            app.logger.debug(f'Playback state JSON: {state_data}')
        except json.JSONDecodeError as e:
            app.logger.error(f'Error decoding JSON: {e}')
            app.logger.debug(f'Playback state response content: {state_response.text}')
            return render_template('menu.html', track=None, artist=None, error="Failed to decode playback state response")
        
        if state_response.status_code != 204 and 'item' in state_data:
            track = state_data['item']['name']
            artist = state_data['item']['artists'][0]['name']
        else:
            return render_template('menu.html', track=None, artist=None, error="No song currently playing")
    
    # Guardar en la sesión la información correspondiente con el usuario

    session['track'] = track
    session['artist'] = artist
    
    return render_template('menu.html', track=track, artist=artist, usuario=usuario, unico=unico, error=None)

@app.route('/personalizacion', methods=['GET', 'POST'])
def personalizacion():
    if request.method == 'POST':
        track = request.form.get('track')
        artist = request.form.get('artist')
        usuario = request.form.get('usuario')
        unico = request.form.get('unico')
        
        # Aquí puedes procesar y utilizar los datos según tus necesidades
        return render_template('personalizacion.html', track=track, artist=artist, usuario=usuario,unico=unico)

    # Si es una solicitud GET, simplemente renderizar la página de personalización
    return render_template('personalización.html', track=track, artist=artist, usuario=usuario, unico=unico)


@app.route('/insertar_imagen', methods=['POST'])
def insertar_imagen_endpoint():
    data = request.get_json()
    nombre = data['unico']
    imagen = data['src']
    insertar_imagen(nombre,imagen)
    return jsonify({'status': 'success'})

@app.route('/pagina3')
def pagina3():
    ##insertar_usuarios(4)
    ##eliminar_usuarios()
    usuarios = get_usuarios()
    return render_template('pagina3.html', lista_elementos=usuarios)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/prueba')
def prueba():
    return render_template('prueba.html')

@app.route('/tiemporeal')
def tiemporeal():
    return render_template('tiemporeal.html')

@app.route('/personajes')
def personajes():
    return render_template('personajes.html')

# Manejar el evento de nueva canción
##@socketio.on('new_song')
##def handle_new_song(json):
  ##  app.logger.info(f'Received new song: {json}')
    ##active_songs.append(json)
    ##emit('new_song', json, broadcast=True)

## En vez de añadir un id unico que tiene cada sesion abierta , lo que hay que añadir es el personaje 
## que ese usuario haya escogido para que le represente en el mapa. 


@socketio.on('connect')
def handle_connect(auth=None):
    connected_users.add(session.get('id'))
    chat_conexions[session.get('id')] = request.sid
    usuario = session.get('usuario')
    img = obtener_imagen(session.get('id'))
    new_dic2 = {'id': session.get('id'),'usuario': usuario, 'imagen' : img, 'track': session.get('track'), 'artist': session.get('artist')}
    imagenes.append(new_dic2)
    emit('update_user_list', list(imagenes), broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    connected_users.discard(session.get('id'))
    if session.get('id') in chat_conexions:
        del chat_conexions[session.get('id')]
    global imagenes
    imagenes = [imagen for imagen in imagenes if imagen['id'] != session.get('id')]
    emit('update_user_list', list(imagenes), broadcast=True)
    
@socketio.on('send_message')
def handle_send_message(data):
    user_id = data['userId']  # ID del destinatario
    message = data['message']
    username = session.get('usuario')  # Nombre del remitente

    # Crear una sala única para el par de usuarios
    room_name = f"{min(session.get('id'), user_id)}_{max(session.get('id'), user_id)}"
    emit('mostrarNombre',room_name)


    # Guardar en la base de datos
    insertar_mensaje(room_name, username, message)
    
    # Enviar el mensaje solo al destinatario
    emit('receive_message', {'userId': session.get('id'), 'username': username, 'message': message}, room=chat_conexions.get(user_id))

    # Opcional: si quieres reenviar el mensaje al remitente para tener control adicional,
    # puedes emitir a la propia conexión del remitente también.
@socketio.on('start_chat')
def handle_start_chat(data):
    user_id = data['userId']
    room_name = f"{min(session.get('id'), user_id)}_{max(session.get('id'), user_id)}"

    # Unir al usuario que inicia el chat a la sala
    join_room(room_name)

    # Cargar los mensajes correspondientes con esa room de usuarios 
    mensajes = cargar_mensajes(room_name)
    
    # Emitir los mensajes antiguos al room
    for mensaje in mensajes: 
        emit('receive_message', {'userId': session.get('id'), 'username': mensaje[0], 'message': mensaje[1]}, room=room_name)

@socketio.on('get_chat_list')
def handle_chat_list():
    user_id = session.get('id')
    rooms = obtener_rooms(user_id)

    user_chats = {}
    for room in rooms:
        room_name = room[0]
        other_user_id = room_name.split('_')
        other_user_id.remove(user_id)
        other_user_id = other_user_id[0]

        user_chats[other_user_id] = []
    
    emit('chat_list', user_chats)

@socketio.on('canciones_mas_escuchadas')
def handle_canciones_mas_escuchadas(data):
    periodos = ['long_term', 'medium_term', 'short_term']
    
    track = None
    # Iteramos sobre todos los periodos para ambos usuarios
    for periodo1 in periodos:  # Para el destinatario
        lista1 = calcularLista("destinatario", periodo1, data)
        
        for periodo2 in periodos:  # Para el remitente
            lista2 = calcularLista("remitente", periodo2, None)
            
            # Método que devuelve si hay alguna coincidencia en canciones
            track = comprobarCoincidencia(lista1, lista2)
            
            if track:
                break  # Si se encuentra una coincidencia, detener el bucle externo
        if track:
            break  # Detener si ya se ha encontrado coincidencia
    if track is None:
        ## comprobar en canciones guardadas , las ultimas 50 solo por el momento 

        r1 = comprobarCancionesGuardadas(data)
        r2 = comprobarCancionesGuardadas(None)

        emit('imprimir', r1)
        emit('imprimir', r2)

        guardada = comprobarCoincidencia(r1,r2)

        
        if guardada is None:
           emit('track', {'status': 'no_match', 'message': 'No tienen ninguna canción en común.'})
        else:
            emit('track', {
            'status': 'match',
            'name': guardada['name'],
            'artist': guardada['artist'],
            'image_url': guardada['image_url']})
   
    else:
        emit('track', {
            'status': 'match',
            'name': track['name'],
            'artist': track['artist'],
            'image_url': track['image_url']})
    
    
    #emit('canciones', {'access_token':lista1, 'otro_access_token': lista2})   

def comprobarCancionesGuardadas(data):
    if data:
      access_token = tokens.get(data)
    else:
      access_token = session.get('access_token')

    params = {
      'limit': request.args.get('limit', default=50, type=int),
      'offset': request.args.get('offset', default=0)  # Corrige el error tipográfico
    }

    headers = {
      'Authorization': f'Bearer {access_token}'
    }

    profile_url = 'https://api.spotify.com/v1/me/tracks'

    response = requests.get(profile_url, headers=headers, params=params)

# Convertimos la respuesta a JSON
    response_json = response.json()

    lista = []

    canciones_guardadas = response_json['items']

    for item in canciones_guardadas:
       track = item.get('track', {})  # Asegúrate de que 'track' esté presente
       album_info = track.get('album', {})
    
    # Manejo seguro de la URL de la imagen del álbum
       image_url = album_info.get('images', [{'url': 'default_image_url'}])[0]['url']
    
    # El primer artista en la lista de artistas
       artist_name = track['artists'][0]['name'] if track.get('artists') else 'Unknown Artist'
    
    # Añadir a la lista
       lista.append({
        'name': track.get('name', 'Unknown Track'),
        'artist': artist_name,
        'image_url': image_url,
        'id': track.get('id')
       })

# Devuelve la lista procesada
    return lista


    

def calcularLista(quien, tiempo, data):
    
    if quien == "destinatario":

        access_token = tokens.get(data)

    else:
        access_token = session.get('access_token')

    params = {
    'limit': request.args.get('limit', default=50, type=int),
    'time_range': request.args.get('time_range', default=tiempo)
    }
    
    headers = {
        'Authorization': f'Bearer {access_token}'
    }
    profile_url = 'https://api.spotify.com/v1/me/top/tracks'
    
    response = requests.get(profile_url, headers=headers, params=params)

    response = response.json()
    
    artistas = response['items']
    lista = []

    for artista in artistas: 
        image_url = artista['album']['images'][0]['url'] if artista['album']['images'] else 'default_image_url'
        
        # El primer artista en la lista de artistas
        artist_name = artista['artists'][0]['name'] if artista['artists'] else 'Unknown Artist'
        
        lista.append({
            'name': artista['name'],
            'artist': artist_name,
            'image_url': image_url,
            'id': artista['id']
        })
    
    return lista


def comprobarCoincidencia(lista1,lista2):
     for track in lista1: 
            for track2 in lista2:
                if track['id'] == track2['id']: 
                    coincidencia = True
                    return track
                

# Ejecución de la aplicación
if __name__ == '__main__':
    ##app.run(debug=True, host='0.0.0.0')
    socketio.run(app, debug=True, host='0.0.0.0')
