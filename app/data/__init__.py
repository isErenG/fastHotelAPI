from dotenv import load_dotenv
import os

import psycopg2

load_dotenv()

# conn = psycopg2.connect(database=os.getenv('POSTGRES_DATABASE'),
#                         host=os.getenv('POSTGRES_HOST'),
#                         user=os.getenv('POSTGRES_USER'),
#                         password=os.getenv('POSTGRES_PASSWORD'),
#                         port=os.getenv('POSTGRES_PORT'))
