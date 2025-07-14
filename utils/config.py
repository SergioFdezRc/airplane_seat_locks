import os
from dotenv import load_dotenv
from typing import List

load_dotenv()

class Config:
    REDIS_HOST: str = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT: int = int(os.getenv('REDIS_PORT', 6379))
    SOURCE: str = os.getenv('SOURCE', 'Badajoz')
    DESTINY: str = os.getenv('DESTINY', 'Barcelona')
    DEPARTURE_HOUR: str = os.getenv('DEPARTURE_HOUR', '07:00:00')
    DATES: List[str] = os.getenv('DATES', '').split(',') if os.getenv('DATES') else []

config = Config() 