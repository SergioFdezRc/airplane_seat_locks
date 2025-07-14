# Airplane Seat Locks

Airplane seat reservation system with distributed concurrency management using Redis and the Redlock algorithm.

- Author: Sergio Fernández Rincón
- Version: 1.0
- Creation date: 2020-07-24

## Description

This project implements an airplane seat reservation application, where multiple users can reserve seats concurrently. To avoid race conditions and ensure reservation integrity, Redis is used as the storage system and Redlock as the distributed locking algorithm.

The system allows you to:
- Create flights and airplanes with different configurations.
- View and reserve available seats.
- Calculate ticket prices based on class and distance.
- Print personalized tickets for each reservation.
- Guarantee exclusive seat reservation even in distributed environments.

## Architecture

- **Python 3.10+**
- **Redis** as the database and locking system.
- **Redlock** for distributed lock management.
- Modular structure: `airport/`, `redis_lock/`, `utils/`.

## Main modules

- `airport/Flight.py`: Flight and reservation logic.
- `airport/Airplane.py`: Airplane and seat modeling.
- `airport/Seat.py`: Seat logic and price calculation.
- `redis_lock/RedLock.py`: Wrapper for Redlock and connection/lock management.
- `utils/ticket.py`: Ticket generation and printing.
- `main.py`: Main execution script.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/SergioFdezRc/airplane_seat_locks.git
   cd airplane_seat_locks
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make sure you have Redis running on localhost (default port 6379):**
   ```bash
   docker run -p 6379:6379 -it redis:latest
   ```

## Usage
### Local
Run the main application:
```bash
python main.py
```

Follow the console instructions to:
- List available flights.
- Select a flight.
- Reserve seats (with distributed locking).
- Enter customer data and payment method.
- Receive a personalized ticket.

### Running with Docker

You can run the entire project (app + Redis) using Docker Compose:

1. Build and start the containers:
   ```bash
   docker-compose up --build
   ```

2. The application will start and connect automatically to the Redis service.

3. You can interact with the app via the console inside the container.

To stop and remove the containers:
```bash
docker-compose down
```


## Configuration

- Flight, airplane, and distance parameters are in `utils/constants.py` and `airport/planes.py`.
- You can modify origins, destinations, dates, and airplane models as needed.

## Redlock Algorithm

The system uses the [redlock-py](https://github.com/SPSCommerce/redlock-py) library to implement the Redlock algorithm, which allows safe distributed lock management in environments with multiple Redis instances. This ensures that two users cannot reserve the same seat simultaneously.

## Main dependencies

- `redlock==1.2.0`
- `redlock-py==1.0.8`
- `redis` (Python client for Redis)

See `requirements.txt` for the full list.

## Example usage

```text
LIST OF FLIGHTS ->
ID: 0
Origin: Badajoz - Destination: Barcelona
Departure date: 2020-08-04 - Departure time: 07:00:00
Plane registration: EC-KXN - Occupancy: 0 of 416
__________________________________________________
Select a flight from the list: 0
You have selected the following flight:
...
Select a seat > 1
The ticket price is 120.0 €. Do you want to continue? YES
Fill in your customer details:
Name: John
Surname: Smith
...
+=======================================================================+
| TICKET ID - 0      PRICE: 120.0 €     
| Client: John Smith - john@email.com                  
| Plane Ref: EC-KXN                    
| Source: Badajoz Destination: Barcelona        
| Departure date 2020-08-04 Flight time 07:00:00        
+=======================================================================+
```

