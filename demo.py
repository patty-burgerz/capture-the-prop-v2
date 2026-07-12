from core.game import Game
from entities.player import Player
from entities.weapons.gun import Gun
from entities.weapons.gun_library import GLOCK_17
from entities.weapons.gun_library import AR_15

from entities.weapons.shot_modifiers import DoubleDamageModifier

if __name__ == "__main__":
    print("Hello from demo.py!")

    game = Game()

    hunter = Player("Hunter 1", "hunter", game)
    #prop = Player("Prop 1", "prop", game)

    #glock = Gun(GLOCK_17)
    ar15 = Gun(AR_15)
    

    #hunter.attempt_pickup_weapon(glock)
    #hunter.attempt_use_weapon()
    #hunter.attempt_use_weapon()
    #game.update(.1)

    #hunter.attempt_switch_slot("secondary")
    #hunter.add_shot_modifier(DoubleDamageModifier())
    hunter.attempt_pickup_weapon(ar15)
    #hunter.attempt_use_weapon()

    game.switch_state(game.playing_state)
    
    hunter.attempt_use_weapon()
    hunter.add_shot_modifier(DoubleDamageModifier())
    hunter.attempt_use_weapon()
 
