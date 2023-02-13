from dataclasses import dataclass
from game.skills import Skill, FuryPunch, HardShot


@dataclass
class UnitClass:
    name: str
    max_health: float
    max_stamina: float
    # Модификатор атаки
    attack: float
    # Модификатор выносливости
    stamina: float
    # Модификатор брони
    armor: float
    skill: Skill


warriorClass = UnitClass(
    name="Воин", 
    max_health=60.0, 
    max_stamina=30.0,
    attack=0.8,
    stamina=0.9,
    armor=1.2,
    skill=FuryPunch())


thiefClass = UnitClass(
    name="Вор",
    max_health=50.0,
    max_stamina=25.0,
    attack=1.5,
    stamina=1.2,
    armor=1.0,
    skill=HardShot())


unit_classes = {
    thiefClass.name: thiefClass,
    warriorClass.name: warriorClass
}
