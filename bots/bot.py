from sys import stdin, stdout
from chess.helpers import coords_to_alpha_numeric


class ChessBot():

    def __init__(self, colour="unknown"):
        self.colour = colour

    def move(self, board):
        pass

    def cmd_move(self):
        line = stdin.readline()
        (colour, board) = line.split(" ")
        self.colour = colour
        move = self.move(board)
        if move:
            ((x1, y1), (x2, y2)) = move
            move_str = "%s%s" % (coords_to_alpha_numeric(x1, y1), coords_to_alpha_numeric(x2, y2))
            print move_str