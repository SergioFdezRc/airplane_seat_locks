from airport.Airplane import Airplane
from airport.Flight import Flight
from redis_lock.RedLock import RedLock
from utils.config import config
from datetime import datetime


def create_initial_config():
    _id = 1
    _model = "Boeing 747-400"
    _reg = "EC-KXN"
    flight_list = []
    flight_number_list = []

    for i, date in enumerate(config.DATES):
        _seed = i
        airplane = Airplane(_id, _model, _reg, _seed)
        departure_time_obj = datetime.strptime(config.DEPARTURE_HOUR, "%H:%M:%S").time()
        date_obj = datetime.strptime(date, "%Y-%m-%d").date()
        flight = Flight()
        flight.create_flight(i, config.SOURCE, config.DESTINY, departure_time_obj, False, airplane, date_obj)
        flight_list.append(flight)
        flight_number_list.append(i)

    return flight_list, flight_number_list


def print_flights(flights, _redlock):
    print("LISTADO DE VUELOS ->\n")
    for flight in flights:
        if not flight.get_airplane().get_occupation() >= flight.get_airplane().get_max_capacity():
            print(flight.print_flight(_redlock))


def main():
    _redlock = RedLock()
    _redlock.create_connection()

    flight_list, flight_number_list = create_initial_config()
    bool_res = True
    while bool_res:
        print_flights(flight_list, _redlock)
        flight_selection = int(input("Selecciona un vuelo en la lista: "))
        while flight_selection not in flight_number_list:
            print("Error de selección.")
            flight_selection = int(input("Selecciona un vuelo en la lista: "))

        selected_flight = flight_list[flight_selection]
        print("Has seleccionado el siguiente vuelo: ")
        print(selected_flight.print_flight(_redlock))
        selected_flight.reserve_seat(_redlock)
        res = input("¿Quieres reservar otro asiento? (Sí/No)")
        bool_res = True if res.upper() in ["SÍ", "SI", "YES", "S", "Y", ""] else False

if __name__ == '__main__':
    main()
