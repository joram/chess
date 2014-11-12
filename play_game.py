import subprocess
from pieces.king import King

def play_single_game(player_1, player_2, debug=False):
    from board import Board
    board = Board()
    board.start_board()
    while not board.game_over:
        for player in [player_1, player_2]:
            if not board.game_over:
                other_colour = "white" if player['colour'] == "black" else "black"
                input_str = "%s %s\n" % (player['colour'], board.state_str())
                process = subprocess.Popen(player['cmd'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                move = process.communicate(input=input_str)[0]
                if debug:
                    print "%s\t %s %s" % (len(board.move_history), player['colour'], move)

                if len(move) < 4:
                    print "game over because of invalid move"
                    board.game_over = True
                    board.winner = other_colour

                else:
                    move = move[:4]

                    taken_piece = board.move(move)
                    if taken_piece:
                        print "took %s" % taken_piece
                        if isinstance(taken_piece, King):
                            print "took a king"
                            board.game_over = True
                            board.winner = player['colour']

                    # stale mate
                    # if board.possible_moves(other_colour) == []:
                    #     board.game_over = True
                    #     board.winner = player['colour']
    return board


def play_command_line(bot_a_cmd, bot_b_cmd, bot_a_name="Bot A", bot_b_name="Bot B", num_games=20, debug=False):

    player_a = {
        'cmd': bot_a_cmd,
        'name': bot_a_name,
        'wins': 0}

    player_b = {
        'cmd': bot_b_cmd,
        'name': bot_b_name,
        'wins': 0}

    for game_num in range(0, num_games):
        if game_num > num_games/2:
            player_a['colour'] = "black"
            player_b['colour'] = "white"
        else:
            player_a['colour'] = "white"
            player_b['colour'] = "black"

        white_player = player_a if player_a['colour'] == "white" else player_b
        black_player = player_a if player_a['colour'] == "black" else player_b
        board = play_single_game(white_player, black_player, debug)
        winner = player_a if board.winner == player_a['colour'] else player_b
        winner['wins'] += 1

        print "game %d: won by %s (%s) in %s moves" % (game_num, winner['name'], winner['colour'], len(board.move_history))

    for player in [player_a, player_b]:
        print "%s won: %s" % (player['name'], player['wins'])