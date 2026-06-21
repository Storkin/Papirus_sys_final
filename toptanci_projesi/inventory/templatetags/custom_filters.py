from django import template

register = template.Library()


@register.filter
def format_phone(value):
    """
    05123478485  →  0512 347 8485
    5123478485   →  512 347 8485
    """
    if not value:
        return value
    digits = ''.join(filter(str.isdigit, str(value)))
    if len(digits) == 11:
        return f"{digits[0:4]} {digits[4:7]} {digits[7:11]}"
    elif len(digits) == 10:
        return f"{digits[0:3]} {digits[3:6]} {digits[6:10]}"
    return value


@register.filter
def format_money(value):
    """
    15000.5   →  15.000,50
    1250000   →  1.250.000,00
    """
    try:
        value = float(value)
        # Önce 2 ondalık basamaklı ingilizce formatla: 15,000.50
        formatted = f"{value:,.2f}"
        # Türkçe formata çevir: nokta=binlik ayraç, virgül=ondalık
        formatted = formatted.replace(',', 'X').replace('.', ',').replace('X', '.')
        return formatted
    except (ValueError, TypeError):
        return value
