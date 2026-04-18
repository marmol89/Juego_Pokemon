import time
from src.menus.menuBattle import menuBattle
class battleController:
    def __init__(self, room, user):
        self.room = room
        self.battle = room.getBattle()
        self.user = user
        self.updateTeams()
    
    def inicio(self):
        if not self.battle:
            return
        menuBattle(self.room).inicio(self.user, self.enemy)
        menuBattle(self.room).presentacionPokemons(self.user, self.enemy, self.userTeam, self.enemyTeam)
        self.combate()

    def combate(self):
        if not self.battle:
            return
        from src.Consultas.movementCS import movementCS
        from src.Consultas.teamCS import teamCS
        import json
        movCS = movementCS()
        teamdb = teamCS()

        while (self.room.isVidaTeamUser() and self.room.isVidaTeamEnemigo()):
            self.updateTeams()
            activeUserTeam = next((t for t in self.userTeam if t.active), self.userTeam[0])
            activeEnemyTeam = next((t for t in self.enemyTeam if t.active), self.enemyTeam[0])
            
            if self.user.id == self.room.user_id:
                userPokemon = self.room.pokemonActivoUser()
                enemyPokemon = self.room.pokemonActivoEnemigo()
            else:
                userPokemon = self.room.pokemonActivoEnemigo()
                enemyPokemon = self.room.pokemonActivoUser()
            
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
            
            if activeUserTeam.vida <= 0:
                userAlives = [t for t in self.userTeam if t.vida > 0]
                if not userAlives:
                    break
                new_active = menuBattle(self.room).cambiarPokemon(self.userTeam)
                teamdb.changeActive(activeUserTeam.id, new_active.id)
                time.sleep(2)
            
            if activeEnemyTeam.vida <= 0:
                enemyAlives = [t for t in self.enemyTeam if t.vida > 0]
                if not enemyAlives:
                    break
                print("\nEsperando a que el rival elija su próximo Pokémon...")
                while True:
                    self.updateTeams()
                    newEnemy = next((t for t in self.enemyTeam if t.active), None)
                    if newEnemy and newEnemy.vida > 0:
                        break
                    time.sleep(1.5)

        if activeUserTeam.vida <= 0:
            menuBattle(self.room).derrota(self.user, self.enemy, self.userTeam, self.enemyTeam)
            self.cleanUp(ganador=False)
        elif activeEnemyTeam.vida <= 0:
            menuBattle(self.room).victoria(self.user, self.enemy, self.userTeam, self.enemyTeam)
            self.cleanUp(ganador=True)

    def cleanUp(self, ganador=False):
        from src.database.users import users
        userdb = users()
        
        puntos_actuales = self.user.puntos
        puntos_finales = puntos_actuales
        res_puntos = 0

        if ganador:
            pokemon_vivos = len([t for t in self.userTeam if t.vida > 0])
            res_puntos = 20 + (pokemon_vivos * 5)
            print(f"\n  ¡HAS GANADO! +{res_puntos} puntos de ranking.")
        else:
            pokemon_derrotados_enemigo = len([t for t in self.enemyTeam if t.vida <= 0])
            res_puntos = -10
            if pokemon_derrotados_enemigo == 0:
                res_puntos -= 5 # Penalización por no matar ninguno
            print(f"\n  HAS PERDIDO. {res_puntos} puntos de ranking.")

        puntos_finales += res_puntos
        userdb.updatePuntos(self.user.id, puntos_finales)

        print(f"  Puntuación total: {puntos_finales} puntos.")
        print("\nBatalla terminada. Volviendo al menú en 5 segundos...")
        time.sleep(5)
        
        if self.room.user_id == self.user.id:
            from src.database.rooms import rooms
            roomsdb = rooms()
            roomsdb.deleteRoom(self.room.id)
            

    def updateTeams(self):
        self.userTeam = self.room.getMyTeam(self.user.id)
        self.enemyTeam = self.room.getTheirTeam(self.user.id)
        self.enemy = self.room.getTheirUser(self.user.id)