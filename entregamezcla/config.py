import os

class Config:
    SECRET_KEY = 'mi_clave_secreta_super_segura'
    SESSION_TYPE = 'filesystem'

    # Configuración de la base de datos
    DB_CONFIG = {
        'user': 'mai',
        'password': 'calavera',
        'host': 'db',
        'database': 'Spotifind',
        'port': '3306'
    }

    # Otras configuraciones
    CLIENT_ID = '78050eff52214768b3b663c4ed5ca7d1'
    CLIENT_SECRET = '93ac17d42d3441ada7cfd98345ef5c42'
    REDIRECT_URI ='http://35.205.145.118/callback'
