import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import csv
from FaceDetector import FaceDetector
from Person import Person
from Phototaker import Phototaker
import threading
from Trainer import Trainer


class App:
    def __init__(self, master):
        # Variables
        self.trainingError = None
        self.amount_of_photos = 0
        self.current_person = None
        self.photo_directory = None
        self.working_directory = "Resources/"
        self.photo_directory = self.working_directory + "Persons/"
        self.master = master

        genders = self.import_csv_to_list(self.working_directory + "genders.csv")

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

        # button to see all current persons in the system
        self.showPersons_button = tk.Button(left_frame, text="Show Persons", command=self.showPersons, padx=20, pady=10)
        self.showPersons_button.pack()



        # Add the labels and entries to the right frame
        self.label_takePhotos = tk.Label(right_frame, text="Fotos aufnehmen")
        self.label_takePhotos.pack(pady=(20, 10))  # Add some padding above and below the label

        self.photo_button = tk.Button(right_frame, text="Start Shooting", command=self.start_phototaker,
                                      padx=20, pady=10, state="disabled")
        self.photo_button.pack()

        # Create a button to change the working directory
        self.wd_button = tk.Button(right_frame, text=self.working_directory, command=self.change_directory,
                                   compound=tk.LEFT)
        self.wd_button.place(relx=1.0, rely=1.0, anchor=tk.SE)

        self.training_label = tk.Label(right_frame, text="Face Training")
        self.training_label.pack(pady=(20, 0))
        self.training_button = tk.Button(right_frame, text="Start Training", command=self.start_face_training,
                                         padx=20, pady=5)
        self.training_button.pack()

        self.progress = ttk.Progressbar(right_frame, orient="horizontal", length=150, mode="determinate")
        self.progress.pack(pady=(10, 5))

        self.trainingstatus_label = tk.Label(right_frame, text="")
        self.trainingstatus_label.pack()

        # add a separator
        separator = ttk.Separator(right_frame, orient="horizontal")
        separator.pack(fill="x", pady=10)

        # label with headline for the face detection
        self.label_face_detection = tk.Label(right_frame, text="Face Detection", font=("Arial", 16, "bold"))
        self.label_face_detection.pack(pady=(10, 0))

        # button to start the face detection
        self.face_detection_button = tk.Button(right_frame, text="Start Face Detection",
                                               command=self.start_facedetector,
                                               padx=20, pady=10)
        self.face_detection_button.pack()

        # check if working directory exists
        if not os.path.exists(self.working_directory):
            os.mkdir(self.working_directory)

        # check if photo directory exists
        if not os.path.exists(self.photo_directory):
            os.mkdir(self.photo_directory)

    def submit(self):
        # check if folder with name already exists
        if os.path.exists(self.photo_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get()):
            messagebox.showinfo("Already Exists", "A folder with this name already exists", icon="info")
            self.photo_button.config(state="normal")
            return
        else:
            os.mkdir(self.photo_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get())

        self.current_person = Person(
            name=self.entry_firstname.get(),
            lastname=self.entry_lastname.get(),
            age=self.entry_age.get(),
            gender=self.entry_gender.cget("text"),
            profile_pic_path="",
            photo_folder_path=self.photo_directory + self.entry_firstname.get() + "_" + self.entry_lastname.get()
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

        print(f"[App]: Firstname: {firstname}, Lastname: {lastname}, Age: {age}, Gender: {gender}")
        self.saveInJSON()
        # os.mkdir(self.working_directory + firstname + "_" + lastname)
        self.photo_button.config(state="normal", borderwidth=5, relief="raised")

    def change_directory(self):
        working_directory = tk.filedialog.askdirectory(title="Changing Working Directory for depositing further Photos",
                                                       initialdir=self.working_directory)
        if working_directory:
            print(f"[App]: Working directory changed to: {working_directory}")
            self.working_directory = working_directory

            # check if the path is too long to display
            if len(working_directory) > 30:
                # use the last 3 words of the path
                self.wd_button.config(text=".../" + "/".join(working_directory.split("/")[-3:]))
            else:
                self.wd_button.config(text=working_directory)

    def saveInJSON(self):
        # open file to read and write in json format
        person_dict = {"firstname": self.current_person.name, "lastname": self.current_person.lastname,
                       "age": self.current_person.age, "gender": self.current_person.gender,
                       "profile_pic_path": "", "photo_folder_path": self.current_person.photo_folder_path}

        try:
            with open(self.photo_directory + "persons.json", "r") as f:
                lines = f.readlines()

            del lines[-1]
            last_line = lines[-1]

            # add to the penultimate line a comma
            last_line = last_line[:-1] + "," + "\n"
            lines[-1] = last_line

            with open(self.photo_directory + "persons.json", "w") as f:
                f.writelines(lines)
                # write the new person information
                json.dump(person_dict, f, indent=4)
                f.write("\n]")
                print(f"[App]: Informationen erfolgreich in {self.photo_directory}/persons.json gespeichert.")

        except Exception as e:
            print(f"[App]: {e}")
            print("[App]: File not found. Creating new file.")
            with open(self.photo_directory + "persons.json", "a") as f:
                f.write("[\n")
                json.dump(person_dict, f, indent=4)
                f.write("\n]")
                print(f"[App]: Informationen erfolgreich in {f} gespeichert.")

    def start_phototaker(self):
        print("[App]: Starting Phototaker")

        # print all information of the current person
        print(f"[App]: {self.current_person.photo_folder_path}")

        print("[App]:  " + self.working_directory)
        pt = Phototaker(self.master, self.current_person, self.photo_directory)
        pt.start()

    def start_face_training(self):
        print("[App]: Starting Face Training")
        face_recognizer = Trainer(self.working_directory, self.photo_directory,
                                  "Resources/Cascades/data/haarcascade_frontalface_default.xml")
        threading.Thread(target=self.worker_face_training, args=(face_recognizer,)).start()

        # disable the button
        self.training_button.config(state="disabled", text="Training...", background="grey")

        # progress bar
        # get amount of training photos
        self.amount_of_photos = 0
        self.amout_of_photos()
        amount_of_photos = self.amount_of_photos

        self.progress["maximum"] = amount_of_photos + 3
        self.progress["value"] = 0
        self.trainingstatus_label.config(fg="black")

        while self.progress["value"] < self.progress["maximum"]:
            self.progress["value"] = face_recognizer.getTrainingStatus()
            self.master.update_idletasks()
            self.master.update()

            # update the label with the precentage of the training
            self.trainingstatus_label.config(
                text=f"Training Status: {int(100 * self.progress['value'] / self.progress['maximum'])}%")

            # if something goes wrong with the training
            if self.trainingError:
                self.trainingstatus_label.config(text="Training failed", fg="red")
                break

        # enable the button again
        self.training_button.config(state="normal", text="Start Training", background="SystemButtonFace")
        self.trainingstatus_label.config(text="Training complete", fg="green")

    def worker_face_training(self, face_recognizer):
        self.trainingError = face_recognizer.process()
        return self.trainingError, print("[App]: Training complete")

    def start_facedetector(self):
        print("[App]:Starting Face Detector")
        fd = FaceDetector(self.master, self.working_directory)
        fd.start()


    def showPersons(self):
        persons = []
        with open(self.photo_directory + "persons.json", "r") as f:
            persons = json.load(f)
        print(persons)
        for person in persons:
            print(f"Name: {person['firstname']} {person['lastname']}, Age: {person['age']}")
            messagebox.showinfo("Persons", person, icon="info")






    def amout_of_photos(self):
        for root, dirs, files in os.walk(self.working_directory):
            for file in files:
                if file.endswith("jpg"):
                    self.amount_of_photos += 1

    def import_csv_to_list(self, file_path):
        if not os.path.exists(file_path):
            data = ["male", "female", "diverse"]
            return data

        with open(file_path, "r") as csv_file:
            csv_reader = csv.reader(csv_file)
            data = []
            for row in csv_reader:
                data.append("".join(row))

            return data


# Create the main window
if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()
