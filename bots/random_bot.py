from bots.bot import ChessBot
import random


class RandomBot(ChessBot):

    def __str__(self):
        return "Random Bot"

    def move(self, board):
        possible_moves = board.possible_moves(self.colour)
        return random.choice(possible_moves)