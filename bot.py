# -*- coding: utf-8 -*-
import telebot
import kociemba
import config
import botan

bot = telebot.TeleBot(config.token)

markup = telebot.types.ReplyKeyboardMarkup(True, False)

markup.row('/help', '/example_of_message')
markup.row('/#solve', '/#color-solve')
markup.row('/#text-solve', '/#text-color-solve')


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    start = """
https://github.com/dposokhov/crazy_cube_solve

/solve:
На вход бот получает строку из 54 символов.
UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB

/color-solve
На вход бот получает строку из 54 символов.                
WWWWWWWWWOOOOOOOOOBBBBBBBBBYYYYYYYYYRRRRRRRRRGGGGGGGGG
Кубик нужно расположить
White == Up 
Blue == Front 
Red == Left                     
Нужно построчно ввести все цвета с граней в такой последовательности: 
Up, Right, Front, Down, Left, Back 

                THE=====END      
                                                                """
    bot.send_message(message.chat.id, start, reply_markup=markup)
    botan.track(config.botan_key, message.chat.id, message, 'start')


@bot.message_handler(commands=['#solve', '#color-solve', '#text-solve', '#text-color-solve'])
def print_text(message):
    text_example = """
/solve {U, R, F, D, L, B} -> output text and photos
/text-solve {U, R, F, D, L, B} -> output text
/color-solve {W, B, R, O, G, Y} -> output text and photos      
/text-color-solve {W, B, R, O, G, Y} -> output text    
        """
    bot.send_message(message.chat.id, text_example)


@bot.message_handler(commands=['example_of_message'])
def print_example(message):
    example = 'UFRDUFBRFDDULRBFLBDBLDFBLFDUURFDURUDLBRRLLBRFFLBUBDLRU'
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(example) and len(example) == 54:
        bot.send_message(message.chat.id, 'Пример входной строки: \n /solve {}'.format(example))
        out = kociemba.solve(example)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, str(len(out.split()))+' steps')


@bot.message_handler(commands=['solve'])
def solve(message):
    data = message.text.split()[-1].upper()
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'solve')
    else:
        if len(data) > 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Должно быть {U, R, F, D, L, B}',
                             reply_markup=markup)


@bot.message_handler(commands=['text-solve'])
def solve(message):
    data = message.text.split()[-1].upper()
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        bot.send_message(message.chat.id, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'solve')
    else:
        if len(data) > 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Должно быть {U, R, F, D, L, B}',
                             reply_markup=markup)


@bot.message_handler(commands=['color-solve'])
def solve(message):
    data = message.text.split()[-1].upper()
    for old, new in ((data[4], 'U'), (data[22], 'F'), (data[40], 'L'), (data[13], 'R'), (data[49], 'B'), (data[31], 'D')):
        data = data.replace(old, new)
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'color-solve')
    else:
        if len(data) > 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Должно быть {W, B, R, O, G, Y}',
                             reply_markup=markup)


@bot.message_handler(commands=['text-color-solve'])
def solve(message):
    data = message.text.split()[-1].upper()
    for old, new in ((data[4], 'U'), (data[22], 'F'), (data[40], 'L'), (data[13], 'R'), (data[49], 'B'), (data[31], 'D')):
        data = data.replace(old, new)
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        bot.send_message(message.chat.id, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'color-solve')
    else:
        if len(data) > 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, 'Введены неверные входные данные: Должно быть {W, B, R, O, G, Y}',
                             reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
