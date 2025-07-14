from utils.check_personal_data import check_card
from getpass import getpass

from utils.constants import DOMAINS, SERVER_LIST


def check_email(ppal_email):
    if '@' not in ppal_email:
        print("Introduce un correo válido.")
        return False
    server = ppal_email.split('@')[1]
    if '.' not in server:
        print("Introduce un correo válido.")
        return False

    if server.split('.')[0] not in SERVER_LIST:
        print("El servidor de correo no es válido.")
        return False
    if server.split('.')[1] not in DOMAINS:
        print("El dominio no es válido.")
        return False
    return True


def manage_payment_form(_payment):
    if _payment == 1:
        validity_credit_card = False
        card_values = []
        while not validity_credit_card:
            credit_card_number = input("You have selected credit/debit card payment.\n"
                                       "Please, introduce the number of your credit card.\n\n> ")
            security_number = input("Introduce the security code of your card. > ")
            expiration_date = input("Introduce the expiration date of your card. > ")
            card_values.append(credit_card_number)
            card_values.append(security_number)
            card_values.append(expiration_date)
            validity_credit_card = check_card(card_values)
            if validity_credit_card:
                print("The credit card is correct.")
                print("Checking the payment...")
        return validity_credit_card
    else:
        validity_paypal = False
        while not validity_paypal:
            ppal_email = input("You have selected paypal payment.\n"
                               "Please, introduce the email asociated to your account.\n\n\tEmail: ")
            validity_paypal = check_email(ppal_email)
            ppal_password = getpass(prompt='\tPassword: ')
            if validity_paypal:
                print("The email verification is correct.")
                print("Checking the payment...")
            return validity_paypal
