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
