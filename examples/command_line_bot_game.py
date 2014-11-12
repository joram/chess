from play_game import play_command_line

bot_a_cmd = ["python", "./bots/angry_bot.py"]
bot_b_cmd = ["python", "./bots/random_bot.py"]
play_command_line(bot_a_cmd, bot_a_cmd, "Angry_1", "Angry_2", 20)

