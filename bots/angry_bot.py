from bots.bot import ChessBot
from board import Board
import random


class AngryBot(ChessBot):

    def __str__(self):
        return "Angry Bot"

    def move(self, board):
        if type(board) == str:
            board = Board(board_string=board)

        taking_moves = {}
        possible_moves = board.possible_moves(self.colour)
        if len(possible_moves) > 0:
            for possible_move in possible_moves:
                temp_board = board.duplicate()
                taken_piece = temp_board.move(possible_move)
                if taken_piece:
                    taking_moves[possible_move] = taken_piece

            if len(taking_moves) > 0:
                chosen_move = random.choice(taking_moves.keys())
            else:
                chosen_move = random.choice(possible_moves)

            return chosen_move

if __name__ == "__main__":
    AngryBot().cmd_move()