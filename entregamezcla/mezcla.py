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
from threading import Thread 
from flask_cors import CORS
import time

app = Flask(__name__)
# Configuración de la clave secreta
app.secret_key = 'mi_clave_secreta_super_segura'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
cors = CORS(app, resources={r"/*": {"origins": "https://mt.spotifind.eus"}})


##socketio = SocketIO(app, cors_allowed_origins="https://mt.spotifind.eus")
socketio = SocketIO(app, cors_allowed_origins="https://mt.spotifind.eus")

##active_songs = []
connected_users = set()
chat_conexions = {}
## por cada connected user quiero que haya un diccionario donde se almacene que cancion esta escuchando esa persona
personas = []
imagenes = [] 
message_history = {}
pending_messages = {}
user_locations = {} ## para poder guardar las ubicaciones

tokens = {}

active_chats = {}
chats = defaultdict(list) 

CLIENT_ID = '78050eff52214768b3b663c4ed5ca7d1'
CLIENT_SECRET = '93ac17d42d3441ada7cfd98345ef5c42'
REDIRECT_URI = 'http://35.205.145.118/callback'


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
        query = "SELECT nombre FROM Usuarios"
        cursor.execute(query)
        users = cursor.fetchall()
    return users

# Funciones para manipular usuarios en la base de datos

## insertar un nuevo usuario en la base de datos
def insertar_usuario(nombre, contrasena, imagen, display_name):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        # Verificar si el usuario ya existe
        query = "SELECT COUNT(*) FROM Usuarios WHERE nombre = %s"
        cursor.execute(query, (nombre,))
        count = cursor.fetchone()[0]
        # Si el usuario no existe, insertarlo
        if count == 0:
            if (imagen == ""):
                #imagen = "https://img.pokemondb.net/sprites/bank/normal/tangela.png"
                query = "INSERT INTO Usuarios(nombre, contrasena, display_name) VALUES (%s, %s, %s)"
                cursor.execute(query, (nombre, contrasena, display_name))
                conn.commit()

##eliminar los usuarios que están añadidos en la base de datos
def eliminar_usuarios():
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM Usuarios"
        cursor.execute(query)
        conn.commit()

## eliminar un usuario en concreto
def eliminar_usuario(user_id):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        query = "DELETE FROM Usuarios WHERE nombre = %s"
        cursor.execute(query,(user_id,))
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
def insertar_mensaje(room_name, username, message, user_id):
    with mysql.connector.connect(**db_config) as conn: 
        cursor = conn.cursor()
        cursor.execute("INSERT INTO mensajes (room_name, username, message,user_id) VALUES (%s, %s, %s, %s)", (room_name, username, message, user_id))
        conn.commit()

## método para obtener los mensajes de la room de dos usuarios 
def cargar_mensajes(room_name):
    with mysql.connector.connect(**db_config) as conn: 
        cursor = conn.cursor()
        cursor.execute("SELECT username, message, user_id FROM mensajes WHERE room_name = %s", (room_name,))
        mensajes = cursor.fetchall()
    return mensajes 

def obtener_rooms(user_id):
    with mysql.connector.connect(**db_config) as conn: 
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT room_name FROM mensajes WHERE room_name LIKE %s", (f"%{user_id}%",))
        rooms = cursor.fetchall()
    return rooms

def obtener_chats_usuarios(user_id):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT DISTINCT room_name FROM mensajes WHERE user_id = %s", (user_id,))
        chats = cursor.fetchall()
    return chats

