from pieces.piece import Piece


class King(Piece):
    def __init__(self, colour, position, board):
        Piece.__init__(self, "king", colour, position, board)

    def possible_moves(self, recurse=5):
        # TODO, make so the king doesn't move into threated squares.
        possible_moves = []
        directions = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]
        # [(0, 1), (0, -1), (1, 0), (-1, 0),  # straights
        #               (1, 1), (1, -1), (-1, 1), (-1, -1)]  # and diagonals

        if recurse == 0:
            return []

        for offset in directions:
            new_position = (self.position[0]+offset[0], self.position[1]+offset[1])
            if self._within_board(new_position) and not self.board.square_occupied_by(new_position, self.colour):
                old_position = self.position
                self.position = new_position
                if not self.board.threatened(self, recurse-1):
                    possible_moves.append(new_position)
                self.position = old_position

        return possible_moves


class WhiteKing(King):
    def __init__(self, position, board):
        King.__init__(self, "white", position, board)


class BlackKing(King):
    def __init__(self, position, board):
        King.__init__(self, "black", position, board)
