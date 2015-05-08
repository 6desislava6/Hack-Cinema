import sqlite3


class CreateDB:
    COL_SIZE = 10
    ROW_SIZE = 10

    def __init__(self):
        self.db = sqlite3.connect('HackCinema')
        # gets the response of the query in dict format
        # instead of a list
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Movies(
            movies_id INTEGER PRIMARY KEY,
            name TEXT,
            rating REAL) """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Projections(
            projections_id INTEGER PRIMARY KEY,
            movie_id INTEGER,
            projection_type TEXT,
            projection_date DATE,
            time TEXT,
            FOREIGN KEY (movie_id) REFERENCES Movies(movies_id)) """)

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS Reservations(
            reservations_id INTEGER PRIMARY KEY,
            username TEXT,
            projection_id INTEGER,
            row INTEGER,
            col INTEGER,
            FOREIGN KEY(projection_id) REFERENCES Projections(projections_id))
            """)

    def add_movie(self, name, rating):
        self.cursor.execute("""INSERT INTO Movies(name, rating)
                VALUES(?, ?)
            """, (name, rating))
        self.db.commit()

    def list_movies(self):
        return self.cursor.execute("""SELECT movies_id, name, rating
            FROM Movies
            """)

    def delete_movie(self, movie_id):
        self.cursor.execute("""DELETE FROM Movies
            WHERE movie_id = (?)
            """, (movie_id, ))
        self.db.commit()

    def add_projection(self, movie_id, projection_type, projection_date, time):
        self.cursor.execute("""INSERT INTO Projections(movie_id, projection_type, projection_date, time)
            VALUES(?, ?, ?, ?)
            """, (movie_id, projection_type, projection_date, time))
        self.db.commit()

    def list_projections(self):
        return self.cursor.execute(
            """SELECT a.projections_id, b.name, a.projection_type, a.projection_date, a.time
            FROM Projections AS a
            JOIN Movies AS b
            ON a.movie_id = b.movies_id
            """)

    def delete_projection(self, projection_id):
        self.cursor.execute("""DELETE FROM Projections
            WHERE projections_id = (?)
            """, (projection_id, ))
        self.db.commit()

    def are_enough_seats(self, wanted_seats, projection_id):
        self.cursor.execute("""SELECT Count(projection_id)
            FROM Reservations
            WHERE projection_id = ?
            """, (projection_id, ))
        data = self.cursor.fetchone()
        free_seats = CreateDB.ROW_SIZE * CreateDB.COL_SIZE - int(data['Count(projection_id)'])
        return free_seats >= wanted_seats

    def get_available_seats(self, wanted_projection):
        free_seats = [(i, j) for i in range(1, CreateDB.ROW_SIZE + 1) for j in range(1, CreateDB.COL_SIZE + 1)]
        self.cursor.execute("""SELECT row, col
            FROM Reservations
            WHERE projection_id = ?
            """, (wanted_projection, ))
        taken_seats = self.cursor.fetchall()
        for seat in taken_seats:
            free_seats.remove((seat['row'], seat['col']))
        return free_seats
        # free_seats is a list of tuples!

    def show_movie_projections(self, movie_id):
        return self.cursor.execute("""SELECT * FROM Projections
                                               JOIN Movies
                                               ON movie_id = movies_id
                                               WHERE movie_id = ?
                                               ORDER BY projection_date""",
                                   (movie_id, ))

    def make_reservation(self, username, projection_id, row, col):
        self.cursor.execute("""INSERT INTO Reservations(username, projection_id, row, col)
            VALUES (?, ?, ?, ?)
            """, (username, projection_id, row, col))
    # save_seat по стария начин
        self.db.commit()

    def undo_reservation(self, count):
        self.cursor.execute("""DELETE FROM Reservations
        WHERE reservations_id IN
        (SELECT reservations_id
         FROM Reservations
         ORDER BY reservations_id
         DESC LIMIT ?)""",
                            (count, ))
        self.db.commit()

    def show_last_n_reservations(self, count):
        return self.cursor.execute("""SELECT name, username, projection_date, row, col
        FROM (SELECT * FROM (SELECT * FROM Reservations
        WHERE reservations_id IN
        (SELECT reservations_id
         FROM Reservations
         ORDER BY reservations_id
         DESC LIMIT ?)) as a JOIN Projections as b
         ON a.projection_id = b.projections_id) as c
        JOIN Movies as d ON c.movie_id = d.movies_id
         """, (count, ))
