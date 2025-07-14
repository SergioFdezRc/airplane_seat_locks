from datetime import datetime, date, time

from airport.Airplane import Airplane
from airport.planes import plane_params
from redis_lock.RedLock import RedLock
from utils.Payment import manage_payment_form, check_email
from utils.check_personal_data import check_tel
from utils.constants import YES, DISTANCES

# Comprobar si el número de asientos del avión asociado a este vuelo está completo, si está completo, bloquear el recurso
# Hasta el día en que salga el vuelo.
from utils.ticket import Ticket


def _manage_seat(_selected_seat, _redlock):
    """
    Bloquea el asiento y crea un lock para el asiento
    :param _selected_seat: el asiento seleccionado
    :param _redlock: el lock de redlock
    :return: el lock del asiento
    """
    # bloqueamos el recurso...
    _selected_seat.set_locked(True)
    _lock = _redlock.create_lock(str(_selected_seat.get_number()), 180000)
    if not _lock:
        print("The seat is busy")
        return False
    print(_selected_seat.print_seat())
    print("El estado del asiento ahora es {}.".format("Bloqueado" if not _lock else "Libre"))
    # Pasamos al siguiente paso y es confirmar la reserva. Si la reserva se confirma, entonces se libera el lock y
    #
    print(
        "Has seleccionado el asiento número {} de tipo {} ubicado en el {}".format(_selected_seat.get_number(),
                                                                                   _selected_seat.get_str_class(),
                                                                                   _selected_seat.get_str_position()))
    return _lock


