from create_database import CreateDB
from io_class import IO


def main():
    cinema_database = CreateDB()
    IO.show_movies(cinema_database)
    IO.show_projections(cinema_database)

    # user_input = input("command>")

    # while True:
        # IO.execute_command(cinema_database, user_input)
        # user_input = input("command>")


if __name__ == '__main__':
    main()
