from core.game import Game
from entities.player import Player
from entities.weapon import Gun


if __name__ == "__main__":
    game = Game()

    hunter = Player("Hunter 1", "hunter", game)
    prop = Player("Prop 1", "prop", game)

    glock = Gun("Glock 17")
    ar15 = Gun("AR-15")

    hunter.attempt_pickup_weapon(glock)
    hunter.attempt_use_weapon()

    hunter.attempt_switch_slot("secondary")
    hunter.attempt_pickup_weapon(ar15)
    hunter.attempt_use_weapon()

    game.switch_state(game.playing_state)
    hunter.attempt_use_weapon()
