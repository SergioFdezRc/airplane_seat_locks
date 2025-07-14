# Airplane Seat Locks

Sistema de reservas de asientos de avión con gestión de concurrencia distribuida mediante Redis y el algoritmo Redlock.

- Autor: Sergio Fernández Rincón
- Version: 1.0
- Fecha de creación: 24-07-2020

## Descripción

Este proyecto implementa una aplicación de reservas de asientos de avión, donde varios usuarios pueden reservar asientos de forma concurrente. Para evitar condiciones de carrera y garantizar la integridad de las reservas, se utiliza Redis como sistema de almacenamiento y el algoritmo Redlock para la gestión de bloqueos distribuidos.

El sistema permite:
- Crear vuelos y aviones con diferentes configuraciones.
- Consultar y reservar asientos disponibles.
- Calcular precios de billetes en función de clase y distancia.
- Imprimir tickets personalizados para cada reserva.
- Garantizar la exclusividad de la reserva de asientos incluso en entornos distribuidos.

## Arquitectura

- **Python 3.10+**
- **Redis** como base de datos y sistema de locking.
- **Redlock** para la gestión de bloqueos distribuidos.
- Estructura modular: `airport/`, `redis_lock/`, `utils/`.

## Principales módulos

- `airport/Flight.py`: Lógica de vuelos y reservas.
- `airport/Airplane.py`: Modelado de aviones y asientos.
- `airport/Seat.py`: Lógica de asientos y cálculo de precios.
- `redis_lock/RedLock.py`: Wrapper para Redlock y gestión de conexiones/bloqueos.
- `utils/ticket.py`: Generación e impresión de tickets.
- `main.py`: Script principal de ejecución.

## Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/tu_usuario/airplane_seat_locks.git
   cd airplane_seat_locks
   ```

2. **Crea un entorno virtual y actívalo:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Asegúrate de tener Redis corriendo en localhost (puerto 6379 por defecto):**
   ```bash
   docker run -p 6379:6379 -it redis:latest
   ```

## Uso
### Local
Ejecuta la aplicación principal:
```bash
python main.py
```

Sigue las instrucciones en consola para:
- Listar vuelos disponibles.
- Seleccionar un vuelo.
- Reservar asientos (con bloqueo distribuido).
- Introducir datos de cliente y forma de pago.
- Recibir un ticket personalizado.

### Ejecución con Docker

Puedes ejecutar todo el proyecto (app + Redis) usando Docker Compose:

1. Construye e inicia los contenedores:
   ```bash
   docker-compose up --build
   ```

2. La aplicación se iniciará y se conectará automáticamente al servicio de Redis.

3. Puedes interactuar con la app desde la consola dentro del contenedor.

Para detener y eliminar los contenedores:
```bash
docker-compose down
```

## Configuración

- Los parámetros de vuelos, aviones y distancias están en `utils/constants.py` y `airport/planes.py`.
- Puedes modificar los orígenes, destinos, fechas y modelos de avión según tus necesidades.

## Algoritmo Redlock

El sistema utiliza la librería [redlock-py](https://github.com/SPSCommerce/redlock-py) para implementar el algoritmo Redlock, que permite gestionar bloqueos distribuidos de forma segura en entornos con múltiples instancias de Redis. Esto garantiza que dos usuarios no puedan reservar el mismo asiento simultáneamente.

## Dependencias principales

- `redlock==1.2.0`
- `redlock-py==1.0.8`
- `redis` (cliente Python para Redis)

Consulta `requirements.txt` para la lista completa.

## Ejemplo de uso

```text
LISTADO DE VUELOS ->
ID: 0
Origen: Badajoz - Destino: Barcelona
Fecha de salida: 2020-08-04 - Hora de salida: 07:00:00
Matrícula avión: EC-KXN - Ocupación: 0 de 416
__________________________________________________
Selecciona un vuelo en la lista: 0
Has seleccionado el siguiente vuelo:
...
Selecciona un asiento > 1
El precio del billete es 120.0 €. ¿Desea continuar? SÍ
Rellene sus datos de cliente:
Nombre: Juan
Apellidos: Pérez
...
+=======================================================================+
| TICKET ID - 0      PRICE: 120.0 €     
| Client: Juan Pérez - juan@email.com                  
| Plane Ref: EC-KXN                    
| Source: Badajoz Destination: Barcelona        
| Departure date 2020-08-04 Flight time 07:00:00        
+=======================================================================+
```