class Flight():
    """
    Clase que representa un vuelo
    """

    def __init__(self) -> None:
        self.__source = None
        self.__destiny = None
        self.__departure_time = None  # datetime hour
        self.__check_in = None
        self.__airplane = None
        self.__date = None  # Datetime date
        self.__blocked = False
        self.__departure_gate = None

    def create_flight(self, _id: int, _source: str, _destiny: str, _departure: time, _checkin,
                      _airplane: Airplane,
                      _date: date):
        """
        Crea un vuelo con un origen, destino, avión asociado a él, con una fecha y hora de salida
        :param _id: el id del vuelo
        :param _source: el origen del vuelo
        :param _destiny: el destino del vuelo
        :param _departure: la hora de salida del vuelo
        :param _checkin: el checkin del vuelo
        :param _airplane: el avión asociado al vuelo
        :param _date: la fecha de salida del vuelo
        """
        self.__id = _id
        self.__source = _source
        self.__destiny = _destiny
        self.__departure_time = _departure
        self.__check_in = _checkin
        self.__airplane = _airplane
        self.__date = _date

    def get_id(self):
        return self.__id

    def get_source(self):
        return self.__source

    def get_destiny(self):
        return self.__destiny

    def get_departure_time(self):
        return self.__departure_time

    def get_date(self):
        return self.__date

    def get_airplane(self):
        return self.__airplane

    def block_flight(self):
        """
        Bloquea el vuelo
        :return: True si el vuelo está bloqueado, False en caso contrario
        """
        if self.__airplane is not None and self.__airplane.get_status():
            self.__blocked = True

    def is_blocked(self):
        return self.__blocked

    @staticmethod
    def __get_nros_seats(seats):
        """
        Obtiene los números de los asientos
        :param seats: la lista de asientos
        :return: la lista de números de los asientos
        """
        numbers = []
        for seat in seats:
            numbers.append(int(seat.get_number().split("_")[1]))
        return numbers

    def calculate_flight_time(self):
        """
        Calcula el tiempo de vuelo
        :return: el tiempo de vuelo en segundos
        """
        if self.__airplane is None:
            return 0
        source = self.get_source()
        destiny = self.get_destiny()
        if source is None or destiny is None:
            print("Origen o destino no definidos.")
            return 0
        return (DISTANCES[source][destiny] / self.__airplane.get_cruising_speed()) * 60 * 60

    def reserve_seat(self, _redlock: RedLock):
        """
        Reserva un asiento
        :param _redlock: el lock de redlock
        :return: True si se ha reservado el asiento, False en caso contrario
        """
        if self.is_blocked():
            print("El vuelo está bloqueado.")
            return

        if self.__airplane is None:
            print("No hay un avión asignado a este vuelo.")
            return

        _available_seats = self.__airplane.get_available_seats()
        if not _available_seats:
            print("No hay asientos disponibles.")
            return

        for seat in _available_seats:
            print(seat.print_seat())

        nros_seats = self.__get_nros_seats(_available_seats)
        seat_selection = int(input("Selecciona un asiento > "))
        while seat_selection not in nros_seats:
            print("Error.")
            seat_selection = int(input("Selecciona un asiento > "))

        _selected_seat = self.__airplane.find_seat(str(self.get_id()) + "_" + str(seat_selection))
        if _selected_seat is None:
            print("Asiento no encontrado.")
            return

        source = self.get_source()
        destiny = self.get_destiny()
        if source is None or destiny is None:
            print("Origen o destino no definidos.")
            return

        _selected_seat.compute_price(plane_params[self.__airplane.get_model()]['price_base'],
                                     DISTANCES[source][destiny])
        _lock = _manage_seat(_selected_seat, _redlock)
        if not _lock:
            return

        res = input("El precio del billete es {} €. ¿Desea continuar?".format(_selected_seat.get_price()))
        res = res.upper()
        if res not in YES:
            _redlock.unlock_a_lock(_lock)
            return

        print("Rellene sus datos de cliente:")
        client_name = input("Nombre: ")
        client_second_name = input("Apellidos: ")
        client_dir = input("Dirección: ")
        client_email = input("Email: ")
        check_email(client_email)
        tel = input("Teléfono: ")
        if not check_tel(tel):
            _redlock.unlock_a_lock(_lock)
            return

        payment_form = input("Selecciona la forma de pago:\n\t1. Tarjeta de crédito/débito.\n\t2. Paypal.\n\n> ")
        card = manage_payment_form(int(payment_form))
        if not card:
            _redlock.unlock_a_lock(_lock)
            return

        _selected_seat.set_locked(False)
        islocked = _redlock.unlock_a_lock(_lock)
        print(islocked)
        if islocked:
            print("El recurso se ha desbloqueado")
            departure_date = self.get_date()
            departure_time_obj = self.get_departure_time()
            if departure_date is None or departure_time_obj is None:
                print("Fecha u hora de salida no definidas.")
                return
            departure_time = datetime.combine(departure_date, departure_time_obj)
            print(departure_time)
            if _selected_seat.reserve(departure_time, _redlock):
                flight_time = self.calculate_flight_time()
                from datetime import timedelta
                flight_time_str = str(timedelta(seconds=int(flight_time)))
                client_full_name = client_name + " " + client_second_name

                ticket = Ticket(
                    str(self.get_id()),
                    client_full_name,
                    client_email,
                    self.__airplane.get_reg(),
                    source,
                    destiny,
                    departure_date,
                    departure_time_obj,
                    _selected_seat.get_price()
                )
                ticket.print_ticket()

    def print_flight(self, _redlock):
        """
        Imprime el vuelo
        :param _redlock: el lock de redlock
        :return: el vuelo en formato de cadena
        """
        airplane = self.get_airplane()
        if airplane is None:
            reg = "N/A"
            ocupacion = "N/A"
            capacidad = "N/A"
        else:
            reg = airplane.get_reg()
            ocupacion = airplane.get_actual_occupation(_redlock)
            capacidad = airplane.get_max_capacity()
        return "ID: {}\nOrigen: {} - Destino: {}\n" \
               "Fecha de salida: {} - Hora de salida: {}\n" \
               "Matrícula avión: {} - Ocupación: {} de {}\n" \
               "__________________________________________________".format(
            self.get_id(), self.get_source(),
            self.get_destiny(),
            self.get_date(), self.get_departure_time(),
            reg, ocupacion, capacidad)
