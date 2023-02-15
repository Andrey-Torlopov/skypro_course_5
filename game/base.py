from game.unit import BaseUnit


class BaseSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Arena(metaclass=BaseSingleton):
    STAMINA_PER_ROUND = 1
    player = None
    enemy = None
    game_is_running = False

    def start_game(self, player: BaseUnit, enemy: BaseUnit) -> None:
        self.player = player
        self.enemy = enemy
        self.game_is_running = True
        self.battle_result = None
        self.log: list[str] = []

    def _check_players_hp(self) -> None:
        if self.player.hp > 0 >= self.enemy.hp:
            self.battle_result = "Игрок виграл битву"
            self.game_is_running = False
        elif self.player.hp <= 0 < self.enemy.hp:
            self.battle_result = "Игрок проиграл битву"
            self.game_is_running = False
        elif self.player.hp <= 0 <= self.enemy.hp:
            self.battle_result = "Ничья"
            self.game_is_running = False
        else:
            return

    def _stamina_regeneration(self) -> None:
        self.player.stamina += self.STAMINA_PER_ROUND
        self.enemy.stamina += self.STAMINA_PER_ROUND

        if self.player.stamina > self.player.max_stamina:
            self.player.stamina = self.player.max_stamina

        if self.enemy.stamina > self.enemy.max_stamina:
            self.enemy.stamina = self.enemy.max_stamina

    def next_turn(self) -> None:
        self._check_players_hp()

        if self.battle_result is not None:
            return

        self._stamina_regeneration()
        self.log.append(self.enemy.hit(self.player))

    def _end_game(self) -> None:
        self._instances = {}
        self.game_is_running = False

    def player_hit(self) -> None:
        self.log.append(self.player.hit(self.enemy))

        next_turn_result = self.next_turn()
        if next_turn_result is not None:
            self.log.append(next_turn_result)

    def player_use_skill(self) -> None:
        self.log.append(self.player.use_skill(self.enemy))
        next_turn_result = self.next_turn()
        if next_turn_result is not None:
            self.log.append(next_turn_result)
