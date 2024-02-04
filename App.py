import os
import tkinter as tk
from tkinter import filedialog, messagebox
import json
from Person import Person
from Phototaker import Phototaker
import threading


class App:
    def __init__(self, master):
        # Variables
        self.current_person = None
        self.photo_directory = None
        self.working_directory = "Resources/Persons/"
        self.master = master

        genders = [
            "Male",
            "Female",
            "Non-binary",
            "Transgender",
            "Agender",
            "Genderqueer",
            "Genderfluid",
            "Intersex",
            "Two-Spirit",
            "Prefer not to say",
        ]

        master.title("Person Detector")
        master.geometry("500x400")  # Setzt die Größe des Fensters auf 600x400 Pixel

        # Create a frame for the left column
        left_frame = tk.Frame(master)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, )

        # Create a frame for the right column
        right_frame = tk.Frame(master)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Add the labels and entries to the left frame
        self.label_information_title = tk.Label(left_frame, text="Information", font=("Arial", 16, "bold"))
        self.label_information_title.pack(pady=(10, 20))

        self.label_firstname = tk.Label(left_frame, text="Name")
        self.label_firstname.pack(pady=(10, 5))  # Add some padding above and below the label
        self.entry_firstname = tk.Entry(left_frame)
        self.entry_firstname.pack(pady=(0, 5))  # Add some padding below the entry

        self.label_lastname = tk.Label(left_frame, text="Lastname")
        self.label_lastname.pack(pady=(1, 5))
        self.entry_lastname = tk.Entry(left_frame)
        self.entry_lastname.pack(pady=(0, 5))

        self.label_age = tk.Label(left_frame, text="Age")
        self.label_age.pack(pady=(10, 5))  # Add some padding above and below the label
        self.entry_age = tk.Entry(left_frame)
        self.entry_age.pack(pady=(0, 5))  # Add some padding below the entry

        self.label_gender = tk.Label(left_frame, text="Gender")
        self.label_gender.pack(pady=(1, 5))  # Add some padding above and below the label
        selected = tk.StringVar()
        self.entry_gender = tk.OptionMenu(left_frame, selected, *genders)
        self.entry_gender.pack(pady=(0, 20))
        self.entry_gender.config(width=15)

        self.submit_button = tk.Button(left_frame, text="Submit", command=self.submit, padx=20, pady=10)
        self.submit_button.pack()

        # Add the labels and entries to the right frame
        self.label_takePhotos = tk.Label(right_frame, text="Fotos aufnehmen")
        self.label_takePhotos.pack(pady=(20, 10))  # Add some padding above and below the label

        self.photo_button = tk.Button(right_frame, text="Start Shooting", command=self.start_Phototaker,
                                      padx=20, pady=10)
        self.photo_button.pack()

        # Create a button to change the working directory
        self.wd_button = tk.Button(right_frame, text=self.working_directory, command=self.change_directory,
                                   compound=tk.LEFT)
        self.wd_button.place(relx=1.0, rely=1.0, anchor=tk.SE)

    def submit(self):
        # check if folder with name already exists
        if os.path.exists(self.working_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get()):
            messagebox.showinfo("Already Exists", "A folder with this name already exists", icon="info")
            self.photo_button.config(state="normal")
            return
        else:
            photo_directory = self.working_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get()
            os.mkdir(self.working_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get())

        self.current_person = Person(
            name=self.entry_firstname.get(),
            lastname=self.entry_lastname.get(),
            age=self.entry_age.get(),
            gender=self.entry_gender.cget("text"),
            profile_pic_path="",
            photo_folder_path=self.working_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get()
        )

        firstname = self.entry_firstname.get()
        lastname = self.entry_lastname.get()
        age = self.entry_age.get()
        gender = self.entry_gender.cget("text")

        # check if all fields are filled
        if not firstname or not lastname or not age:
            messagebox.showerror("Error", "Please fill all fields", icon="error")
            return
        # check if age is a number
        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a number", icon="error")
            return

        # check if a gender selected
        if not gender:
            messagebox.showerror("Error", "Please select a gender from the dropdown", icon="error")
            return

        # ask if really want to submit
        if not messagebox.askyesno("Submit", "Do you really want to submit?"):
            return

        print(gender)

        print(f"Firstname: {firstname}, Lastname: {lastname}, Age: {age}, Gender: {gender}")
        # self.saveInJSON(self.working_directory)
        # os.mkdir(self.working_directory + firstname + "_" + lastname)
        self.photo_button.config(state="normal", borderwidth=5, relief="raised")

    def change_directory(self):
        working_directory = tk.filedialog.askdirectory(title="Changing Working Directory for depositing further Photos",
                                                       initialdir=self.working_directory)
        if working_directory:
            print(f"Working directory changed to: {working_directory}")
            self.working_directory = working_directory
            self.wd_button.config(text=working_directory)

    def saveInJSON(self, folder_path, person_folder_path):
        # open file to read and write in json format
        person_dict = {"firstname": self.entry_firstname.get(), "lastname": self.entry_lastname.get(),
                       "age": self.entry_age.get(), "gender": self.entry_gender.cget("text"),
                       "profile_pic_path": "", "photo_folder_path": person_folder_path}

        try:
            with open(folder_path + "persons.json", "r") as f:
                lines = f.readlines()

            del lines[-1]

            with open(folder_path + "persons.json", "w") as f:
                print(lines)
                f.writelines(lines)
                f.writelines(json.dumps(person_dict))
                f.write(",\n")
                f.write("}")
                print(f"Informationen erfolgreich in {f} gespeichert.")

        except Exception as e:
            print(e)
            with open(folder_path + "persons.json", "a") as f:
                f.write("{\n")
                f.write("    \"Version\": \"1.0\",\n")
                json.dump(person_dict, f)
                f.write(",\n}")
                print(f"Informationen erfolgreich in {f} gespeichert.")

    def start_Phototaker(self):
        print("Starting Phototaker")

        # print all information of the current person
        print(self.current_person.photo_folder_path)

        print(self.working_directory)
        pt = Phototaker(self.master, self.current_person, self.working_directory)
        pt.start()


# Create the main window
if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()
