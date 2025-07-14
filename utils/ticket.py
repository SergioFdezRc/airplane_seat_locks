from datetime import date, time

class Ticket():

    def __init__(self, _id: str, _client_full_name: str, _client_email: str, _plane: str, _source: str,
                 _destination: str, _departure_date: date,
                 _flight_time: time, _price: float) -> None:
        super().__init__()
        self.__id = _id
        self.__client_full_name = _client_full_name
        self.__client_email = _client_email
        self.__plane = _plane
        self.__source = _source
        self.__destination = _destination
        self.__departure_date = _departure_date
        self.__flight_time = _flight_time
        self.__price = _price

    def print_ticket(self):
        s = "+=======================================================================+\n"
        s += "| TICKET ID - {}      PRICE: {} €     \n".format(self.__id, self.__price)
        s += "| Client: {} - {}                  \n".format(self.__client_full_name, self.__client_email)
        s += "| Plane Ref: {}                    \n".format(self.__plane)
        s += "| Source: {} Destination: {}        \n".format(self.__source, self.__destination)
        s += "| Departure date {} Flight time {}        \n".format(self.__departure_date, self.__flight_time)
        s += "+=======================================================================+\n"
        print(s)
