import unittest
from unittest.mock import patch, MagicMock

from src.models.pokemon import pokemon
from src.utils.combat.damage import calcular_dano, obtener_multiplicador


class TestBattle(unittest.TestCase):

    def test_damage_calculation(self):
        # Mock pokemon stats and test damage formula
        attack = 50
        defense = 30
        power = 90
        expected_damage = ((attack / defense) * power) / 2
        result = calcular_dano(attack, defense, power)
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