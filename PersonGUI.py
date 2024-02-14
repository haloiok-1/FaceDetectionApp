import tkinter as tk
from tkinter import messagebox

from Person import Person, dict_to_person
import json


class PersonGUI:

    def __init__(self, master, working_directory: str):
        self.master = master
        self.persons = []

        self.working_directory = working_directory + "Persons/"
        self.master.title("Person GUI")
        self.master.geometry("800x600")

        self.label = tk.Label(self.master, text="Person GUI", font=("Arial", 20))
        # self.label.pack()

        self.get_persons_button = tk.Button(self.master, text="Get Persons", command=self.get_persons, padx=20, pady=10)
        # self.get_persons_button.pack()

        self.close_button = tk.Button(self.master, text="Close", command=self.master.destroy, padx=20, pady=10)
        # self.close_button.pack()

        self.start()

    def start(self):
        print("[PersonGUI]: Starting the person GUI")
        self.get_persons()

        self.create_grid_for_persons(self.persons)

        self.master.mainloop()

    def get_persons(self):
        try:
            with open(self.working_directory + "persons.json", "r") as file:
                persons = json.load(file)
        except FileNotFoundError:
            messagebox.showerror("Error", "No persons found")
            return

        for person in persons:
            self.persons.append(dict_to_person(person))
        print(f"[PersonGUI]: Found {len(self.persons)} persons")

    def create_grid_for_persons(self, persons: list[Person]):
        for i, p in enumerate(persons):

            # Create a name label for the person
            label = tk.Label(self.master, text=p.firstname + " " + p.lastname, font=("Arial", 14))
            label.grid(row=i, column=0)

            # create photo with the profile picture if it exists
            try:
                if p.profile_pic_path == "":
                    print(f"[PersonGUI]: Profile picture for {p.firstname} {p.lastname} not set")
                img = tk.PhotoImage(file=p.profile_pic_path)
                img_label = tk.Label(self.master, image=img)
                img_label.grid(row=i, column=1)
            except FileNotFoundError:
                print(f"[PersonGUI]: Profile picture for {p.firstname} {p.lastname} not found")

            # Create a button to open the persons photo folder
            button = tk.Button(self.master, text="Open photo folder",
                               command=lambda: print(f"Opening {p.photo_folder_path}"), padx=0, pady=10)
            button.grid(row=i, column=2)

            # Create a button to delete the person
            delete_button = tk.Button(self.master, text="Delete",
                                      command=lambda: self.delete_person(p), padx=0, pady=10, bg="red")
            delete_button.grid(row=i, column=3)

            # Create a button to open the photo taker
            photo_taker_button = tk.Button(self.master, text="Take Photos",
                                           command=lambda: print(f"Opening photo taker for {p.firstname} {p.lastname}"),
                                           padx=0, pady=10, bg="green")
            photo_taker_button.grid(row=i, column=4)

            # label for amount of photos in folder
            amount_of_photos_label = tk.Label(self.master, text=f"Amount of photos: {p.current_amount_of_photos()}",
                                              padx=20, pady=10, font=("Arial", 12))
            amount_of_photos_label.grid(row=i, column=5)





            # create a separator between the persons

    def delete_person(self, person: Person):
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = PersonGUI(root, "Resources/")
    root.mainloop()
