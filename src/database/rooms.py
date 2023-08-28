from src.database.db import db
from src.models.room import room
class rooms:

    def __init__(self):
        self.dbp = db().mydb
    
    def getRooms(self):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        rooms = []
        if room != None:
            for row in data:
                rooms.append(room(row[0], row[1], row[2], row[3], row[4]))
        return rooms
    
    def getRoomActivos(self):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms where estado=1"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        rooms = []
        if room != None:
            for row in data:
                rooms.append(room(row[0], row[1], row[2], row[3], row[4]))
        return rooms
    
    def getRoomCerrados(self):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms where estado=2"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        rooms = []
        if room != None:
            for row in data:
                rooms.append(room(row[0], row[1], row[2], row[3], row[4]))
        return rooms
    
    def getRoomFinalizados(self):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms where estado=3"
        mycursor.execute(sql)
        data = mycursor.fetchall()
        rooms = []
        if room != None:
            for row in data:
                rooms.append(room(row[0], row[1], row[2], row[3], row[4]))
        return rooms
    
    def getRoomUser(self, user_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms where user_id=%s OR enemigo_id=%s"
        mycursor.execute(sql, (user_id, user_id))
        data = mycursor.fetchall()
        rooms = []

        if room != None:
            for row in data:
                rooms.append(room(row[0], row[1], row[2], row[3], row[4]))
        return rooms
    
    def getRoomUserActiva(self, user_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms where (user_id=%s OR enemigo_id=%s) AND estado=1"
        mycursor.execute(sql, (user_id, user_id))
        data = mycursor.fetchone()
        
        if room != None:
            data = room(data[0], data[1], data[2], data[3], data[4])
        
        return data
    
    def createRoom(self, user_id , name):
        mycursor = self.dbp.cursor()
        sql = "INSERT INTO rooms (user_id, nombre, estado) VALUES (%s, %s, %s)"
        val = (user_id , name , 1)
        mycursor.execute(sql, val)
        self.dbp.commit()
    
    def getRoom(self, id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM rooms where id=%s"
        mycursor.execute(sql, (id,))
        data = mycursor.fetchone()
        
        if room != None:
            data = room(data[0], data[1], data[2], data[3], data[4])
        
        self.dbp.commit()
        return data
    
    def updateRoom(self, room):
        mycursor = self.dbp.cursor()
        sql = "UPDATE rooms SET user_id = %s, enemigo_id = %s, nombre = %s , estado = %s  WHERE id = %s"
        val = (room.user_id, room.enemigo_id, room.nombre, room.estado, room.id)
        mycursor.execute(sql, val)
        self.dbp.commit()