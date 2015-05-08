from create_database import CreateDB
from io_class import IO


def main():
    cinema_database = CreateDB()
    # IO.show_movies(cinema_database)
    # IO.show_projections(cinema_database)
    # print(cinema_database.get_available_seats(1))
    # user_input = input("command>")

    # while True:
        # IO.execute_command(cinema_database, user_input)
        # user_input = input("command>")

    IO.buy_tickets(cinema_database, "lala")


if __name__ == '__main__':
    main()
