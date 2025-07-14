import re
from datetime import datetime


def check_char(cadena):
    numbers = re.compile('[0-9]')
    return False if numbers.match(cadena) is None else True


def check_tel(_tel: str = None):
    if _tel is None or _tel is '':
        print("You must specify a telephone number.")
        return False

    is_number = check_char(_tel)
    if not is_number:
        print("The telephone number must not contains any character.")
        return is_number
    if len(_tel) < 9 or len(_tel) > 9:
        print("The telephone number is incorrect")
        return False

    return True


def check_card_number(card, _length):
    if card is None or card is '':
        print("You must specify a credit card number.")
        return False
    is_number = check_char(card)
    if not is_number:
        print("The credit card number must not contains any character.")
        return is_number
    if len(card) < _length or len(card) > _length:
        print("The credit card number is incorrect")
        return False
    return True


def check_expiration_date(_expiration_date):
    _expiration_date = datetime.strptime(_expiration_date, "%m/%Y")
    print(_expiration_date)
    actual_date = datetime.now()
    if actual_date >= _expiration_date:
        return False
    return True


def check_card(card):
    if check_card_number(card[0], 16):
        if check_card_number(card[1], 3):
            if check_expiration_date(card[2]):
                return True
    return False
