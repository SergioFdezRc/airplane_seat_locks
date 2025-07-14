import datetime

from redlock import Lock

from airport.seat_position import SeatPosition
from utils.constants import intervals


class Seat(Lock):

    def __init__(self, number: str = "", _class: int = 1, _pos: int = 0) -> None:
        self.__seat_number = number
        self.__locked = False
        self.__reserved = False
        self.__class_type = _class
        self.__position = _pos
        self.__price = None

    def get_number(self):
        return self.__seat_number

    def set_locked(self, value):
        self.__locked = value

    def set_reserved(self, value):
        self.__reserved = value

    def is_locked(self):
        return self.__locked

    def is_reserved(self):
        return self.__reserved

    def get_class_type(self):
        return self.__class_type

    def get_str_class(self):
        return "Turista" if self.get_class_type() == 2 else "Business"

    def get_num_position(self):
        return self.__position

    def get_str_position(self):
        """
        Devuelve la posición del asiento en formato de cadena
        :return: la posición del asiento
        """
        if self.__position == 0:
            return SeatPosition.LEFT
        elif self.__position == 1:
            return SeatPosition.CENTER
        elif self.__position == 2:
            return SeatPosition.RIGHT
        return ""


    def compute_price(self, price_base, distance):
        """
        El precio del billete se calcula en función de
        - La clase del asiento
        - La distancia del vuelo
        :param price_base: el precio base del asiento
        :param distance: la distancia del vuelo
        :return: el precio del billete
        """
        price_class = price_base * 1.25 if self.get_class_type() == 2 else price_base * 2
        price_distance = distance * 0.05
        self.__price = round(price_class + price_distance, 2)

    def get_price(self):
        return self.__price

    def reserve(self, departure_date, _redlock):
        """
        Reserva el asiento
        :param departure_date: la fecha de salida del vuelo
        :param _redlock: el lock de redlock
        :return: True si se ha reservado el asiento, False en caso contrario
        """
        try:
            self.set_reserved(True)
            self.set_locked(True)
            today = datetime.datetime.now()
            print("Hoy es: {}".format(today))
            timeleft = departure_date - today
            timeleft = timeleft.seconds + (timeleft.days * intervals['days'])
            print("Tiempo restante: {}".format(timeleft))
            _redlock.create_lock(self.get_number(), timeleft)
            print("Asiento {} bloqueado y en estado de reserva hasta {}".format(self.get_number(), departure_date))
            return True
        except Exception:
            pass
        return False

    def print_seat(self):
        """
        Imprime el asiento
        :return: el asiento en formato de cadena
        """
        return "· Nro: {} \n· Cat: {}\n ·Ubi: {}\n_________________________".format(
            self.get_number(), self.get_str_class(), self.get_str_position())
