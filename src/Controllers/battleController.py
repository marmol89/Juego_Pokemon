import time
from src.menus.menuBattle import menuBattle
class battleController:
    def __init__(self, room, user):
        self.room = room
        self.battle = room.getBattle()
        self.user = user
        self.updateTeams()
    
    def inicio(self):
        menuBattle(self.room).inicio(self.user, self.enemy)
        menuBattle(self.room).presentacionPokemons(self.user, self.enemy, self.userTeam, self.enemyTeam)
        self.combate()

    def combate(self):
        from src.Consultas.movementCS import movementCS
        from src.Consultas.teamCS import teamCS
        import json
        movCS = movementCS()
        teamdb = teamCS()

        while (self.room.isVidaTeamUser() and self.room.isVidaTeamEnemigo()):
            self.updateTeams()
            activeUserTeam = next((t for t in self.userTeam if t.active), self.userTeam[0])
            activeEnemyTeam = next((t for t in self.enemyTeam if t.active), self.enemyTeam[0])
            userPokemon = self.room.pokemonActivoUser()
            enemyPokemon = self.room.pokemonActivoEnemigo()
            
            move = menuBattle(self.room).combate(self.user, self.enemy, self.userTeam, self.enemyTeam)
            movCS.insertMovement(self.room.id, userPokemon.id, move['nombre'], json.dumps(move))
            
            print("Esperando la acción del oponente...")
            opponentMoveRow = None
            while opponentMoveRow is None:
                opponentMoveRow = movCS.getMovement(self.room.id, enemyPokemon.id)
                time.sleep(1)
                
            opponentMove = json.loads(opponentMoveRow['efecto'])
            
            if userPokemon.velocidad >= enemyPokemon.velocidad:
                firstAtk, firstDef = userPokemon, enemyPokemon
                firstMove, secondMove = move, opponentMove
                firstVidaVar, secondVidaVar = activeUserTeam, activeEnemyTeam
                firstName, secondName = self.user.username, self.enemy.username
            else:
                firstAtk, firstDef = enemyPokemon, userPokemon
                firstMove, secondMove = opponentMove, move
                firstVidaVar, secondVidaVar = activeEnemyTeam, activeUserTeam
                firstName, secondName = self.enemy.username, self.user.username
                
            def calc_damage(atk, dfen, pwr):
                return max(1, int((atk / dfen) * pwr * 0.5))

            print(f"\n{firstName} usa {firstMove['nombre']}!")
            dmg1 = calc_damage(firstAtk.ataque, firstDef.defensa, firstMove['poder'])
            secondVidaVar.vida -= dmg1
            print(f"Causa {dmg1} puntos de daño.")
            time.sleep(2)
            
            if secondVidaVar.vida > 0:
                print(f"\n{secondName} usa {secondMove['nombre']}!")
                dmg2 = calc_damage(firstDef.ataque, firstAtk.defensa, secondMove['poder'])
                firstVidaVar.vida -= dmg2
                print(f"Causa {dmg2} puntos de daño.")
                time.sleep(2)
            
            teamdb.updateVida(activeUserTeam.id, activeUserTeam.vida)
            
            my_move_row = movCS.getMovement(self.room.id, userPokemon.id)
            if my_move_row:
                movCS.deleteMovement(my_move_row['id'])
            time.sleep(1.5)

        
        if (self.room.isVidaTeamEnemigo()):
            self.battle.winner_id = self.enemy.id
            self.battle.loser_id = self.user.id
            self.battle.save()
            menuBattle(self.room).derrota(self.user, self.enemy, self.userTeam, self.enemyTeam)
            self.cleanUp()
        elif (self.room.isVidaTeamUser()):
            self.battle.winner_id = self.user.id
            self.battle.loser_id = self.enemy.id
            self.battle.save()
            menuBattle(self.room).victoria(self.user, self.enemy, self.userTeam, self.enemyTeam)
            self.cleanUp()

    def cleanUp(self):
        print("\nBatalla terminada. Volviendo al menú en 5 segundos...")
        time.sleep(5)
        if self.room.user_id == self.user.id:
            from src.database.rooms import rooms
            roomsdb = rooms()
            roomsdb.deleteRoom(self.room.id)
            

    def updateTeams(self):
        if (self.user.id == self.room.user_id):
            self.userTeam = self.room.getUserTeam()
            self.enemyTeam = self.room.getEnemigoTeam()
            self.enemy = self.room.getEnemigo()
        if (self.user.id == self.room.enemigo_id):
            self.userTeam = self.room.getEnemigoTeam()
            self.enemyTeam = self.room.getUserTeam()
            self.enemy = self.room.getUser()