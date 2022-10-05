from django import template


register = template.Library()

CURRENCIES_SYMBOLS = {
   'rub': '₽',
   'usd': '$',
}


# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def currency(value, code='rub'):
    """
    value: значение, к которому нужно применить фильтр
    """
    postfix = CURRENCIES_SYMBOLS[code]
    # Возвращаемое функцией значение подставится в шаблон.
    return f'{value} {postfix}'

@register.filter()
def censor(value, code='wolf'):
    """
    value: значение, к которому нужно применить фильтр
    """
    len_1 = len(code)-1
    val_1 = value.replace(code, f'{code[0]}{len_1*"*"}')

    return val_1
