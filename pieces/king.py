from pieces.piece import Piece


class King(Piece):
    def __init__(self, colour, position, board):
        Piece.__init__(self, "king", colour, position, board)
        self.directions = [(x, y) for x in [-1, 0, 1] for y in [-1, 0, 1]]

    def _beside_other_king(self, position):
        other_king_class = WhiteKing if self.opposing_colour == "white" else BlackKing
        other_king = self.board.get_piece(other_king_class)
        for offset in self.directions:
            beside_other_king_position = (other_king.position[0]+offset[0], other_king.position[1]+offset[1])
            if position == beside_other_king_position:
                return True

    def possible_moves(self):
        # TODO, make so the king doesn't move into threated squares.
        possible_moves = []

        for offset in self.directions:
            new_position = (self.position[0]+offset[0], self.position[1]+offset[1])
            if self._within_board(new_position) and not self.board.square_occupied_by(new_position, self.colour):
                old_position = self.position
                self.position = new_position

                if not self.board.threatened(self, ignore_kings=True):
                    possible_moves.append(new_position)
                self.position = old_position

        return possible_moves


class WhiteKing(King):
    def __init__(self, position, board):
        King.__init__(self, "white", position, board)


class BlackKing(King):
    def __init__(self, position, board):
        King.__init__(self, "black", position, board)
