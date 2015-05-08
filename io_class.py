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
        print('* "show_movie_projections"')
        print('* "make_reservation"')
        print('* "help"')
        print('* "exit"')

    @staticmethod
    def exit(database):
        print('Bye!')
        return 0

    @staticmethod
    def __str_to_numbers(answer_customer):
        numbers = answer_customer.split(', ')
        numbers[0] = numbers[0][1:]
        numbers[1] = numbers[1][:1]
        return numbers

    @staticmethod
    def make_reservation(database):
        pass

    @staticmethod
    def execute_command(database, user_input):
        all_commands = {
                        "exit": IO.exit,
                        "show_movies": IO.show_movies,
                        "show_projections": IO.show_projections,
                        "show_movie_projections": IO.show_movie_projections,
                        "make_reservation": IO.make_reservation,
                        "help": IO.help

        }
        try:
            all_commands[user_input](database)
        except:
            print("Invalid command!")

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
            answer_customer = input("""your choice (in format (x, y),
            please. Otherwise it will not work :D)>""")

            seat = IO.__str_to_numbers(answer_customer)
            print(seat)
            db.make_reservation(username, wanted_projection, seat[0], seat[1])
