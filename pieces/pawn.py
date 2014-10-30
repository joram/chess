from pieces.piece import Piece


class Pawn(Piece):
    def __init__(self, colour, position, board):
        Piece.__init__(self, "pawn", colour, position, board)

    def possible_moves(self):
        possible_moves = []
        (x, y) = self.position

        forward_one = (x, y+self.direction)
        forward_one_not_occupied = not self.board.square_occupied(forward_one)
        if forward_one_not_occupied and self._within_board(forward_one):
            possible_moves.append(forward_one)

        forward_two = (x, y+2*self.direction)
        forward_two_not_occupied = not self.board.square_occupied(forward_two)
        if y == 2 and self.colour == "white" and forward_one_not_occupied and forward_two_not_occupied:
            possible_moves.append(forward_two)

        diagonal_left = (x-1, y+self.direction)
        if self._within_board(diagonal_left) and self.board.square_occupied_by(diagonal_left, self.opposing_colour):
            possible_moves.append(diagonal_left)

        diagonal_right = (x+1, y+self.direction)
        if self._within_board(diagonal_right) and self.board.square_occupied_by(diagonal_right, self.opposing_colour):
            possible_moves.append(diagonal_right)

        return possible_moves


class WhitePawn(Pawn):
    def __init__(self, position, board):
        Pawn.__init__(self, "white", position, board)


class BlackPawn(Pawn):
    def __init__(self, position, board):
        Pawn.__init__(self, "black", position, board)
