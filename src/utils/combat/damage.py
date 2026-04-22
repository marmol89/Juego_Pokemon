def calculate_damage(attacker, defender, move_power):
    """
    Calcula el daño infligido basándose en las estadísticas del atacante y defensor.
    Fórmula: max(1, int((Atk / Def) * Poder * 0.5))
    """
    if defender.defensa <= 0:
        # Evitar división por cero
        return max(1, int(attacker.ataque * move_power * 0.5))
        
    dmg = int((attacker.ataque / defender.defensa) * move_power * 0.5)
    return max(1, dmg)


def calcular_dano(attack: float, defense: float, power: float) -> float:
    """
    Calculates damage based on attack, defense and power.
    Formula: ((attack / defense) * power) / 2
    """
    if defense <= 0:
        return max(1, (attack * power) / 2)
    return ((attack / defense) * power) / 2


# Type effectiveness chart
_TYPE_EFFECTIVENESS = {
    ('fuego', 'planta'): 2.0,    # Fire vs Grass = super effective
    ('fuego', 'agua'): 0.5,       # Fire vs Water = not very effective
    ('fuego', 'fuego'): 0.5,
    ('agua', 'fuego'): 2.0,
    ('agua', 'planta'): 0.5,
    ('planta', 'agua'): 2.0,
    ('planta', 'fuego'): 0.5,
    ('electrico', 'agua'): 2.0,
    ('electrico', 'planta'): 0.5,
}


def obtener_multiplicador(tipo_ataque: str, tipo_defensa: str) -> float:
    """
    Returns the damage multiplier based on attack and defense types.
    Default is 1.0 (neutral).
    """
    return _TYPE_EFFECTIVENESS.get((tipo_ataque, tipo_defensa), 1.0)
