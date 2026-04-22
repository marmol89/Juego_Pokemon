import unittest
from unittest.mock import patch, MagicMock

from src.models.pokemon import pokemon
from src.utils.combat.damage import calculate_damage, obtener_multiplicador


class TestBattle(unittest.TestCase):

    def test_damage_calculation(self):
        # Test damage formula using calculate_damage
        attack = 50
        defense = 30
        power = 90
        expected_damage = max(1, int((attack / defense) * power * 0.5))
        result = calculate_damage(base_power=power, attack=attack, defense=defense)
        self.assertEqual(result, expected_damage)

    def test_effectiveness_fire_vs_grass(self):
        # Fire vs Grass = super effective (2x)
        result = obtener_multiplicador('fuego', 'planta')
        self.assertEqual(result, 2.0)

    def test_effectiveness_fire_vs_water(self):
        # Fire vs Water = not very effective (0.5x)
        result = obtener_multiplicador('fuego', 'agua')
        self.assertEqual(result, 0.5)

    def test_effectiveness_neutral(self):
        # Neutral = 1x
        result = obtener_multiplicador('fuego', 'electrico')
        self.assertEqual(result, 1.0)

    def test_fainted_pokemon(self):
        pikachu = pokemon(
            id=1,
            nombre='Pikachu',
            tipos=['electrico'],
            movimientos=[],
            EVs={"ataque": 40, "defensa": 30},
            puntos_de_salud=0
        )
        self.assertTrue(pikachu.ha_perdido())

    def test_not_fainted_pokemon(self):
        pikachu = pokemon(
            id=1,
            nombre='Pikachu',
            tipos=['electrico'],
            movimientos=[],
            EVs={"ataque": 40, "defensa": 30},
            puntos_de_salud=50
        )
        self.assertFalse(pikachu.ha_perdido())