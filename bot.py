import random
import telebot
from telebot import types


bot = telebot.TeleBot('5496966751:AAEO-KaDYhZpTO5K26YmmRwKEnXiSAHkY68')

board = ' -------------- \n ' \
        '| 1 | 2 | 3 | \n ' \
        '-------------- \n ' \
        '| 4 | 5 | 6 | \n ' \
        '-------------- \n ' \
        '| 7 | 8 | 9 | \n ' \
        '-------------- \n'

change_board = board
players_moves = []
pc_moves = []
all_moves: list = []
msg = None

win = False
win_list = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9], [1, 5, 9], [3, 5, 7]]


@bot.message_handler(commands=['start', 'info'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Я бот, который умеет играть в крестики-нолики. Если хочешь сыграть со мной, напиши /start_game.")


@bot.message_handler(commands=['end'])
def end_game(message):
    bot.send_message(message.chat.id,
                     "Жаль, мне так нравилось с тобой играть :( Жду тебя на новую игру!"
                     "\n P.S.: Чтобы сыграть снова, напиши /start_game")


@bot.message_handler(commands=['start_game'])
def handle_msg(message):
    global msg, change_board
    change_board = board
    all_moves.clear()
    pc_moves.clear()
    players_moves.clear()
    bot.send_message(message.chat.id, f"{change_board}\nВаш ход: ")
    msg = message
    bot.register_next_step_handler(msg, player_turn)


def player_turn(message):
    # Player move
    global change_board, msg
    player_move = int(message.text)
    while player_move in all_moves:
        bot.reply_to(message, "Похоже это место уже занято. Выберите другое поле.")
        return handle_msg(message)
    players_moves.append(player_move)
    all_moves.append(player_move)
    change_board = change_board.replace(str(player_move), 'X')
    for i in win_list:
        if i[0] in players_moves and i[1] in players_moves and i[2] in players_moves:
            bot.send_message(message.chat.id, "Вы победили, поздравляем!")
            bot.send_message(message.chat.id, change_board)
            return end_game(message)

    # PC move
    pc_move = random.randint(1, 9)
    while pc_move in all_moves:
        pc_move = random.randint(1, 9)
    bot.send_message(message.chat.id, f"Ход компьютера: {pc_move}")
    pc_moves.append(pc_move)
    all_moves.append(pc_move)
    change_board = change_board.replace(str(pc_move), 'O')
    bot.send_message(message.chat.id, change_board)
    for i in win_list:
        if i[0] in pc_moves and i[1] in pc_moves and i[2] in pc_moves:
            bot.send_message(message.chat.id, "Вы проиграли( Попробуйте еще раз.")
            bot.send_message(message.chat.id, change_board)
            return end_game(message)
    bot.register_next_step_handler(message, player_turn)


bot.infinity_polling()
