from pieces.piece import Piece


class Knight(Piece):
    def __init__(self, colour, position, board):
        Piece.__init__(self, "knight", colour, position, board)

    def possible_moves(self, recurse=0):
        possible_offsets = [(1, 2), (-1, 2), (1, -2), (-1, -2),
                            (2, 1), (-2, 1), (2, -1), (-2, -1)]

        possible_moves = []
        for offset in possible_offsets:
            new_position = (self.position[0] + offset[0], self.position[1] + offset[1])
            if self._within_board(new_position) and not self.board.square_occupied_by(new_position, self.colour):
                possible_moves.append(new_position)
        return possible_moves


class WhiteKnight(Knight):
    def __init__(self, position, board):
        Knight.__init__(self, "white", position, board)


class BlackKnight(Knight):
    def __init__(self, position, board):
        Knight.__init__(self, "black", position, board)
