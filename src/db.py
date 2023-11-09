import os
from pymongo import MongoClient


connection_string_name: str = 'MONGODB_CS'  # NOTE: env var name


if connection_string_name not in os.environ:
    raise Exception(f'application requires "{connection_string_name}" to be '
                    f'defined in environemnt')

connection_string: str | None = os.getenv(connection_string_name)
client = MongoClient(connection_string)

# mongodb+srv://m3ck0:1lMTqRBCKq1wVpFU@demo.cysajd7.mongodb.net/?retryWrites=true&w=majority