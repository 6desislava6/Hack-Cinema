from create_database import CreateDB
from io_class import IO


def main():
    cinema_database = CreateDB()
    command = IO.execute_command(cinema_database)
    while command:
        command = IO.execute_command(cinema_database)

if __name__ == '__main__':
    main()
