import telebot
from config import TOKEN, exchanger
from extensions import Convertor, ConverterException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = r"""/values - список доступных валют,
валюта1 валюта2 сумма - перевод суммы из валюты1 в валюту2"""
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    text += '\n'.join(f"{i + 1}) {key}" for i, key in enumerate(exchanger.keys()))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    values = message.text.split(' ')
    values = list(map(str.lower, values))
    try:
        result = Convertor.get_price(values)
    except ConverterException as e:
        bot.reply_to(message, f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:
        text = f'Цена {values[2]} {values[0]} в {values[1]} -- {result} {exchanger[values[1]]}'
        bot.reply_to(message, text)

bot.polling(none_stop=True, interval=0)


