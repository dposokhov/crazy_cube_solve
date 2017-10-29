# -*- coding: utf-8 -*-
import telebot
import kociemba

token = 'TOKEN'

bot = telebot.TeleBot(token)

markup = telebot.types.ReplyKeyboardMarkup()
markup.row_width
markup.row('/help', '/example')


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    start = 'https://github.com/dposokhov/kubik_solve_tlgrm \n' \
            'На вход бот получает строку из 54 символов. Если бы кубик рубика был собран, то это строка \n' \
            'выглядела бы так UUUUUUUUURRRRRRRRRFFFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'
    bot.send_message(message.chat.id, start, reply_markup=markup)


@bot.message_handler(commands=['example'])
def print_example(message):
    example = 'UFRDUFBRFDDULRBFLBDBLDFBLFDUURFDURUDLBRRLLBRFFLBUBDLRU'
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(example) and len(example) == 54:
        bot.send_message(message.chat.id, 'Пример входной строки: \n /solve {}'.format(example))
        out = kociemba.solve(example)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, 'Введены неверные входные данные')


@bot.message_handler(commands=['solve'])
def solve(message):
    data = message.text.split()[-1]
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(message.text.split()[-1])
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
    else:
        bot.send_message(message.chat.id, 'Введены неверные входные данные', reply_markup=markup)


if __name__ == '__main__':
    bot.polling(none_stop=True)