def guardar_opciones(data, user_id):
    cuerpo_info = data.get('body_type', {})
    cuerpo_categoria = list(cuerpo_info.keys())[0] if cuerpo_info else None

    ojos_info = data.get('ojos', {})
    ojos_categoria = list(ojos_info.keys())[0] if ojos_info else None
    ojos_color = ojos_info.get(ojos_categoria, None) if ojos_categoria else None

    camiseta_info = data.get('camisetas', {})
    camiseta_categoria = list(camiseta_info.keys())[0] if camiseta_info else None
    camiseta_color = camiseta_info.get(camiseta_categoria, None) if camiseta_categoria else None

    boca_info = data.get('bocas', {})
    boca = list(boca_info.keys())[0] if boca_info else None



    gafas_info = data.get('gafas', {})
    gafas = list(gafas_info.keys())[0] if gafas_info else None


    pelo_info = data.get('pelos', {})
    pelo_categoria = list(pelo_info.keys())[0] if pelo_info else None
    pelo_color = pelo_info.get(pelo_categoria, None) if pelo_categoria else None

    pantalones_info = data.get('pantalones', {})
    pantalones_categoria = list(pantalones_info.keys())[0] if pantalones_info else None
    pantalones_color = pantalones_info.get(pantalones_categoria, None) if pantalones_categoria else None

    zapatillas_info = data.get('zapatillas', {})
    zapatillas = list(zapatillas_info.keys())[0] if zapatillas_info else None


    accesorio_info = data.get('accesorios', {})
    accesorio = list(accesorio_info.keys())[0] if accesorio_info else None


    # Consulta SQL para insertar o actualizar
    query = """
        INSERT INTO Opciones (user_id, cuerpo_categoria, ojos_color, ojos_categoria, camiseta_color, camiseta_categoria, 
                               boca, gafas, pelo_color, pelo_categoria, pantalones_categoria, 
                               pantalones_color, zapatillas, accesorio) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE 
            cuerpo_categoria = VALUES(cuerpo_categoria),
            ojos_color = VALUES(ojos_color),
            ojos_categoria = VALUES(ojos_categoria),
            camiseta_color = VALUES(camiseta_color),
            camiseta_categoria = VALUES(camiseta_categoria),
            boca = VALUES(boca),
            gafas = VALUES(gafas),
            pelo_color = VALUES(pelo_color),
            pelo_categoria = VALUES(pelo_categoria),
            pantalones_categoria = VALUES(pantalones_categoria),
            pantalones_color = VALUES(pantalones_color),
            zapatillas = VALUES(zapatillas),
            accesorio = VALUES(accesorio)
    """

    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        cursor.execute(query, (
            user_id, 
            cuerpo_categoria, 
            ojos_color,  # Este estaba en la posición incorrecta
            ojos_categoria,
            camiseta_color,
            camiseta_categoria, 
            boca, 
            gafas, 
            pelo_color,
            pelo_categoria, 
            pantalones_categoria, 
            pantalones_color, 
            zapatillas, 
            accesorio
        ))
        conn.commit()

## método que devuelve las opciones de personaje que ha guardado el usuario 
def obtener_opciones(user_id):
    with mysql.connector.connect(**db_config) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Opciones WHERE user_id = %s", (user_id,))
        opciones = cursor.fetchall()
    return opciones
 



def actualizar_cancion_periodicamente():
    while True:
        with app.app_context():
            for user_id in connected_users: 
                access_token = tokens.get(user_id)
                if access_token:
                    headers= {
                        'Authorization': f'Bearer {access_token}'
                    }
                    profile_url = 'https://api.spotify.com/v1/me/player/currently-playing'
                    response = requests.get(profile_url, headers=headers)
                    if response.status_code == 200:
                        response_data = response.json()
                        if 'item' in response_data:
                            track = response_data['item']['name']
                            artist = response_data['item']['artists'][0]['name']

                           
                            
                            # Emitir la actualización de la canción
                            socketio.emit('song_update', {
                                'user_id': user_id,
                                'track': track,
                                'artist': artist
                            })
        time.sleep(120)

@app.route('/api/opciones', methods=['GET'])
def obtener_opciones_ruta():
    user_id = session.get('id')
    opciones = obtener_opciones(user_id)

    opciones_list = []
    for opcion in opciones:
            opciones_dict = {
                'user_id': opcion[0],  # Ajusta según el índice
                'cuerpo_categoria': opcion[1],
                'ojos_color': opcion[2],
                'ojos_categoria': opcion[3],
                'camiseta_color': opcion[4],
                'camiseta_categoria': opcion[5],
                'boca': opcion[6],
                'gafas': opcion[7],
                'pelo_color': opcion[8],
                'pelo_categoria': opcion[9],
                'pantalones_categoria': opcion[10],
                'pantalones_color': opcion[11],
                'zapatillas': opcion[12],
                'accesorio': opcion[13]
            }
            opciones_list.append(opciones_dict)
            
    return jsonify(opciones_list)


