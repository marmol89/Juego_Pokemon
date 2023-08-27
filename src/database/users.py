from src.database.db import db
import hashlib

class users:
    salt = 'patata'

    def __init__(self):
        self.dbp = db().mydb
    
    def cifrar_contrasena(self,contrasena):
        contrasena_codificada = contrasena.encode('utf-8')
        hashed = hashlib.pbkdf2_hmac('sha256', contrasena_codificada, self.salt, 100000)
        return hashed
    
    def verificar_contrasena(self , contrasena, hashed):
        contrasena_codificada = contrasena.encode('utf-8')
        nuevo_hash = hashlib.pbkdf2_hmac('sha256', contrasena_codificada, self.salt, 100000)
        return nuevo_hash == hashed
    