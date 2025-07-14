from redlock import Redlock

from utils.config import config


def check_dlm_connections(function):
    """
    Check that the connection is active before launching a function

    :param function: the function to be launched
    :return: the function wrapped
    """

    def wrapper(*args):
        if args[0].dlm is not None:
            return function(*args)
        else:
            print("[ERROR] You must create a connection first")

    return wrapper


class RedLock:

    def __init__(self) -> None:
        self.dlm = None

    def create_connection(self):
        """
        It creates a Redlock instance with a connection server with host and port indicated by config values
        :return: an instance of the dlm
        """
        self.dlm = Redlock([
            {"host": config.REDIS_HOST, "port": config.REDIS_PORT, "db": 0},
            {"host": config.REDIS_HOST, "port": config.REDIS_PORT, "db": 1},
        ])

    @check_dlm_connections
    def add_server_to_dlm(self):
        pass

    @check_dlm_connections
    def create_lock(self, lock_name: str, ttl: int = 1000):
        """
        It creates a new lock of RedLock
        :param lock_name: the name of the lock
        :param ttl: the time to live
        :return: a lock with name :name and a ttl of :ttl
        """
        if self.dlm is None or not hasattr(self.dlm, "lock"):
            print("[ERROR] El objeto Redlock no tiene el método 'lock'.")
            return None
        return self.dlm.lock(lock_name, ttl)

    @check_dlm_connections
    def list_clients(self, db_id: int):
        """
        List the client params of a given db index.
        :param db_id: the index of the db
        :return:
        """
        try:
            if self.dlm is None or not hasattr(self.dlm, "servers") or self.dlm.servers is None:
                print("[ERROR] El objeto Redlock no tiene el atributo 'servers' o está vacío.")
                return None
            return self.dlm.servers[db_id].execute_command("CLIENT", "LIST")
        except Exception as e:
            print("[ERROR] the server with id %d does not exists." % db_id, e)

    @check_dlm_connections
    def unlock_a_lock(self, lock):
        """
        Release a given lock
        :param lock: the lock to be released
        :return: none
        """
        try:
            if self.dlm is None or not hasattr(self.dlm, "unlock"):
                print("[ERROR] El objeto Redlock no tiene el método 'unlock'.")
                return False
            self.dlm.unlock(lock)
            return True
        except Exception:
            pass
        return False
