import telebot
from telebot import types
import main
from Meta import meta_predictes
from NvidiaPredicates import nvda_filename
from ApplePredicates import apple_filename
from TeslaPredicates import tesla_filename

token = "6274738419:AAGFD9Fb28v0fquvJk-2v6_mib7dKCFGH9c"
telBot = telebot.TeleBot(token)


@telBot.message_handler(commands=['get_info', 'info'])
def get_predicates_nvidia(message):
    markup_inline = types.InlineKeyboardMarkup()
    item_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    item_no = types.InlineKeyboardButton(text='Нет', callback_data='no')

    markup_inline.add(item_yes, item_no)
    telBot.send_message(message.chat.id, 'Хотите получить прогноз ?', reply_markup=markup_inline)


@telBot.callback_query_handler(func=lambda call: True)
def answer(call):
    if call.data == 'yes':
        markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item_nvidia = types.KeyboardButton('Акции Nvidia')
        item_apple = types.KeyboardButton('Акции Aplle и Nvidia')
        item_tesla = types.KeyboardButton('Акции Aplle, Nvidia, Tesla')
        item_new_predict = types.KeyboardButton('Прогноз на акции Мета')

        markup_reply.add(item_nvidia, item_apple, item_tesla, item_new_predict)
        telBot.send_message(call.message.chat.id, 'Нажмите на одну из кнопок', reply_markup=markup_reply)



@telBot.message_handler(content_types=['text'])
def get_text(message):
    if message.text == 'Акции Nvidia':
        with open(nvda_filename, "rb") as f:
            telBot.send_photo(message.chat.id, f)
    elif message.text == 'Акции Aplle и Nvidia':
        with open(apple_filename, "rb") as f:
            telBot.send_photo(message.chat.id, f)
    elif message.text == 'Акции Aplle, Nvidia, Tesla':
        with open(tesla_filename, "rb") as f:
            telBot.send_photo(message.chat.id, f)
    elif message.text == 'Прогноз на акции Мета':
        with open(meta_predictes, "rb") as f:
            telBot.send_photo(message.chat.id, f)


# @telBot.message_handler(commands=['start'])
# def start(message):
#      telBot.send_message(message.chat.id, "Происходит анализ данных, немного подождите")
#
# @telBot.message_handler(commands=['predictprices'])
# def predictprices(message):
#      telBot.send_message(message.chat.id, "Ближайший прогноз цен на акции Nvidia: ")
#
#      with open(nvda_filename, "rb") as f:
#         telBot.send_photo(message.chat.id, f)
#
#
# @telBot.message_handler(commands=['predictapple'])
# def predictapple(message):
#      telBot.send_message(message.chat.id, "Ближайший прогноз цен на акции Apple: ")
#
#      with open(apple_filename, "rb") as f:
#         telBot.send_photo(message.chat.id, f)


telBot.infinity_polling()
