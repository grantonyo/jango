from django import template

register = template.Library()


# Это самый простой фильтр, находит слово внутри большого текста, но метод replace не учитывает регистр:
@register.filter()
def censor(value):
    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

    bad_words = ["Редиск", "редиск", "РЕДИСК", "Блин", "блин", "БЛИН", "Хрен", "хрен", "ХРЕН", ]
    a = value

    for x in bad_words:
        a = a.replace(x, x[0] + "*" * (len(x) - 1))
    return a


# Фильтр, приведенный ниже учитывает регистр, но не находит слово внутри другого слова, не учитывает скобки
# или кавычки перед словом и т.д. Поэтому он малоэффективен (хуже предыдущего):
@register.filter()
def censor1(value):
    bad_words_1 = ["редиска", "редиской", "редиске", "блин", "хрен", "нахрена"]
    special_symbols = ['!', ',', '.', ':',
                       ';']  # бывают еще, как минимум, скобки и кавычки вначале и в конце слова и т.д.
    if not isinstance(value, str):
        raise TypeError(f"unresolved type '{type(value)}' expected  type 'str'")

    for word in value.split():
        if word[len(word) - 1] in special_symbols:
            word = word[:len(word) - 1]
        if word.lower() in bad_words_1:
            value = value.replace(word, f"{word[0]}{'*' * (len(word) - 1)}")
    return value
