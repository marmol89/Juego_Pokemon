import time
import json
from src.menus.menuBattle import menuBattle
from src.utils.visuals import type_text, animate_hp_bar, shake_screen
class battleController:
    def __init__(self, room, user):
        self.room = room
        self.battle = room.getBattle()
        self.user = user
        self.items_used = 0
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
            
            move = menuBattle(self.room).combate(self.user, self.enemy, self.userTeam, self.enemyTeam, self.items_used)
            
            # Detectar si el menú vio que el oponente se rindió
            if move.get("tipo_accion") == "opponent_surrender":
                type_text("\n¡EL RIVAL SE HA RENDIDO!")
                activeEnemyTeam.vida = 0
                break

            # Rendición inmediata propia
            if move.get("tipo_accion") == "surrender":
                movCS.insertMovement(self.room.id, userPokemon.id, "Rendición", json.dumps(move))
                break # El bucle principal termina, irá a cleanUp con hp actual (que será >0 pero forzaremos derrota)

            # Si eligió mochila
            if move.get("tipo_accion") == "item":
                chosen_item = menuBattle(self.room).mochila(self.user.id, self.items_used)
                if chosen_item is None:
                    continue # Vuelve al menú anterior
                
                self.items_used += 1 # Incrementar contador
                move = {
                    "nombre": f"Item: {chosen_item.nombre}",
                    "tipo_accion": "use_item",
                    "item_id": chosen_item.id,
                    "efecto_item": chosen_item.efecto
                }

            movCS.insertMovement(self.room.id, userPokemon.id, move['nombre'], json.dumps(move))
            
            print("Esperando la acción del oponente...")
            opponentMoveRow = None
            while opponentMoveRow is None:
                opponentMoveRow = movCS.getMovement(self.room.id, enemyPokemon.id)
                time.sleep(1)
                
            opponentMove = json.loads(opponentMoveRow['efecto'])
            
            # --- DETECTAR RENDICIÓN DEL OPONENTE ---
            if opponentMove.get("tipo_accion") == "surrender":
                type_text("\n¡EL RIVAL SE HA RENDIDO!")
                # Forzamos victoria rompiendo el bucle con la vida del enemigo en 0 ficticio
                activeEnemyTeam.vida = 0
                break

            
            # --- RESOLUCIÓN DE TURNO CON OBJETOS ---
            # Para simplificar, los objetos siempre se usan AL PRINCIPIO del turno antes que cualquier ataque.
            # Si ambos usan objetos, se procesan en orden de velocidad.
            
            participants = [
                {"user": self.user, "pokemon": userPokemon, "move": move, "team": activeUserTeam, "is_user": True},
                {"user": self.enemy, "pokemon": enemyPokemon, "move": opponentMove, "team": activeEnemyTeam, "is_user": False}
            ]
            
            # Ordenar por velocidad (o prioridad si la hubiera)
            if userPokemon.velocidad < enemyPokemon.velocidad:
                participants.reverse()
            
            for p in participants:
                m = p["move"]
                t = p["team"]
                pok = p["pokemon"]
                
                if m.get("tipo_accion") == "use_item":
                    # Aplicar item
                    type_text(f"\n{p['user'].username} usa {m['nombre']}!")
                    efecto = m.get("efecto_item", {})
                    if "cura" in efecto:
                        cura = efecto["cura"]
                        vida_antes = t.vida
                        t.vida = min(pok.puntos_de_salud, t.vida + cura)
                        
                        prefix = f"   {pok.nombre}: "
                        animate_hp_bar(vida_antes, t.vida, pok.puntos_de_salud, prefix=prefix)
                        type_text(f"¡{pok.nombre} recupera vida!")
                    
                    # Consumir de la DB (solo si lo usó el usuario actual localmente)
                    if p["is_user"]:
                        from src.database.items import items
                        items().consumeItem(self.user.id, m["item_id"])
                    time.sleep(2)
                else:
                    # Es un ataque normal
                    # Primero comprobamos si el atacante sigue vivo
                    if t.vida <= 0: continue
                    
                    # Identificar defensor
                    defensor = participants[1] if p == participants[0] else participants[0]
                    def_pok = defensor["pokemon"]
                    def_team = defensor["team"]
                    
                    if def_team.vida <= 0: continue

                    type_text(f"\n{p['user'].username} usa {m['nombre']}!")
                    dmg = max(1, int((pok.ataque / def_pok.defensa) * m['poder'] * 0.5))
                    
                    vida_antes = def_team.vida
                    def_team.vida = max(0, def_team.vida - dmg)
                    
                    # Si el daño es alto, sacudimos la pantalla
                    if dmg > (def_pok.puntos_de_salud * 0.2):
                        shake_screen()
                        
                    prefix = f"   {def_pok.nombre}: "
                    animate_hp_bar(vida_antes, def_team.vida, def_pok.puntos_de_salud, prefix=prefix)
                    type_text(f"¡Causa {dmg} puntos de daño a {def_pok.nombre}!")
                    time.sleep(1)
            
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
                if new_active is None:
                    break
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

        # Si el bucle terminó por rendición propia, move tiene tipo_accion: surrender
        if move.get("tipo_accion") == "surrender":
            menuBattle(self.room).derrota(self.user, self.enemy, self.userTeam, self.enemyTeam)
            self.cleanUp(ganador=False)
        elif activeUserTeam.vida <= 0:
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