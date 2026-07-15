from core.game import Game
from entities.player import Player
from entities.effects import SpeedBoostEffect


game = Game()
hunter = Player("Hunter", "hunter", game)

game.switch_state(game.playing_state)

hunter.position = (100, 100)
hunter.attempt_set_movement_effect(SpeedBoostEffect(2.0))
hunter.attempt_move((101, 100))

print(hunter.position)
assert hunter.position == (102, 100)

 
