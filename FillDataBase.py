from create_database import CreateDB


class FillDataBase:

    @staticmethod
    def add_movies(db):
        db.add_movie('Big Hero 6', 100000)
        db.add_movie('The Hunger Games: Catching Fire', 7.9)
        db.add_movie('Wreck-It Ralph', 7.8)
        db.add_movie('Her', 8.3)
        db.add_movie('Up', 7.3)
        db.add_movie('How to Train Your Dragon', 8.2)
        db.add_movie('Monsters, Inc.', 8.1)

    @staticmethod
    def add_projections(db):
        db.add_projection(1, '3D', '2015-05-07', '11:00')
        db.add_projection(1, '2D', '2015-05-06', '12:00')
        db.add_projection(1, '4DX', '2015-05-05', '17:00')
        db.add_projection(2, '3D', '2015-05-05', '15:00')
        db.add_projection(2, '3D', '2015-05-04', '11:00')
        db.add_projection(3, '4DX', '2015-05-03', '10:00')
        db.add_projection(3, '3D', '2015-05-07', '09:00')
        db.add_projection(3, '3D', '2015-05-06', '09:00')
        db.add_projection(4, '2D', '2015-05-05', '09:00')
        db.add_projection(4, '3D', '2015-05-04', '09:00')
        db.add_projection(5, '3D', '2015-05-06', '09:00')
        db.add_projection(5, '2D', '2015-05-04', '20:00')
        db.add_projection(6, '3D', '2015-05-09', '22:00')
        db.add_projection(6, '2D', '2015-05-08', '21:00')
        db.add_projection(6, '2D', '2015-05-10', '12:00')
        db.add_projection(6, '3D', '2015-05-11', '22:00')
        db.add_projection(6, '3D', '2015-05-09', '22:00')
        db.add_projection(7, '2D', '2015-05-08', '09:00')
        db.add_projection(7, '2D', '2015-05-10', '11:00')
        db.add_projection(7, '3D', '2015-05-11', '20:00')


def main():
    db = CreateDB()
    FillDataBase.add_movies(db)
    FillDataBase.add_projections(db)


if __name__ == '__main__':
    main()
