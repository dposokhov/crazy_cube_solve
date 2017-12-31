# -*- coding: utf-8 -*-
import telebot
import kociemba
import config
import botan
import datetime
import cherrypy


WEBHOOK_HOST = 'IP-адрес сервера, на котором запущен бот'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (config.token)

bot = telebot.TeleBot(config.token)

markup = telebot.types.ReplyKeyboardMarkup(True, False)

markup.row('/help', '/example_of_message')
markup.row('/#solve', '/#color-solve')
markup.row('/#text-solve', '/#text-color-solve')

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(func=lambda message: True, wcommands=['start', 'help'])
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
Нужно построчно ввести все цвета с граней в такой последовательности: 
Up, Right, Front, Down, Left, Back 

                THE=====END      
                                                                """
    bot.reply_to(message, start, reply_markup=markup)
    botan.track(config.botan_key, message.chat.id, message, 'start')


@bot.message_handler(func=lambda message: True, commands=['#solve', '#color-solve', '#text-solve', '#text-color-solve'])
def print_text(message):
    text_example = """
/solve {U, R, F, D, L, B} -> output text and photos
/text-solve {U, R, F, D, L, B} -> output text
/color-solve {W, B, R, O, G, Y} -> output text and photos      
/text-color-solve {W, B, R, O, G, Y} -> output text    
        """
    bot.reply_to(message, text_example)


@bot.message_handler(func=lambda message: True, commands=['example_of_message'])
def print_example(message):
    example = 'UFRDUFBRFDDULRBFLBDBLDFBLFDUURFDURUDLBRRLLBRFFLBUBDLRU'
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(example) and len(example) == 54:
        bot.send_message(message.chat.id, 'Пример входной строки: \n /solve {}'.format(example))
        out = kociemba.solve(example)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.reply_to(message, str(len(out.split()))+' steps')


@bot.message_handler(func=lambda message: True, commands=['solve'])
def solve(message):
    f = open('log.txt', 'a')
    f.write('\n {}: {} -> {} \n'.format(str(datetime.datetime.now()), message.chat.username, message.text))
    f.close()
    data = message.text.split()[-1].upper()
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.send_message(message.chat.id, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.reply_to(message, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'solve')
    else:
        if len(data) > 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.reply_to(message, 'Введены неверные входные данные: Должно быть {U, R, F, D, L, B}',
                             reply_markup=markup)


@bot.message_handler(func=lambda message: True, commands=['text-solve'])
def solve(message):
    f = open('log.txt', 'a')
    f.write('\n {}: {} -> {} \n'.format(str(datetime.datetime.now()), message.chat.username, message.text))
    f.close()
    data = message.text.split()[-1].upper()
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.reply_to(message, out, reply_markup=markup)
        bot.reply_to(message, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'solve')
    else:
        if len(data) > 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.reply_to(message, 'Введены неверные входные данные: Должно быть {U, R, F, D, L, B}',
                             reply_markup=markup)


@bot.message_handler(func=lambda message: True, commands=['color-solve'])
def solve(message):
    f = open('log.txt', 'a')
    f.write('\n {}: {} -> {} \n'.format(str(datetime.datetime.now()), message.chat.username, message.text))
    f.close()
    data = message.text.split()[-1].upper()
    for old, new in ((data[4], 'U'), (data[22], 'F'), (data[40], 'L'), (data[13], 'R'), (data[49], 'B'), (data[31], 'D')):
        data = data.replace(old, new)
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.reply_to(message, out, reply_markup=markup)
        for item in out.split():
            f = open('./kubik/{}.jpg'.format(item), 'rb')
            bot.send_photo(message.chat.id, f)
        bot.reply_to(message, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'color-solve')
    else:
        if len(data) > 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.reply_to(message, 'Введены неверные входные данные: Должно быть {W, B, R, O, G, Y}',
                             reply_markup=markup)


@bot.message_handler(func=lambda message: True, commands=['text-color-solve'])
def solve(message):
    f = open('log.txt', 'a')
    f.write('\n {}: {} -> {} \n'.format(str(datetime.datetime.now()), message.chat.username, message.text))
    f.close()
    data = message.text.split()[-1].upper()
    for old, new in ((data[4], 'U'), (data[22], 'F'), (data[40], 'L'), (data[13], 'R'), (data[49], 'B'), (data[31], 'D')):
        data = data.replace(old, new)
    if 'U' and 'R' and 'F' and 'D' and 'L' and 'B' in list(data) and len(data) == 54:
        out = kociemba.solve(data)
        bot.reply_to(message, out, reply_markup=markup)
        bot.reply_to(message, str(len(out.split()))+' steps')
        botan.track(config.botan_key, message.chat.id, message, 'color-solve')
    else:
        if len(data) > 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит > 54 символов',
                             reply_markup=markup)
        elif len(data) < 54:
            bot.reply_to(message, 'Введены неверные входные данные: Строка содержит < 54 символов',
                             reply_markup=markup)
        else:
            bot.reply_to(message, 'Введены неверные входные данные: Должно быть {W, B, R, O, G, Y}',
                             reply_markup=markup)


bot.remove_webhook()

bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
