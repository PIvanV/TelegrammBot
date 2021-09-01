import json
import requests

from config import exchanger

class ConverterException(Exception):
    pass

class Convertor:
    @staticmethod
    def get_price(values):
        if len(values) != 3:
            raise ConverterException("Неверное количество параметров")
        quote, base, amount = values

        if quote == base:
            raise ConverterException(f'Невозможно перевести одинаковые валюты {base}')

        try:
            quote_formatted = exchanger[quote]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {quote}')

        try:
            base_formatted = exchanger[base]
        except KeyError:
            raise ConverterException(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConverterException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?'
                         f'access_key=1b5fee2ad65271cac40d46ac53803533&format=1'
                         f'&base={quote_formatted}'
                         f'&symbol={base_formatted}')

        result = float(json.loads(r.content)['rates'][base_formatted]) * amount

        return round(result, 3)
