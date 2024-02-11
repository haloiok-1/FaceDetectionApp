import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
from Person import Person


class Phototaker:
    def __init__(self, parent, person: Person, directory_path: str):

        # self.mtcnn_detector = mtcnn.MTCNN()
        self.roi = None
        self.counter = 0
        self.current_person = person
        self.photo_directory = person.photo_folder_path
        self.working_directory = directory_path
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FPS, 60)
        self.is_Shooting = False

        # Create a window
        self.window = tk.Toplevel(parent)
        self.window.title("Photo Taker")

        # Create a label to display the camera stream
        self.video_label = tk.Label(self.window)
        self.video_label.pack()

        # Create a button to take photos
        self.photo_button = tk.Button(self.window, text="Take Photos", command=self.take_photos,
                                      padx=20, pady=10)
        # pack the button to the left of the window
        self.photo_button.pack(side="left")

        # button profile pic
        self.profile_pic_button = tk.Button(self.window, text="Set Profile Picture", command=self.set_profile_pic,
                                            padx=20, pady=10)
        self.profile_pic_button.pack(side="right")

        # label for amount of photos in folder
        self.amount_of_photos_label = tk.Label(self.window, text=f"Amount of photos: {self.current_amount_of_photos()}",
                                               padx=20, pady=10, font=("Arial", 14))
        self.amount_of_photos_label.pack()

        # create close button to close only this window
        self.close_button = tk.Button(self.window, text="Close", command=self.window.destroy, padx=20, pady=10)
        self.close_button.pack()

    def start(self):
        print(f"[PhotoTaker]: Starting the photo taker for {self.current_person.name} {self.current_person.lastname}")
        # Start the camera stream
        threading.Thread(target=self.display_camera_stream).start()
        self.window.mainloop()
        # Start the tkinter main loop
        # Release the camera resources
        self.camera.release()
        cv2.destroyAllWindows()

    # Create a function to display the camera stream
    def display_camera_stream(self):
        # Capture frame-by-frame
        ret, frame = self.camera.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # flip the frame
        frame = (cv2.flip(frame, 1))

        # center of the camera feed
        self.roi = (230, 150, 200, 200)
        # draw broder around region of interest
        cv2.rectangle(frame, (self.roi[0], self.roi[1]), (self.roi[0] + self.roi[2], self.roi[1] + self.roi[3]),
                      (255, 0, 0), 2)

        if not ret:
            print("[PhotoTaker]: No frame available")
            return

        # Load a pre-trained Haar Cascade model for face detection
        face_cascade = cv2.CascadeClassifier("Resources/Cascades/data/haarcascade_frontalface_default.xml")

        # Convert the frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detect faces in the frame
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=1, minSize=(50, 50))

        # Draw a green or red box around each detected face
        for (x, y, w, h) in faces:
            if len(faces) == 1:
                # check if only one face is in the region of interest
                if (x > self.roi[0] and y > self.roi[1] and x + w < self.roi[0]
                        + self.roi[2] and y + h < self.roi[1] + self.roi[3]):
                    self.photo_button.config(state="normal")
                    self.profile_pic_button.config(state="normal")

                if self.is_Shooting:
                    # Draw a red rectangle around the face if the camera is shooting
                    color = (255, 0, 0)  # red
                else:
                    # Draw a green rectangle around the face if the camera is not shooting and only one face is detected
                    color = (0, 255, 0)  # green
            else:
                # Disable the photo button if more than one face is detected
                # Draw a blue rectangle around the face if the camera is not shooting and more than one face is detected
                color = (0, 0, 255)  # blue

            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

        if len(faces) == 0:
            self.photo_button.config(state="disabled")
            self.profile_pic_button.config(state="disabled")

        # Convert the frame to a PIL Image
        img = Image.fromarray(frame)
        img_tk = ImageTk.PhotoImage(image=img)

        # Display the image in the tkinter label
        self.video_label.config(image=img_tk)
        self.video_label.image = img_tk

        self.amount_of_photos_label.config(text=f"Amount of Photos: {self.current_amount_of_photos()}")

        # Call the function again after 10 milliseconds
        self.window.after(10, self.display_camera_stream)

    def take_photos(self):
        photo_thread = threading.Thread(target=self.worker_take_photos)
        photo_thread.start()

        self.photo_button.config(text="Taking Photos...", state="disabled", background="grey")

    def worker_take_photos(self):
        self.is_Shooting = True
        counter = self.counter

        # check if the directory exists
        if not os.path.isdir(self.photo_directory):
            os.makedirs(self.photo_directory)

        while self.counter < counter + 100:
            ret, frame = self.camera.read()
            photo_path = f"{self.photo_directory}/photo_{self.counter}.jpg"
            # flip the frame
            frame = cv2.flip(frame, 1)
            # write the roi to the photo and save it
            cv2.imwrite(photo_path, frame[self.roi[1]:self.roi[1] + self.roi[3], self.roi[0]:self.roi[0] + self.roi[2]])
            self.counter += 1
            print(f"[PhotoTaker]: Photo {self.counter} saved to {photo_path}")

        self.photo_button.config(text="Take Photos", state="normal")
        self.is_Shooting = False

    def save_photos(self):
        pass

    def current_amount_of_photos(self):
        return len(os.listdir(self.photo_directory))

    def set_profile_pic(self):
        # create profile pic if it doesn't exist
        ret, frame = self.camera.read()
        if not ret:
            messagebox.showerror("Error", "Couldn't take a photo")

        profile_pic_path = f"{self.photo_directory}/profile_pic.jpg"
        cv2.imwrite(profile_pic_path, frame)
        self.current_person.profile_pic_path = profile_pic_path
        print(f"[PhotoTaker]: Profile picture set to {profile_pic_path}")


if __name__ == "__main__":
    p = Person(
        name="John",
        lastname="Doe",
        age=30,
        gender="male",
        profile_pic_path="path/to/profile.jpg",
        photo_folder_path="Resources/Persons/John_Doe",
    )
    pt = Phototaker(tk.Tk(), p, "Resources/Persons/")
    pt.start()