@app.route('/obtener-imagen', methods=['POST'])
def obtener_imagen_ruta():
    user_id = session.get('id')  # Obtener el ID del usuario desde la sesión
    if not user_id:
        return jsonify({'imagen': None, 'status': 'no_session'})  # Si no hay sesión
    
    img = obtener_imagen(user_id)  # Asegúrate de que esta función devuelva una lista

    if img is not None:
        img_1 = img[0]  
        if img_1 and img_1[-1] is not None:  # Verifica que img_1 y su último elemento no sean None
            img_base64 = base64.b64encode(img_1[-1]).decode('utf-8')
            return jsonify({'imagen': img_base64, 'status': 'found'})  # Imagen encontrada
        else:
            return jsonify({'imagen': None, 'status': 'not_found'})  # Imagen no encontrada
    else:
        return jsonify({'imagen': None, 'status': 'not_found'})  # Imagen no encontrada

@app.route('/guardar-opciones', methods=['POST'])
def guardar_opciones_ruta():
    user_id = session.get('id')
    data = request.get_json()
    guardar_opciones(data, user_id)
    return "Opciones guardadas", 200

@app.route('/eliminar_usuario', methods=['POST'])
def eliminar_usuario_ruta():
    user_id = request.json['user_id']
    print("El usuario es :", user_id)
    eliminar_usuario(user_id)
    return jsonify({"message": f"Usuario {user_id} eliminado correctamente."})  
    

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/personajes')
def personajes():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    scope = 'user-read-currently-playing user-read-playback-state user-top-read user-library-read user-follow-read'
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
    insertar_usuario(response_data2['id'], "contraseña", "", response_data2['display_name'])
    
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
        return render_template('personajes.html', track=None, artist=None, error="Failed to decode response")
    
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
            return render_template('personajes.html', track=None, artist=None, error="Failed to decode playback state response")
        
        if state_response.status_code != 204 and 'item' in state_data:
            track = state_data['item']['name']
            artist = state_data['item']['artists'][0]['name']
        else:
            return render_template('personajes.html', track=None, artist=None, error="No song currently playing")
    
    # Guardar en la sesión la información correspondiente con el usuario

    session['track'] = track
    session['artist'] = artist
    
    return render_template('personajes.html', track=track, artist=artist, usuario=usuario, unico=unico, error=None)

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
    usuarios = [usuario[0] for usuario in usuarios] ## para no mandar el nombre de los usuarios con comas , ya que se reciben como tuplas
    return render_template('pagina3.html', lista_elementos=usuarios)

@app.route('/mapa')
def mapa():
    return render_template('mapa.html')

@app.route('/administrador')
def administrador():
    return render_template('administrador.html')

@app.route('/prueba')
def prueba():
    return render_template('prueba.html')

@app.route('/tiemporeal')
def tiemporeal():
    return render_template('tiemporeal.html')

@app.route('/menu')
def menu():
    
    return render_template('menu.html')


@app.route('/guardar_imagen', methods=['POST'])
def guardar_imagen():
    data = request.get_json()
    
    # Obtener el nombre del usuario y la imagen en base64
    imagen_base64 = data['imagen']
    
    # Decodificar la imagen base64 a binario
    imagen_binaria = base64.b64decode(imagen_base64)

    # Insertar en la base de datos (puedes ajustar para recibir también el nombre del usuario)
    insertar_imagen(session.get('id'), imagen_binaria)

    return jsonify({'mensaje': 'Imagen guardada correctamente'}), 200

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
    if not any(imagen['id'] == session.get('id') for imagen in imagenes):
            usuario = session.get('usuario')
            img = obtener_imagen(session.get('id'))
            img_1 = img[0]  
            img_base64 = base64.b64encode(img_1[-1]).decode('utf-8')
            session['imagen'] = img_base64   
            new_dic2 = {'id': session.get('id'),'usuario': usuario, 'imagen' : img_base64, 'track': session.get('track'), 'artist': session.get('artist')}
            imagenes.append(new_dic2)
            emit('update_user_list', list(imagenes), broadcast=True)
           

@socketio.on('disconnect')
def handle_disconnect():
    connected_users.discard(session.get('id'))
    if session.get('id') in chat_conexions:
        del chat_conexions[session.get('id')]
    global imagenes
    imagenes = [imagen for imagen in imagenes if imagen['id'] != session.get('id')]

    emit('imprimir', user_locations)
    user_id = session.get('id') 
    if user_id in user_locations:
        del user_locations[user_id]
    emit('remove_user_location', session.get('id'), broadcast=True)
    emit('update_user_list', list(imagenes), broadcast=True)
  
