from pieces.piece import Piece


class King(Piece):
    def __init__(self, colour, position, board):
        Piece.__init__(self, "king", colour, position, board)

    def possible_moves(self):
        possible_moves = []
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),  # straights
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # and diagonals
        for offset in directions:
            new_position = (self.position[0]+offset[0], self.position[1]+offset[1])
            if self._within_board(new_position) and not self.board.square_occupied_by(new_position, self.colour):
                possible_moves.append(new_position)

        return possible_moves


class WhiteKing(King):
    def __init__(self, position, board):
        King.__init__(self, "white", position, board)


class BlackKing(King):
    def __init__(self, position, board):
        King.__init__(self, "black", position, board)
