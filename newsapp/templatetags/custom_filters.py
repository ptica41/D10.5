from django import template

register = template.Library()

@register.filter()
def censor(value):
    bad = [
        'жопа', 'Жопа',
        'херня', 'Херня',
        'чмо', 'Чмо'
    ]
    for i in bad:
        if i in value:
            value = value.replace(i[1:], '*' * (len(i) - 1))
    return f'{value}'
