from flask import Flask
from flask import render_template, request, redirect
from game.unit import BaseUnit, PlayerUnit, EnemyUnit
from game.base import Arena
from game.equipment import Equipment
from game.classes import unit_classes
from typing import Optional

app = Flask(__name__)


heroes: dict[str: BaseUnit] = {}

arena: Arena = Arena()
equipment = Equipment()


@app.route("/")
def menu_page():
    return render_template("index.html")


@app.route("/fight/")
def start_fight():
    arena.start_game(
        player=heroes["player"],
        enemy=heroes["enemy"]
    )
    return render_template("fight.html", heroes=arena)


@app.route("/fight/hit")
def hit():
    if not arena.game_is_running:
        return
        # return render_template('fight.html', heroes=arena)

    arena.player_hit()
    battle_result = "" if arena.battle_result == None else arena.battle_result
    return render_template('fight.html', heroes=arena, result=list(reversed(arena.log)), battle_result=battle_result)


@app.route("/fight/use-skill")
def use_skill():
    if not arena.game_is_running:
        return render_template('fight.html', heroes=arena)

    arena.player_use_skill()
    battle_result = "" if arena.battle_result == None else arena.battle_result
    return render_template('fight.html', heroes=arena, result=list(reversed(arena.log)), battle_result=battle_result)


@app.route("/fight/pass-turn")
def pass_turn():
    if not arena.game_is_running:
        return render_template('fight.html', heroes=arena)

    arena.next_turn()
    return render_template('fight.html', heroes=arena, result=list(reversed(arena.log)), battle_result=arena.battle_result)


@app.route("/fight/end-fight")
def end_fight():
    heroes = {}
    return render_template("index.html")


@app.route("/choose-hero/", methods=['POST', 'GET'])
def choose_hero():
    result = {
        "header": "Choose your hero!",
        "classes": list(unit_classes.keys()),
        "weapons": equipment.get_weapons_names(),
        "armors": equipment.get_armors_names()
    }

    if request.method == "GET":
        return render_template("hero_choosing.html", result=result)
    elif request.method == "POST":
        name = request.form["name"]
        if name == "":
            name = "Unknown warior"
        unit_class_name = request.form["unit_class"]
        weapon_name = request.form["weapon"]
        armor_name = request.form["armor"]

        if None in [name, unit_class_name, weapon_name, armor_name]:
            return None
        unit_class = unit_classes[unit_class_name]

        player = PlayerUnit(name=name, unit_class=unit_class)
        player.equip_armor(equipment.get_armor(armor_name=armor_name))
        player.equip_weapon(equipment.get_weapon(weapon_name=weapon_name))
        if player is None:
            return render_template("hero_choosing.html", result=result)

        heroes["player"] = player
        return redirect('/choose-enemy/')


@app.route("/choose-enemy/", methods=['post', 'get'])
def choose_enemy():
    result = {
        "header": "Choose your Enemy!",
        "classes": list(unit_classes.keys()),
        "weapons": equipment.get_weapons_names(),
        "armors": equipment.get_armors_names()
    }

    if request.method == "GET":
        return render_template("hero_choosing.html", result=result)
    elif request.method == "POST":
        name = request.form["name"]
        if name == "":
            name = "Unknown warior"
        unit_class_name = request.form["unit_class"]
        weapon_name = request.form["weapon"]
        armor_name = request.form["armor"]

        if None in [name, unit_class_name, weapon_name, armor_name]:
            return None
        unit_class = unit_classes[unit_class_name]

        enemy = PlayerUnit(name=name, unit_class=unit_class)
        enemy.equip_armor(equipment.get_armor(armor_name=armor_name))
        enemy.equip_weapon(equipment.get_weapon(weapon_name=weapon_name))
        if enemy is None:
            return render_template("hero_choosing.html", result=result)

        heroes["enemy"] = enemy

        return redirect('/fight/')


if __name__ == "__main__":
    app.run()
