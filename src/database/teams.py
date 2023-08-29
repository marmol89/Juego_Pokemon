from src.database.db import db
from src.models.team import team as Team

class teams:
    def __init__(self):
        self.dbp = db().mydb
    
    def getTeam(self, id):
        mycursor = self.dbp.cursor()
        sql = "SELECT * FROM teams WHERE id=%s"
        mycursor.execute(sql, (id ,))
        data = mycursor.fetchone()
        if data == None:
            return None
        if len(data) > 1:
            team = Team(data[0], data[1], data[2], data[3], data[4], data[5])
            return team
    
    def updateTeam(self, team):
        mycursor = self.dbp.cursor()
        sql = "UPDATE teams SET active = %s, vida = %s, efecto = %s WHERE id = %s"
        val = (team.active, team.vida, team.efecto, team.id)
        mycursor.execute(sql, val)
        self.dbp.commit()

    def createTeam(self, team):
        mycursor = self.dbp.cursor()
        sql = "INSERT INTO teams (room_id, user_id, pokemon_id, active, vida, efecto) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (team.room_id , team.user_id , team.pokemon_id , team.active, team.vida, team.efecto if team.efecto else 'NULL')
        mycursor.execute(sql, val)
        self.dbp.commit()

        return True