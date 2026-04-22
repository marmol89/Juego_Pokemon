def calculate_damage(base_power, attack, defense, type_multiplier=1.0, stab_bonus=1.0):
    """
    Calculates damage based on attack, defense, base power, type effectiveness, and STAB.
    Formula: max(1, int((attack / defense) * base_power * 0.5 * type_multiplier * stab_bonus))
    """
    if defense <= 0:
        # Avoid division by zero
        base_damage = max(1, int(attack * base_power * 0.5))
    else:
        base_damage = int((attack / defense) * base_power * 0.5)
        base_damage = max(1, base_damage)
    
    final_damage = int(base_damage * type_multiplier * stab_bonus)
    return max(1, final_damage)


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
