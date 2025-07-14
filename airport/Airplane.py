from airport.Seat import Seat
from airport.planes import plane_params
from redis_lock.RedLock import RedLock


class Airplane:

    def __init__(self, _id: int = 0, _model: str = "Boeing 747-400", reg: str = "EC-KXN", _seed: int = 0) -> None:
        self.__id = _id
        self.__model = _model
        self.__registration = reg
        self.__max_capacity = plane_params[_model]["max_capacity"]
        self.__current_occupation = 0
        self.__length = plane_params[_model]["length"]
        self.__wingspan = plane_params[_model]["wingspan"]
        self.__height = plane_params[_model]["height"]
        self.__empty_weight = plane_params[_model]["empty_weight"]
        self.__max_weight = plane_params[_model]["max_weight"]
        self.__max_speed = plane_params[_model]["max_speed"]
        self.__cruising_speed = plane_params[_model]["cruising_speed"]
        self.__max_fuel = plane_params[_model]["max_fuel"]
        self.__flights = 0
        self.__seats = self.__create_seats(_seed)

    def get_status(self):
        """
        devuelve el estado del avión (completo o disponible)
        """
        return True if self.__current_occupation - self.__max_capacity == 0 else False

    def add_num_flights(self):
        """
        Aumenta el número de vuelos que ha realizado el avión
        """
        self.__flights += 1

    def update_occupation(self):
        """
        Actualiza la ocupación del avión
        current_occupation +1
        """
        if self.__current_occupation < self.__max_capacity:
            self.__current_occupation += 1

    def get_reg(self):
        return self.__registration

    def get_occupation(self):
        return self.__current_occupation

    def get_max_capacity(self):
        return self.__max_capacity

    def get_cruising_speed(self):
        return self.__cruising_speed

    def get_model(self):
        return self.__model

    @staticmethod
    def __get_seat_position(_pos):
        """
        Devuelve 0 si la posición es menor o igual a 3, 1 si es entre 4 y 7, y 2 si es mayor que 7
        :param _pos: la posición del asiento
        :return: la posición del asiento
        """
        if _pos <= 3:
            return 0
        elif _pos > 7:
            return 2
        else:
            return 1

    def get_actual_occupation(self, _redlock: RedLock):
        """
        Obtiene la ocupación actual del avión
        :param _redlock: el lock de redlock
        :return: la ocupación actual del avión
        """
        counter = 0
        for row in self.__seats:
            for seat in row:
                lock = _redlock.create_lock(seat.get_number(), 20)
                if not lock:
                    counter += 1
                else:
                    _redlock.unlock_a_lock(lock)

        self.__current_occupation = counter
        return counter

    def __create_seats(self, _seed: int):
        """
        Crea n filas de 10 asientos por fila
        :param _seed: el seed para los asientos
        :return: la lista de asientos
        """
        _seats = []
        _seat_id = 1
        _business_class = 0
        _num_seat_by_row = int(self.__max_capacity / 10) + 1
        for _row in range(0, _num_seat_by_row):
            if _row not in _seats:
                _seats.append(_row)
                _seats[_row] = []
            for seat in range(1, 11):
                if _seat_id <= self.__max_capacity:
                    _pos = self.__get_seat_position(seat)
                    _class = 2
                    if _business_class < 10:
                        _class = 1
                        _business_class += 1
                    _seats[_row].append(Seat(str(_seed) + "_" + str(_seat_id), _class, _pos))
                    _seat_id += 1
                else:
                    break
        return _seats

    def get_seat(self, _row, _n):
        """
        Obtiene un asiento
        :param _row: la fila del asiento
        :param _n: el número del asiento
        :return: el asiento
        """
        return self.__seats[_row][_n]

    def print_airplane(self):
        """
        Crea una cadena de caracteres con los ids de los asientos que tiene el avión con la distribución que tienen.
        :return: la cadena de caracteres con los ids de los asientos
        """
        for row in self.__seats:
            row_s = "|"
            for i, seat in enumerate(row):
                row_s += ("-%s" % (seat.get_number()))
                if i == 2 or i == 6:
                    row_s += "-|"

            row_s += "-|\n"
            print(row_s)

    def get_available_seats(self):
        """
        Devuelve una lista de asientos disponibles en el avión
        :return: la lista de asientos disponibles
        """
        _available_seats = []
        for row in self.__seats:
            for seat in row:
                if not seat.is_reserved():
                    _available_seats.append(seat)
        return _available_seats

    def find_seat(self, _number: str):
        """
        Obtiene un asiento
        :param _number: el número del asiento
        :return: el asiento
        """
        for row in self.__seats:
            for seat in filter(lambda x: x.get_number() == _number, row):
                return seat
