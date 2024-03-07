import os
import shutil
import tkinter as tk
from tkinter import messagebox, filedialog

import cv2

from Phototaker import Phototaker
from PIL import Image, ImageTk

from Person import Person, dict_to_person
import json


def createPersonsJSON(working_directory):
    with open(working_directory + "persons.json", "w") as file:
        json.dump([], file, indent=4)
    print(f"[PersonGUI]: Created persons.json file at {working_directory}")


class PersonGUI:

    def __init__(self, master, working_directory: str):
        self.master = master
        self.persons = []

        self.working_directory = working_directory + "Persons/"

        # create title frame
        self.title_frame = tk.Frame(self.master)
        # expand the frame to fill the top half of the window
        self.title_frame.pack(fill="both")



        self.separator = tk.Frame(height=2, bd=1, relief="sunken")
        self.separator.pack(fill="x")

        # create a grid frame
        self.grid_frame = tk.Frame(self.master)
        # expand the frame to fill the top half of the window
        self.grid_frame.pack(expand=True, fill="both")

        # create separator
        self.separator = tk.Frame(height=2, bd=1, relief="sunken")
        self.separator.pack(fill="x")

        # create bottom frame
        self.bottom_frame = tk.Frame(self.master)
        # expand the frame to fill the bottom half of the window
        self.bottom_frame.pack(fill="both")

        self.title_label = tk.Label(self.title_frame, text="List of known Persons", font=("Arial", 18))
        self.title_label.pack()



        self.get_persons_button = tk.Button(self.bottom_frame, text="Get Persons", command=self.get_persons, padx=20,
                                            pady=10)
        self.get_persons_button.pack(side="left")

        self.close_button = tk.Button(self.bottom_frame, text="Close", command=self.master.destroy, padx=20, pady=10)
        # put the button to the right of the window
        self.close_button.pack(side="right")

        # add an update button
        self.update_button = tk.Button(self.bottom_frame, text="Update", command=self.update_grid, padx=20,
                                       pady=10)
        # pin the button to the bottom of the window
        self.update_button.pack(side="bottom")

        self.amount_persons_label = tk.Label(self.title_frame, text="Initialising...",
                                             font=("Arial", 12))
        self.amount_persons_label.pack()

    def start(self):
        print("[PersonGUI]: Starting the person GUI")
        self.get_persons()

        # get amount folders in the persons folder
        amount_of_folders = len([name for name in os.listdir(self.working_directory) if
                                 os.path.isdir(os.path.join(self.working_directory, name))])
        self.amount_persons_label.config(text=f"Amount of persons: {amount_of_folders}")

        self.create_grid_for_persons()

    def get_persons(self):
        self.persons = []

        try:
            with open(self.working_directory + "persons.json", "r") as file:
                persons = json.load(file)

        except Exception as e:
            if type(e) is FileNotFoundError:
                createPersonsJSON(self.working_directory)
            if type(e) is PermissionError:
                messagebox.showerror("Error", "You do not have permission to access the persons.json file.")
            if type(e) is json.decoder.JSONDecodeError:
                messagebox.showerror("Error", "Your persons.json file is corrupted. Please fix it or delete it.")
            return

        for person in persons:
            self.persons.append(dict_to_person(person))
        print(f"[PersonGUI]: Found {len(self.persons)} persons")

    def create_grid_for_persons(self):
        camera_connected = check_if_camera_is_connected()

        persons = self.persons

        for i, p in enumerate(persons):

            # Create a name label for the person
            label = tk.Label(self.grid_frame, text=p.firstname + " " + p.lastname, font=("Arial", 12, "bold"))
            label.grid(row=i, column=0)

            # Create a button to open the persons photo folder
            button = tk.Button(self.grid_frame, text="Open photo folder",
                               command=lambda p=p: self.open_fileexplorer_for_person(p), padx=0, pady=10)
            button.grid(row=i, column=2)

            # Create a button to delete the person
            delete_button = tk.Button(self.grid_frame, text="Delete",
                                      command=lambda p=p: self.delete_person(p), padx=0, pady=10, bg="#BD263C")
            delete_button.grid(row=i, column=3)

            # Create a button to open the photo taker
            photo_taker_button = tk.Button(self.grid_frame, text="Take Photos",
                                           command=lambda p=p: self.open_photo_taker(p),
                                           padx=0, pady=10, bg=("#32936F"))
            if not camera_connected:
                photo_taker_button.config(state="disabled")

            photo_taker_button.grid(row=i, column=4)

            # label for amount of photos in folder
            amount_of_photos_label = tk.Label(self.grid_frame, text=f"Amount of photos: {p.current_amount_of_photos()}",
                                              padx=20, pady=10, font=("Arial", 12, "italic"),
                                              fg="black" if p.current_amount_of_photos() > 100 else "#BD263C")
            amount_of_photos_label.grid(row=i, column=5)

    def open_fileexplorer_for_person(self, person: Person):
        # just to see the photos in the folder
        tk.filedialog.askopenfiles(initialdir=person.photo_folder_path, title="Select folder",
                                   filetypes=(("all files", "*.*"),))

    def delete_person(self, person: Person):
        # ask if the user is sure
        response = messagebox.askyesno("Delete",
                                       f"Are you sure you want to delete {person.firstname} {person.lastname}?")
        if response:
            # delete the person
            self.persons.remove(person)

            # delete the person from the file
            with open(self.working_directory + "persons.json", "w") as file:
                json.dump([p.__dict__ for p in self.persons], file, indent=4)

            # delete the photo folder
            # check if the directory exists
            if os.path.isdir(person.photo_folder_path):
                # delete the directory with all its content
                shutil.rmtree(person.photo_folder_path)
                print(f"[PersonGUI]: Deleted {person.photo_folder_path}")

            self.update_grid()

        else:
            print(f"[PersonGUI]: Did not delete {person.firstname} {person.lastname}")

    def open_photo_taker(self, person: Person):
        # open the photo taker for the person
        Phototaker(self.master, person, self.working_directory).start()

    def update_grid(self):
        self.get_persons()
        # destroy all widgets in the grid frame
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
        # create the grid again
        self.create_grid_for_persons()


def check_if_camera_is_connected() -> bool:
    img = cv2.VideoCapture(0)  # check if the camera is connected
    check = img.isOpened()
    img.release()
    return check




if __name__ == "__main__":
    root = tk.Tk()
    app = PersonGUI(root, "Resources/")
    root.mainloop()
