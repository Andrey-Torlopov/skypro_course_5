from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint
from typing import Optional

from game.equipment import Equipment, Weapon, Armor
from game.classes import UnitClass


class BaseUnit(ABC):
    """
    Базовый класс юнита
    """
    def __init__(self, name: str, unit_class: UnitClass):
        """
        При инициализации класса Unit используем свойства класса UnitClass
        """
        self.name = name
        # Модификаторы зашиты тут
        self.unit_class = unit_class
        self.hp = unit_class.max_health
        self.stamina = unit_class.max_stamina
        self.weapon = None
        self.armor = None
        self.is_skill_used = False
        self.max_stamina = unit_class.max_stamina
        self.max_hp = unit_class.max_health

    @property
    def health_points(self):
        return f"{round(self.hp, 1)} HP"

    @property
    def stamina_points(self) -> str:
        return f"{round(self.stamina,1)} SP"

    def equip_weapon(self, weapon: Weapon) -> str:
        self.weapon = weapon
        return f"{self.name} экипирован оружием {self.weapon.name}"

    def equip_armor(self, armor: Armor) -> str:
        self.armor = armor
        return f"{self.name} экипирован броней {self.armor.name}"

    def _count_damage(self, target: BaseUnit) -> float:
        if self.stamina <= self.weapon.stamina_per_hit:
            return 0
        attacker_damage: float = round(self.weapon.damage * self.unit_class.attack, 1)

        target_armor: float = 0
        if target.stamina > target.armor.stamina_per_turn:
            target_armor = round(target.armor.defence * target.armor.defence, 1)

        damage: float = round(attacker_damage - target_armor, 1)
        target.get_damage(damage)

        self.stamina -= self.armor.stamina_per_turn + self.unit_class.stamina
        if self.stamina < 0:
            self.stamina = 0
        target.stamina -= target.armor.stamina_per_turn + target.unit_class.stamina
        if target.stamina < 0:
            target.stamina = 0

        return damage

    def get_damage(self, damage: float) -> Optional[float]:
        self.hp -= damage
        return damage

    @abstractmethod
    def hit(self, target: BaseUnit) -> str:
        """
        этот метод будет переопределен ниже
        """
        pass

    def use_skill(self, target: BaseUnit) -> str:
        """
        метод использования умения.
        если умение уже использовано возвращаем строку
        Навык использован
        Если же умение не использовано тогда выполняем функцию
        self.unit_class.skill.use(user=self, target=target)
        и уже эта функция вернем нам строку которая характеризует выполнение умения
        """
        if self.is_skill_used:
            return f"{self.unit_class.name} уже использовал скилл, поэтому просто пропускает ход"
        self.is_skill_used = True
        return self.unit_class.skill.use(self, target=target)


class PlayerUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар игрока:
        здесь происходит проверка достаточно ли выносливости для нанесения удара.
        вызывается функция self._count_damage(target)
        а также возвращается результат в виде строки
        """
        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target=target)
        success_result = f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} соперника и наносит {damage} урона."
        fail_result = f"{self.name} используя {self.weapon.name} наносит удар, но {target.armor.name} cоперника его останавливает."

        return success_result if damage > 0 else fail_result


class EnemyUnit(BaseUnit):

    def hit(self, target: BaseUnit) -> str:
        """
        функция удар соперника
        должна содержать логику применения соперником умения
        (он должен делать это автоматически и только 1 раз за бой).
        Например, для этих целей можно использовать функцию randint из библиотеки random.
        Если умение не применено, противник наносит простой удар, где также используется
        функция _count_damage(target
        """
        if randint(0, 100) > 50 and not self.is_skill_used:
            self.is_skill_used = True
            return self.use_skill(target=target)

        if self.stamina < self.weapon.stamina_per_hit:
            return f"{self.name} попытался использовать {self.weapon.name}, но у него не хватило выносливости."

        damage = self._count_damage(target=target)
        success_result = f"{self.name} используя {self.weapon.name} пробивает {target.armor.name} и наносит Вам {damage} урона."
        fail_result = f"{self.name} используя {self.weapon.name} наносит удар, но Ваш(а) {target.armor.name} его останавливает."

        return success_result if damage > 0 else fail_result
