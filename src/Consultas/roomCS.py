from src.database.db import db
from src.models.battle import battle
from src.models.team import team
from src.models.pokemon import pokemon
import json
class roomCS:

    def __init__(self):
        self.dbp = db().mydb
    
    def getBattle(self, room_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM battles where room_id=%s"
        mycursor.execute(sql, (room_id,))
        data = mycursor.fetchone()
        if data != None:
            data = battle(data[0], data[1], data[2], data[3], data[4], data[5])

        self.dbp.commit()
        return data
    
    def getUserTeam(self, room_id , user_id):
        self.dbp.commit()
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM teams where room_id=%s AND user_id=%s"
        mycursor.execute(sql, (room_id, user_id))
        data = mycursor.fetchall()
        teams = []

        if teams != None:
            for row in data:
                teams.append(team(row[0], row[1], row[2], row[3], row[4], row[5], row[6]))
        self.dbp.commit()
        return teams
    
    def isTodosConVida(self, room_id, user_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM teams WHERE room_id=%s AND user_id=%s AND vida > 0"
        mycursor.execute(sql, (room_id ,user_id,))
        data = mycursor.fetchall()
        if data == None:
            return False
        if len(data) > 1:
            return True

    def pokemonActivo(self, room_id, user_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT p.* FROM rooms r JOIN teams t ON t.room_id = r.id AND t.active = 1 JOIN pokemons p ON p.id = t.pokemon_id WHERE r.id = %s AND r.user_id = %s"
        mycursor.execute(sql, (room_id ,user_id,))
        data = mycursor.fetchone()
        if data == None:
            return False
        return pokemon(int(data[0]), data[1], eval(data[2]), eval(data[3]), json.loads(data[4]), int(data[5]))
    