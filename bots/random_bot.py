from board import Board
from bots.bot import ChessBot
import random


class RandomBot(ChessBot):

    def __str__(self):
        return "Random Bot"

    def move(self, board):
        if type(board) == str:
            board = Board(board_string=board)
        possible_moves = board.possible_moves(self.colour)
        if len(possible_moves) > 0:
            return random.choice(possible_moves)

if __name__ == "__main__":
    RandomBot().cmd_move()