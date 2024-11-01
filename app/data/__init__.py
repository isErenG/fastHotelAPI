import os

import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'),
                        user=os.getenv('POSTGRES_USER'),
                        password=os.getenv('POSTGRES_PASSWORD'),
                        host=os.getenv('POSTGRES_HOST'),
                        port=os.getenv('POSTGRES_PORT'))

