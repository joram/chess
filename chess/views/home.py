from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from chess.models import Game, Move

from bots.angry_bot import AngryBot
from bots.random_bot import RandomBot


def create(request):
    destroy(request)
    bot_a_cmd = ["python", "./bots/angry_bot.py"]
    bot_b_cmd = ["python", "./bots/random_bot.py"]
    Game.objects.create_for_cmds(bot_a_cmd, "Angry Bot", bot_b_cmd, "Random Bot")
    return HttpResponse()


def destroy(request):
    Game.objects.all().delete()
    return HttpResponse()


def home(request):
    latest_game_id = list(Game.objects.all())[-1].id
    return game(request, latest_game_id)


def game(request, game_id):
    game = get_object_or_404(Game, id=game_id)
    context = {
        "game": game,
    }
    return render_to_response("game.html", context)


def board_state(request, game_id, move_index):

    try:
        move_index = int(move_index)
    except ValueError:
        move_index = 0

    game = get_object_or_404(Game, id=game_id)
    if game.moves_count < move_index:
        move_index = 0

    move = game.moves[move_index]
    context = {"board_state": move.board_state}
    return render_to_response("board.html", context)


