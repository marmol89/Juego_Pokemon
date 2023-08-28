from src.database.db import db
from src.user import user
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
    
    def verificarUser(self , username):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM users WHERE username = '%s'"
        val = (username)
        mycursor.execute(sql, val)
        data = mycursor.fetchone()
        if(len(data) > 0):
            return True
        return False

    def createUser(self,username,password):
        mycursor = self.dbp.cursor()
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, self.cifrar_contrasena(password))
        mycursor.execute(sql, val)
        return True
    
    def login(self, username, password):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM users WHERE username = '%s' && WHERE password = '%s'"
        val = (username, self.cifrar_contrasena(password))
        mycursor.execute(sql, val)
        data = mycursor.fetchone()
        if len(data) == 0:
            return False
        if len(data) == 1:
            userl = user(user[0], user[1], user[2])
            return userl

        