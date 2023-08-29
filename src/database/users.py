from src.database.db import db
from src.models.user import user
import hashlib

class users:
    salt = 'patata'

    def __init__(self):
        self.dbp = db().mydb
    
    def cifrar_contrasena(self, password):
        passwordS = password + self.salt
        hashed = hashlib.sha512(passwordS.encode()).hexdigest()
        return hashed
    
    def verificar_contrasena(self , contrasena, hashed):
        contrasena_codificada = contrasena.encode('utf-8')
        nuevo_hash = hashlib.pbkdf2_hmac('sha256', contrasena_codificada, self.salt, 100000)
        return nuevo_hash == hashed
    
    def verificarUser(self , username):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM users WHERE username=%s"
        mycursor.execute(sql , (username ,))
        data = mycursor.fetchone()  
        if(data == None):
            return True
        return False

    def createUser(self, username, password):
        mycursor = self.dbp.cursor()
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        val = (username, self.cifrar_contrasena(password))
        mycursor.execute(sql, val)
        self.dbp.commit()
        return True
    
    def login(self, username, password):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM users WHERE username=%s"
        mycursor.execute(sql, (username ,))
        data = mycursor.fetchone()
        if data == None:
            return None
        if data[2] != self.cifrar_contrasena(password):
            return None
        if len(data) > 1:
            userl = user(data[0], data[1], data[2])
            return userl
    
    def getUser(self, id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM users WHERE id=%s"
        mycursor.execute(sql, (id ,))
        data = mycursor.fetchone()
        if data == None:
            return None
        if len(data) > 1:
            userl = user(data[0], data[1], data[2])
            return userl
        