@socketio.on('user-location')
def handle_user_location(location):
        user_id = session.get('id')
        user_locations[user_id] = {

            'userId' : user_id,
            'lat': location['lat'],
            'lng': location['lng'],
            'img': session.get('imagen'),
            'username': session.get('usuario'),
            'song': session.get('track'),
            'artist': session.get('artist')
        }
        
        emit('update_user_locations', list(user_locations.values()), to=request.sid)
        emit('new_user_location', user_locations[user_id], broadcast=True)

@socketio.on('get_user_id')
def handle_get_user_id():
    user_id = session.get('id')  # Obtener el ID del usuario desde la sesión
    emit('receive_user_id', user_id)  # Enviar el ID al cliente

@socketio.on('join_room')
def handle_join_room(data):
    room_name = data['room_name']
    join_room(room_name)
    emit('system_message', f"{session.get('usuario')} se ha unido a la sala {room_name}", room=room_name)

@socketio.on('send_message')
def handle_send_message(data):
    room_name = data['room_name']
    message = data['message']
    username = session.get('usuario')  # Obtiene el nombre del usuario desde la sesión
    user_id = session.get('id')

    # Insertar el mensaje en la base de datos
    insertar_mensaje(room_name,username,message, user_id)

    # Emitir el mensaje a todos en la sala
    emit('receive_message', {
        'room_name': room_name,
        'username': username,
        'message': message,
        'user_id': user_id
    }, room=room_name)

@socketio.on('load_chat_history')
def handle_load_chat_history(room_name):
    messages = cargar_mensajes(room_name)

    emit('imprimir', messages)

    # Enviar el historial de chat al cliente
    emit('chat_history', {
        'room_name': room_name,
        'messages': messages
    })

@socketio.on('load_user_chats')
def load_user_chats():
    user_id = session.get('id')  
    salas = obtener_chats_usuarios(user_id)

    # Enviar la lista de salas al cliente
    emit('user_chats', {'rooms': [sala[0] for sala in salas]})


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

        r1 = comprobarCancionesGuardadas(data) ## lista de canciones guardadas 1
        r2 = comprobarCancionesGuardadas(None) ## lista de canciones guardadas 2 

        ## comprueba si coincide alguna de las canciones guardadas con alguna de las otras canciones guardadas
        guardada = comprobarCoincidencia(r1,r2)

        
        if guardada is None:
           ## deberia comprobar si alguna de las canciones guardadas coincide con alguna de las canciones más oidas
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

@socketio.on('cantante_en_comun')
def handle_cantante_en_comun(data):
    
    periodos = ['long_term', 'medium_term', 'short_term']
    artist = None

    for periodo1 in periodos:
        lista1 = calcularArtista("destinatario", periodo1,data)
        for periodo2 in periodos: 
            lista2 = calcularArtista("remitente", periodo2, data)
            artist = comprobarCoincidencia(lista1,lista2)
            if artist:
                break
        if artist:
            break
    

    if artist is None:
         ## mirar en los cantantes que siguen a ver si hay alguno en comun 
         emit('track', {'status': 'no_match', 'message': 'No tienen ningun cantante en común.'})
    else:
        emit('artist', {
            'status': 'match',
            'name': artist['name'],
            'image_url': artist['image_url']})


def calcularArtista(quien, tiempo, data):
    
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
    profile_url = 'https://api.spotify.com/v1/me/top/artists'
    
    response = requests.get(profile_url, headers=headers, params=params)

    response = response.json()
    
    artistas = response['items']
    lista = []

    for artista in artistas: 
        image_url = artista['images'][0]['url'] if artista['images'] else 'default_image_url'
        
        # El primer artista en la lista de artistas
        artist_name = artista['name'] if artista['name'] else 'Unknown Artist'
        
        lista.append({
            'name': artist_name,
            'image_url': image_url,
            'id': artista['id']
        })
    
    return lista


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
    thread = Thread(target=actualizar_cancion_periodicamente)
    thread.start()

    socketio.run(app, debug=True, host='0.0.0.0')
