import psycopg2


class DBConnect:
    """Connect to postgres database."""

    def __init__(self):
        pass

    @staticmethod
    def get_connection(user, password, host, database, port):
        try:
            connection = psycopg2.connect(
                user=user,
                password=password,
                host=host,
                database=database,
                port=port
            )

            return connection

        except(Exception, psycopg2.Error) as e:
            print('Error connecting to the database ', e)
