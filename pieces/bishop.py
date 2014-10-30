from pieces.piece import SlidingPiece


class Bishop(SlidingPiece):
    def __init__(self, colour, position, board):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]
        SlidingPiece.__init__(self, "bishop", colour, position, board, directions)


class WhiteBishop(Bishop):
    def __init__(self, position, board):
        Bishop.__init__(self, "white", position, board)


class BlackBishop(Bishop):
    def __init__(self, position, board):
        Bishop.__init__(self, "black", position, board)
