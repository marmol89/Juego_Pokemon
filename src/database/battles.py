from src.database.db import db
from src.models.user import user
import json
class battles:
    def __init__(self):
        self.dbp = db().mydb
    
    def createBattle(self, room_id):
        mycursor = self.dbp.cursor()
        sql = "INSERT INTO battles (room_id) VALUES (%s)"
        val = (room_id,)
        mycursor.execute(sql, val)
        self.dbp.commit()
        return mycursor.lastrowid
    
    def updateBattle(self, battle):
        mycursor = self.dbp.cursor()
        sql = "UPDATE battles SET winner_id=%s , loser_id=%s , user_team_ids=%s , enemy_team_ids=%s WHERE room_id=%s"
        val = (battle.winner_id, battle.loser_id, json.dumps(battle.user_team_ids), json.dumps(battle.enemy_team_ids), battle.room_id)
        mycursor.execute(sql, val)
        self.dbp.commit()
    
    def getUser(self, battle_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT users.* FROM battles JOIN rooms ON battles.room_id = rooms.id JOIN users ON rooms.user_id = users.id WHERE battles.id =%s;"
        mycursor.execute(sql, (battle_id,))
        data = mycursor.fetchone()
        
        if data != None:
            data = user(data[0], data[1], data[2])
        
        self.dbp.commit()
        return data
    
    def getEnemy(self, battle_id):
        mycursor = self.dbp.cursor()
        sql = "SELECT users.* FROM battles JOIN rooms ON battles.room_id = rooms.id JOIN users ON rooms.enemigo_id = users.id WHERE battles.id =%s;"
        mycursor.execute(sql, (battle_id,))
        data = mycursor.fetchone()
        
        if data != None:
            data = user(data[0], data[1], data[2])
        
        self.dbp.commit()
        return data
    
    def updateBattleUserTeam(self, battle):
        mycursor = self.dbp.cursor()
        sql = "UPDATE battles SET user_team_ids=%s WHERE room_id=%s"
        val = (json.dumps(battle.user_team_ids), battle.room_id)
        mycursor.execute(sql, val)
        self.dbp.commit()
    
    def updateBattleEnemyTeam(self, battle):
        mycursor = self.dbp.cursor()
        sql = "UPDATE battles SET enemy_team_ids=%s WHERE room_id=%s"
        val = (json.dumps(battle.enemy_team_ids), battle.room_id)
        mycursor.execute(sql, val)
        self.dbp.commit()