from django.shortcuts import render_to_response
from board import Board


def home(request):
    board = Board()
    board.start_board()
    context = {
        "board_state": board.state()
    }
    return render_to_response("game.html", context)