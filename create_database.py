import sqlite3


class CreateDB:
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
            projection_id INTEGER
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
