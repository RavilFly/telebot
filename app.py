import telebot
from config import currency, TOKEN
from extensions import APIException, CurrencyConverter



bot = telebot.TeleBot(TOKEN)


#стартовый обработчик, выводит начальные инструкции
@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Для того, что бы узнать доступные валюты\n' \
           'введите команду в формате /values .\n' \
           'Чтобы узнать формат запроса введите /help .'
    bot.reply_to(message, text)

#обработчик помощи, выводит инструкции для пользователя
@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = 'Для запроса стоимости конвертации введите:\n' \
           '<Имя валюты> <В какую валюту> <Количество>\n' \
           'Если количество не вводить, Вы просто получите\n' \
           'текущий курс. Примеры ввода: "евро рубль 150"\n' \
           '"доллар юань".'
    bot.reply_to(message, text)

#выводит все доступные валюты
@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in currency.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)

#обработчик с основной логикой, принимает данные и выводит результаты
@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')#разберем переданные данные в список
        if len(values) == 3:#если параметра три, то отправляем запрос с количеством
            quote, base, amount = values
            result = CurrencyConverter.get_price(quote, base, amount)
        elif len(values) == 2:#если параметра два, отправим запрос только на курс
            quote, base = values
            amount = None#на всякий случай очистим
            rate = CurrencyConverter.get_price(quote, base)

        else:#если параметров больше 3 или меньше 2
            raise APIException('Недопустимое количество параметров')

    except APIException as e:
        bot.reply_to(message,f'Ошибка пользователя \n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду \n{e}')
    else:#вывод итогового сообщения в зависимости - был ли запрос с количеством или без
        if amount:
            text = f'Цена {amount} {quote} за {base} равна {result}.'
        else:
            text = f'Курс {quote} к {base} равен {rate}.'
        bot.send_message(message.chat.id, text)


bot.polling()