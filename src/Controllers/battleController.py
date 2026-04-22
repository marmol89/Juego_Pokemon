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
            
            # Usar getLatestMovement para obtener solo el movimiento más reciente
            latest_movs = movCS.getLatestMovements(self.room.id, 2)
            opponentMove = None
            for m in latest_movs:
                if m['pokemon_id'] == enemyPokemon.id:
                    opponentMove = json.loads(m['efecto'])
                    movCS.deleteMovement(m['id'])
                    break

            if opponentMove is None:
                # Seguir esperando si no hay movimiento del oponente
                while opponentMove is None:
                    latest_movs = movCS.getLatestMovements(self.room.id, 10)
                    for m in latest_movs:
                        if m['pokemon_id'] == enemyPokemon.id:
                            opponentMove = json.loads(m['efecto'])
                            movCS.deleteMovement(m['id'])
                            break
                    if opponentMove is None:
                        time.sleep(0.5)
            
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
                    from src.utils.combat.damage import calculate_damage, obtener_multiplicador
                    
                    # Calculate type multiplier
                    attack_type = m.get('tipo', '').lower()
                    defense_types = def_pok.tipos if isinstance(def_pok.tipos, list) else []
                    type_multiplier = 1.0
                    for def_type in defense_types:
                        type_multiplier *= obtener_multiplicador(attack_type, def_type.lower())
                    
                    # Calculate STAB bonus (1.5 if attacker type matches move type)
                    attacker_types = pok.tipos if isinstance(pok.tipos, list) else []
                    stab_bonus = 1.0
                    move_type_lower = attack_type
                    for atk_type in attacker_types:
                        if atk_type.lower() == move_type_lower:
                            stab_bonus = 1.5
                            break
                    
                    dmg = calculate_damage(m['poder'], pok.ataque, def_pok.defensa, type_multiplier, stab_bonus)
                    
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

            opp_move_row = movCS.getMovement(self.room.id, enemyPokemon.id)
            if opp_move_row:
                movCS.deleteMovement(opp_move_row['id'])
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

    def _calculate_scoring(self, winner):
        """
        Calculates and updates the scoring for battle outcome.
        
        Args:
            winner: Boolean indicating if the user won the battle
        """
        from src.database.users import users
        userdb = users()
        
        puntos_actuales = self.user.puntos
        res_puntos = 0

        if winner:
            pokemon_vivos = len([t for t in self.userTeam if t.vida > 0])
            res_puntos = 20 + (pokemon_vivos * 5)
            print(f"\n  ¡HAS GANADO! +{res_puntos} puntos de ranking.")
        else:
            pokemon_derrotados_enemigo = len([t for t in self.enemyTeam if t.vida <= 0])
            res_puntos = -10
            if pokemon_derrotados_enemigo == 0:
                res_puntos -= 5
            print(f"\n  HAS PERDIDO. {res_puntos} puntos de ranking.")

        puntos_finales = max(0, puntos_actuales + res_puntos)
        userdb.updatePuntos(self.user.id, puntos_finales)
        print(f"  Puntuación total: {puntos_finales} puntos.")
        return res_puntos
    
    def _cleanup_battle(self):
        """
        Performs cleanup operations after the battle ends.
        Only the room creator performs cleanup (deletes the room).
        """
        if self.room.user_id == self.user.id:
            from src.database.rooms import rooms
            roomsdb = rooms()
            roomsdb.deleteRoom(self.room.id)
    
    def cleanUp(self, ganador=False):
        print("\nBatalla terminada. Volviendo al menú en 5 segundos...")
        time.sleep(5)
        self._calculate_scoring(ganador)
        self._cleanup_battle()
            

    def updateTeams(self):
        self.userTeam = self.room.getMyTeam(self.user.id)
        self.enemyTeam = self.room.getTheirTeam(self.user.id)
        self.enemy = self.room.getTheirUser(self.user.id)