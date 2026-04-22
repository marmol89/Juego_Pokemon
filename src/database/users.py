from src.database.db import db
from src.models.user import user
import hashlib
import bcrypt
import secrets


def _generate_salt() -> str:
    """Generate per-user unique salt (32 bytes)."""
    return secrets.token_hex(16)


def _hash_password(password: str) -> str:
    """Hash password with bcrypt, rounds=12."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(rounds=12)).decode('utf-8')


def _verify_password(password: str, hashed: str) -> bool:
    """Verify bcrypt password."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))


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
        salt = _generate_salt()
        hash_bcrypt = _hash_password(password)
        val = {
            "username": username,
            "password": self.cifrar_contrasena(password),
            "puntos": 0,
            "salt": salt,
            "hash": hash_bcrypt,
            "needs_migration": False
        }
        self.dbp.table("users").insert(val).execute()
        return True
    
    def login(self, username, password):
        if not self.dbp: return None
        data = self.dbp.table("users").select("*").eq("username", username).execute()
        if len(data.data) == 0:
            return None
        user_row = data.data[0]

        # Try bcrypt first (new hash column)
        if user_row.get('hash') and _verify_password(password, user_row['hash']):
            return user(user_row['id'], user_row['username'], user_row['password'], user_row.get('puntos', 0))

        # Fallback to legacy hash via verificar_contrasena
        if self.verificar_contrasena(password, user_row['password']):
            # Legacy match — rehash with bcrypt and update
            new_hash = _hash_password(password)
            self.dbp.table("users").update({
                "hash": new_hash,
                "hash_legacy": user_row['password'],
                "needs_migration": False
            }).eq("id", user_row['id']).execute()
            return user(user_row['id'], user_row['username'], user_row['password'], user_row.get('puntos', 0))

        return None
    
    def getUser(self, id):
        if not self.dbp: return None
        data = self.dbp.table("users").select("*").eq("id", id).execute()
        if len(data.data) == 0:
            return None
        user_row = data.data[0]
        return user(user_row['id'], user_row['username'], user_row['password'], user_row.get('puntos', 0))

    def updatePuntos(self, user_id, nuevos_puntos):
        if not self.dbp: return
        self.dbp.table("users").update({"puntos": nuevos_puntos}).eq("id", user_id).execute()