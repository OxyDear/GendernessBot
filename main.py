import telebot
from telebot import types
import config
import random
from translate.translate import Translator

bot = telebot.TeleBot(config.TOKEN)
name = None
lang_code = 'ru'
translator = Translator(from_lang='ru', to_lang=lang_code)


@bot.message_handler(commands=['start'])
def main(msg):
    global lang_code
    lang_code = msg.from_user.language_code
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Share your genderness🥰", switch_inline_query=''))
    bot.send_message(msg.chat.id, "hello", reply_markup=markup)


@bot.message_handler(commands=['help'])
def helping(msg):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Share your genderness🥰", switch_inline_query=''))
    bot.send_message(msg.chat.id, config.HELPISITY, reply_markup=markup)


@bot.message_handler(commands=['changelang'])
def change_lang(msg):
    global translator
    translator = Translator(from_lang='ru', to_lang=lang_code)
    lang_name = translator.translate(config.CHANGE_LANG)
    bot.send_message(msg.chat.id, lang_name)
    bot.register_next_step_handler(msg, set_lang)


def set_lang(msg):
    global lang_code
    lang_code = msg.text
    bot.send_message(msg.chat.id, "Completed!")


@bot.inline_handler(lambda query: query.query == '')
def query_text(inline_query):
    with open('genders.txt', 'r') as file:
        src = file.read().split()

    try:
        translator = Translator(from_lang='ru', to_lang=lang_code)
        phrase = translator.translate(config.PHRASE)
        helpisity = translator.translate(config.HELPISITY)
        genderName = translator.translate(random.choice(src))
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Share your genderness🥰", switch_inline_query=''))
        gender = types.InlineQueryResultArticle('1', 'Genderness', types.InputTextMessageContent(
            phrase.format(random.randint(1, 100), genderName)),
                                    thumbnail_url="https://m.media-amazon.com/images/I/61XmTyKs7sL._AC_SL1000_.jpg",
                                    thumbnail_height=1000, thumbnail_width=1000, reply_markup=markup)
        helping = types.InlineQueryResultArticle('2', 'Helpisity', types.InputTextMessageContent(
            helpisity), thumbnail_url="https://m.media-amazon.com/images/I/61XmTyKs7sL._AC_SL1000_.jpg",
                                    thumbnail_height=1000, thumbnail_width=1000, reply_markup=markup)
        bot.answer_inline_query(inline_query.id, [gender, helping], cache_time=0)
    except Exception as e:
        print(e)


@bot.inline_handler(lambda query: query)
def query_text2(inline_query):
    with open('genders.txt', 'r') as file:
        src = file.read().split()

    try:
        translator = Translator(from_lang='ru', to_lang=lang_code)
        phrase = translator.translate(config.PHRASE2)
        genderName = translator.translate(random.choice(src))
        helpisity = translator.translate(config.HELPISITY)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Share your genderness🥰", switch_inline_query=''))
        gender = types.InlineQueryResultArticle('1', 'Genderness', types.InputTextMessageContent(
            phrase.format(inline_query.query, random.randint(1, 100), genderName)),
                                                thumbnail_url="https://m.media-amazon.com/images/I/61XmTyKs7sL._AC_SL1000_.jpg",
                                                thumbnail_height=1000, thumbnail_width=1000, reply_markup=markup)
        helping = types.InlineQueryResultArticle('2', 'Helpisity', types.InputTextMessageContent(
            helpisity), thumbnail_url="https://m.media-amazon.com/images/I/61XmTyKs7sL._AC_SL1000_.jpg",
                                                 thumbnail_height=1000, thumbnail_width=1000, reply_markup=markup)
        bot.answer_inline_query(inline_query.id, [gender, helping], cache_time=0)
    except Exception as e:
        print(e)


bot.infinity_polling()
