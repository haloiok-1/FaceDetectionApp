import tkinter as tk
from tkinter import filedialog, messagebox


class App:
    def __init__(self, master):
        # Variables
        self.photo_directory = None
        self.master = master

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

        self.label_name = tk.Label(left_frame, text="Name")
        self.label_name.pack(pady=(10, 5))  # Add some padding above and below the label
        self.entry_name = tk.Entry(left_frame)
        self.entry_name.pack(pady=(0, 5))  # Add some padding below the entry

        self.label_age = tk.Label(left_frame, text="Age")
        self.label_age.pack(pady=(10, 5))  # Add some padding above and below the label
        self.entry_age = tk.Entry(left_frame)
        self.entry_age.pack(pady=(0, 5))  # Add some padding below the entry

        self.label_gender = tk.Label(left_frame, text="Gender")
        self.label_gender.pack(pady=(10, 5))  # Add some padding above and below the label
        self.entry_gender = tk.Entry(left_frame)
        self.entry_gender.pack(pady=(0, 20))  # Add some padding below the entry

        self.submit_button = tk.Button(left_frame, text="Submit", command=self.submit, padx=20, pady=10)
        self.submit_button.pack()

        # Add the labels and entries to the right frame
        self.label_takePhotos = tk.Label(right_frame, text="Fotos aufnehmen")
        self.label_takePhotos.pack(pady=(20, 10))  # Add some padding above and below the label

        self.photo_button = tk.Button(right_frame, text="Start Shooting", command="self.takePhotos", padx=20, pady=10)
        self.photo_button.pack()

        # Create a button to change the working directory
        self.wd_button = tk.Button(right_frame, text="Directory", command=self.change_directory,
                                   compound=tk.LEFT)
        self.wd_button.place(relx=1.0, rely=1.0, anchor=tk.SE)

    def submit(self):
        name = self.entry_name.get()
        age = self.entry_age.get()
        gender = self.entry_gender.get()

        print(f"Name: {name}, Age: {age}, Gender: {gender}")

    def change_directory(self):
        working_directory = tk.filedialog.askdirectory()
        if working_directory:
            print(f"Working directory changed to: {working_directory}")
            self.photo_directory = working_directory


# Create the main window
if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()