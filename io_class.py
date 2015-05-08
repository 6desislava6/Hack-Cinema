import re
from create_database import CreateDB


class IO:
    @staticmethod
    def show_movies(database):
        movies = database.list_movies()
        for movie in movies:
            print("{}. {} - {}".format(movie['movies_id'],
                                       movie['name'],
                                       movie['rating']))

    @staticmethod
    def show_projections(database):
        projections = database.list_projections()
        for projection in projections:
            print("{}. {} - {} - {} - {}".format(projection['projections_id'],
                                                 projection['name'],
                                                 projection['projection_type'],
                                                 projection['projection_date'],
                                                 projection['time']))

    @staticmethod
    def show_movie_projections(db, movie_id):
        projections = db.show_movie_projections(movie_id)
        for projection in projections:
                print("{}. {} - {} - {} - {}".format(
                    projection['projections_id'],
                    projection['name'],
                    projection['projection_type'],
                    projection['projection_date'],
                    projection['time']))

    @staticmethod
    def help(database):
        print('Commands:')
        print('* "show_movies"')
        print('* "show_projections"')
        print('* "make_reservation"')
        print('* "help"')
        print('* "exit"')

    @staticmethod
    def make_reservation(database):
        username = input('Type your username: ')
        IO.buy_tickets(database, username)

    @staticmethod
    def execute_command(database):
        user_input = input('command>')
        all_commands = {
                        "show_movies": IO.show_movies,
                        "show_projections": IO.show_projections,
                        "make_reservation": IO.make_reservation,
                        "help": IO.help
        }
        if user_input in all_commands:
            if user_input != 'exit':
                all_commands[user_input](database)
        if user_input == 'exit':
            return False
        return True

    @staticmethod
    def print_seats(free_seats):
        matrix = [['.' for x in range(CreateDB.COL_SIZE)] for x in range(CreateDB.ROW_SIZE)]
        for seat in free_seats:
            matrix[seat[0] - 1][seat[1] - 1] = '*'
        firstrow = ''
        for x in range(CreateDB.COL_SIZE):
            firstrow += str(x) + ' '
        print(firstrow)
        for x in range(CreateDB.ROW_SIZE):
            row = str(x) + ' '
            for y in range(CreateDB.COL_SIZE):
                row += matrix[x][y]
            print(row)

    @staticmethod
    def buy_tickets(db, username):
        wanted_tickets = int(input('Quantity of tickets>'))

        print('Choose a movie')
        IO.show_movies(db)
        movie_id = input('movie_id>')

        print('Choose a projection')
        IO.show_movie_projections(db, movie_id)
        wanted_projection = input('Projection ID>')

        if not db.are_enough_seats(wanted_tickets, wanted_projection):
            print('Not enough tickets!')
            return

        for x in range(wanted_tickets):
            print('Free seats for this projection are: ')
            free_seats = db.get_available_seats(wanted_projection)
            IO.print_seats(free_seats)
            seat = IO.__make_seats(free_seats)
            db.make_reservation(username, wanted_projection, seat[0], seat[1])

        print('Do you confirm your reservation? y/n')
        user_input = input('Answer>')
        if user_input == 'n':
            db.undo_reservation(wanted_tickets)
        print(wanted_tickets)
        IO.show_reservations(db,    wanted_tickets)

    @staticmethod
    def __find_numbers_regex(customer_input):
        regular_expression = re.compile('\d+')
        matches = regular_expression.findall(customer_input)
        result = []
        for number in matches:
            result.append(int(number))

        return tuple(result)

    @staticmethod
    def __validate_seat(seat, free_seats):
        return seat in free_seats

    @staticmethod
    def __make_seats(free_seats):
        answer_customer = input("""your choce>""")
        seat = IO.__find_numbers_regex(answer_customer)
        print(seat)
        is_valid_seat = IO.__validate_seat(seat, free_seats)

        while not is_valid_seat:
            print('This is not a valid seat! Type again!')
            answer_customer = input("""your choce>""")
            seat = IO.__find_numbers_regex(answer_customer)
            is_valid_seat = IO.__validate_seat(seat, free_seats)
        return seat

    @staticmethod
    def show_reservations(db, count):
        reservations_raw = db.show_last_n_reservations(count)
        for line in reservations_raw:
            name = line['username']
            projection_date = line['projection_date']
            movie_name = line['name']
            row = line['row']
            col = line['col']
            reservation = 'username: {}, movie: {} ---> {}, place ({}, {})'.format(name, movie_name, projection_date, row, col)
            print(reservation)


