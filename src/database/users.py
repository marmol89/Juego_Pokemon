from src.database.db import db
from src.models.user import user
import hashlib

class users:
    salt = 'patata'

    def __init__(self):
        self.dbp = db().get_connection()
    
    def cifrar_contrasena(self, password):
        contrasena_codificada = password.encode('utf-8')
        hashed = hashlib.pbkdf2_hmac('sha256', contrasena_codificada, self.salt.encode('utf-8'), 100000)
        return hashed.hex()
    
    def verificar_contrasena(self, contrasena, hashed_hex):
        return self.cifrar_contrasena(contrasena) == hashed_hex
    
    def verificarUser(self , username):
        if not self.dbp: return False
        data = self.dbp.table("users").select("*").eq("username", username).execute()
        return len(data.data) == 0

    def createUser(self, username, password):
        if not self.dbp: return False
        val = {"username": username, "password": self.cifrar_contrasena(password)}
        self.dbp.table("users").insert(val).execute()
        return True
    
    def login(self, username, password):
        if not self.dbp: return None
        data = self.dbp.table("users").select("*").eq("username", username).execute()
        if len(data.data) == 0:
            return None
        user_row = data.data[0]
        if not self.verificar_contrasena(password, user_row['password']):
            return None
        return user(user_row['id'], user_row['username'], user_row['password'])
    
    def getUser(self, id):
        if not self.dbp: return None
        data = self.dbp.table("users").select("*").eq("id", id).execute()
        if len(data.data) == 0:
            return None
        user_row = data.data[0]
        return user(user_row['id'], user_row['username'], user_row['password'])