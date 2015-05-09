import tkinter as tk
from tkinter import *
from create_database import CreateDB
from tkinter import messagebox


class GUI:

    def __init__(self):
        self.master = tk.Tk()
        self.cinema_database = CreateDB()
        self.buttons = {}
        self.make_username_field()
        # self.make_quantity_field()
        self.make_movie_list()
        self.clicked = []
        mainloop()

    def make_username_field(self):
        self.username_ment = StringVar()
        # What is typed is stored in ment
        username_entry = Entry(self.master, textvariable=self.username_ment).pack()
        self.confirm_name_btn = tk.Button()
        self.confirm_name_btn["text"] = "Confirm name"
        self.confirm_name_btn["command"] = self.get_username
        self.confirm_name_btn.pack()

    def get_username(self):
        self.username = self.username_ment.get()
        return self.username

    def make_quantity_field(self):
        self.quantity_spinbox = Spinbox(self.master, from_=1, to=20)
        self.quantity_spinbox.pack()
        self.confirm_quantity_btn = tk.Button()
        self.confirm_quantity_btn["text"] = "Confirm quantity of tickets"
        self.confirm_quantity_btn["command"] = self.get_quantity_field
        self.confirm_quantity_btn.pack()

    def get_quantity_field(self):
        return self.quantity_spinbox.get()

    def make_movie_list(self):
        self.listbox = Listbox(self.master, width=50)
        self.listbox.pack()
        for item in self.cinema_database.list_movies():
            name = item['name']
            movies_id = item['movies_id']
            data = '{}. {}'.format(movies_id, name)
            self.listbox.insert(END, data)

        self.confirm_movie_btn = tk.Button()
        self.confirm_movie_btn["text"] = "Confirm movie"
        self.confirm_movie_btn["command"] = self.confirm_movie
        self.confirm_movie_btn.pack()

    # Returns the ID of a movie
    def confirm_movie(self):
        all_data = self.listbox.get(ACTIVE).split('.')
        self.make_projections(all_data[0])
        return all_data[0]

    def make_projections(self, movies_id):
        self.listbox_projection = Listbox(self.master, width=50)
        self.listbox_projection.pack()
        for item in self.cinema_database.show_movie_projections(movies_id):
            movie_name = item['name']
            projections_id = item['projections_id']
            projection_date = item['projection_date']
            projection_type = item['projection_type']
            data = '{}. {} type: {} -> name: {}'.format(projections_id, projection_date, projection_type, movie_name)
            self.listbox_projection.insert(END, data)

        self.confirm_projection_btn = tk.Button()
        self.confirm_projection_btn["text"] = "Confirm projection"
        self.confirm_projection_btn["command"] = self.confirm_projection
        self.confirm_projection_btn.pack()

    def confirm_projection(self):
        all_data = self.listbox_projection.get(ACTIVE).split('.')
        projection_id = all_data[0]
        self.listbox_projection.destroy()
        self.confirm_projection_btn.destroy()
        self.createBoard(projection_id)

    @staticmethod
    def __hash(id_seat):
        col = -1
        row = id_seat // 10 + 1
        col = id_seat % 10 + 1
        return (row, col)

    # Makes a boad, returns saved places
    def createBoard(self, projection_id):
        tuples_seats = self.cinema_database.get_available_seats(projection_id)
        clicked = []
        toplevel = Toplevel()
        toplevel.geometry("400x400+580+100")
        buttonNum = 0
        x = -300
        y = 65

        def makeChoice(event):
            clicked.append(self.buttons[event.widget])

        def dismiss():
            count_reserved = 0
            for id_seat in clicked:
                seat = GUI.__hash(id_seat)
                if (seat[0], seat[1]) in tuples_seats:
                    count_reserved += 1
                    self.cinema_database.make_reservation(self.get_username(), projection_id, seat[0], seat[1])

            message = self.show_reservations(count_reserved)
            messagebox.showinfo(title='reservations', message=message, width=3)
            toplevel.destroy()
            return

        for b in range(1, 11):
            for b2 in range(1, 11):
                color = 'red'
                if (b, b2) in tuples_seats:
                    color = 'green'
                button = Button(
                    toplevel, text=b2, font="Courier 6", width=2, bd=3, bg=color)
                button.place(relx=1, x=x, y=y)
                self.buttons[button] = buttonNum
                buttonNum += 1
                button.bind("<Button-1>", makeChoice)
                x += 25
            x = -300
            y += 26

        button = Button(toplevel, text="Confirm", command=dismiss)
        button.pack()

    def show_reservations(self, count):
        reservations_raw = self.cinema_database.show_last_n_reservations(count)
        info = ''
        for line in reservations_raw:
            name = line['username']
            projection_date = line['projection_date']
            movie_name = line['name']
            row = line['row']
            col = line['col']
            reservation = 'username: {}, movie: {} ---> {}, place ({}, {})'.format(name, movie_name, projection_date, row, col)
            info += reservation + '\n'
        return info

