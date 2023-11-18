import os
from redis import Redis


connection_string_name: str = 'REDIS_CS'  # NOTE: env var name


if connection_string_name not in os.environ:
    raise Exception(f'application requires "{connection_string_name}" to be '
                    f'defined in environemnt')

connection_string: str | None = os.getenv(connection_string_name)
# print(connection_string)
client = Redis.from_url(connection_string)
