import tkinter as tk
from PIL import Image, ImageTk
import cv2

from Person import Person


class Phototaker:
    def __init__(self, person, directory_path):
        self.current_person = person
        self.photo_directory = person.photo_folder_path
        self.working_directory = directory_path
        self.camera = cv2.VideoCapture(0)

        # Create a window
        self.window = tk.Tk()
        self.window.title("Camera Stream with tkinter")

        # Create a label to display the camera stream
        self.video_label = tk.Label(self.window)
        self.video_label.grid(row=0, column=0, columnspan=2)

        # Create a button to take photos
        self.photo_button = tk.Button(self.window, text="Take Photos", command="self.take_photos", padx=20, pady=10)
        self.photo_button.grid(row=1, column=0)

        self.display_camera_stream()

        self.window.mainloop()

        # Release the camera resources
        self.camera.release()
        cv2.destroyAllWindows()

    # Create a function to display the camera stream
    def display_camera_stream(self):
        # Capture frame-by-frame
        ret, frame = self.camera.read()

        # Convert the frame to a PIL Image
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)

        # Display the image in the tkinter label
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk

        # Call the function again after 10 milliseconds
        self.window.after(10, self.display_camera_stream)


if __name__ == "__main__":
    p = Person(
        name="John",
        lastname="Doe",
        age=30,
        gender="male",
        profile_pic_path="path/to/profile.jpg",
        photo_folder_path="path/to/photo/folder",
    )
    pt = Phototaker(p, "Resources/Persons")
