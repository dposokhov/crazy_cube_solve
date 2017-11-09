# -*- coding: utf-8 -*-
import telebot
import kociemba

token = 'TOKEN'
bot = telebot.TeleBot(token)

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
Если бы кубик рубика был собран, то строка выглядела бы так
UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB
/color-solve
На вход бот получает строку из 54 символов.                
Кубик расположить White == Up, Blue == Front, Red == Left             
White, Orange, Blue, Yellow, Red, Green.                   
WWWWWWWWWOOOOOOOOOBBBBBBBBBYYYYYYYYYRRRRRRRRRGGGGGGGGG     
THE=====END      
                                                                """
    bot.send_message(message.chat.id, start, reply_markup=markup)


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


@bot.message_handler(commands=['solve'])
def solve(message):
    data = message.text.split()[-1].upper()
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, str(len(out.split()))+' хода')
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
        bot.send_message(message.chat.id, str(len(out.split()))+' хода')
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
    for old, new in (('W', 'U'), ('B', 'F'), ('R', 'L'), ('O', 'R'), ('G', 'B'), ('Y', 'D')):
        data = data.replace(old, new)
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.send_message(message.chat.id, str(len(out.split()))+' хода')
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
    for old, new in (('W', 'U'), ('B', 'F'), ('R', 'L'), ('O', 'R'), ('G', 'B'), ('Y', 'D')):
        data = data.replace(old, new)
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        bot.send_message(message.chat.id, str(len(out.split()))+' хода')
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
