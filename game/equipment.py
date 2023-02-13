from dataclasses import dataclass
from random import uniform
import marshmallow_dataclass
import marshmallow
import json


@dataclass
class Armor:
    id: int
    name: str
    defence: int
    stamina_per_turn: int


@dataclass
class Weapon:
    id: int
    name: str
    min_damage: float
    max_damage: float
    stamina_per_hit: float

    @property
    def damage(self) -> float:
        return round(uniform(self.min_damage, self.max_damage), 1)


@dataclass
class EquipmentData:
    weapons: list[Weapon]
    armors: list[Armor]


@dataclass
class Equipment:
    equipment: EquipmentData

    def __init__(self):
        self.equipment = self._get_equipment_data()

    def get_weapon(self, weapon_name: str) -> Weapon:
        return list(filter(lambda x: x.name == weapon_name, self.equipment.weapons))[0]

    def get_armor(self, armor_name: str) -> Armor:
        return list(filter(lambda x: x.name == armor_name, self.equipment.armors))[0]

    def get_weapons_names(self) -> list:
        return list(map(lambda x: x.name, self.equipment.weapons))

    def get_armors_names(self) -> list:
        return list(map(lambda x: x.name, self.equipment.armors))

    @staticmethod
    def _get_equipment_data() -> EquipmentData:
        with open("./data/equipment.json") as file:
            data = json.load(file)

        equipment_schema = marshmallow_dataclass.class_schema(EquipmentData)
        try:
            return equipment_schema().load(data)
        except marshmallow.exceptions.ValidationError:
            raise ValueError
