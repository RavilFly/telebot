import requests
from config import currency, url

class APIException(Exception):
    pass

class ServerException(Exception):
    pass

class CurrencyConverter:
    @staticmethod
    def get_price(quote, base, amount=None):#основная функция для формирования запроса к API

        if quote == base:#совпадение валюты перевода и базовой
            raise APIException('Нельзя перевести валюту в саму себя')
        #проверяем, есть ли введенные валюты в словаре
        if quote not in currency.keys():
            raise APIException(f'Вы ввели недоступную валюту {quote}.')
        if base not in currency.keys():
            raise APIException(f'Вы ввели недоступную валюту {base}.')

        if amount:#если введено корректное количество отправим запрос на стоимость
            #операции конвертации
            try:
                amount = float(amount)
            except ValueError:
                raise APIException(f'Неверно введено количество {amount}')
            data = requests.get(f'{url}{currency[quote]}/{currency[base]}/{amount}').json()
            if data['result'] == 'success':
                result_ = (data['conversion_result'])
                return result_
        else:#если без количества, запросим и выдадим только курс
            data = requests.get(f'{url}{currency[quote]}/{currency[base]}').json()
            if data['result'] == 'success':
                rate_ = (data['conversion_rate'])
                return rate_
        #если сервер вернет ошибку, передадим в бот ее код
        if data['result'] == 'error':
            raise ServerException(f"Ошибка сервера: {data['error-type']}.")
