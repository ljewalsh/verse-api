import os

user = os.getenv('POSTGRES_USER')
password = os.getenv('POSTGRES_PASSWORD')
host = os.getenv('POSTGRES_HOST')
database = os.getenv('POSTGRES_DB')
port = os.getenv('POSTGRES_PORT')

DATABASE_CONNECTION_URI = 'postgres://{}:{}@{}:{}/{}'.format(user, password, host, port, database)

