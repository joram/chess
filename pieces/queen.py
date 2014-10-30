from pieces.piece import SlidingPiece


class Queen(SlidingPiece):
    def __init__(self, colour, position, board):
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),  # straights
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]  # and diagonals
        SlidingPiece.__init__(self, "queen", colour, position, board, directions)


class WhiteQueen(Queen):
    def __init__(self, position, board):
        Queen.__init__(self, "white", position, board)


class BlackQueen(Queen):
    def __init__(self, position, board):
        Queen.__init__(self, "black", position, board)
