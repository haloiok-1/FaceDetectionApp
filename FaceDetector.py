import cv2
import numpy as np
import pickle
import tkinter as tk
from PIL import Image, ImageTk
import threading


class FaceDetector:

    def __init__(self, parent, working_directory):
        self.running = True
        self.img = None
        self.cap = cv2.VideoCapture(0)
        self.face_cascades = cv2.CascadeClassifier("Resources/Cascades/data/haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("trainner.yml")
        self.labels = {}

        with open("labels.pickle", "rb") as f:
            og_labels = pickle.load(f)
            self.labels = {v: k for k, v in og_labels.items()}
        self.parent = parent
        self.working_directory = working_directory

        # Create a window
        self.window = tk.Toplevel(parent)
        self.window.title("Face Detector")

        # Create a label to display the camera stream
        self.video_label = tk.Label(self.window)
        self.video_label.pack()

        # create a thread for the face detection
        self.thread = threading.Thread(target=self.detect_faces)
        self.video_label_thread = threading.Thread(target=self.display_camera_stream)

        # Start the thread
        self.thread.start()
        self.video_label_thread.start()

        self.close_button = tk.Button(self.window, text="Close", command=self.stop, padx=20, pady=10)
        self.close_button.pack()

    def detect_faces(self):
        while self.running:
            success, img = self.cap.read()
            # flip the frame
            img = cv2.flip(img, 1)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascades.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                roi_gray = gray[y:y + h, x:x + w]
                id_, conf = self.recognizer.predict(roi_gray)
                if 55 <= conf <= 90:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    confRounded = round(conf, 1)
                    name = ((self.labels[id_]) + " " + str(int(confRounded)) + "%")
                    color = (100, 255, 100)
                    stroke = 1
                    name = name.replace("_", " ")
                    name = name.title()
                    cv2.putText(img, name, (x, y - 5), font, 0.5, color, stroke, cv2.LINE_AA)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (100, 255, 100), 2)
                else:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    name = "Unknown"
                    color = (0, 0, 255)
                    stroke = 1
                    cv2.putText(img, name, (x, y - 5), font, 0.5, color, stroke, cv2.LINE_AA)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # writing the processed image to the img variable
            self.img = img

        print("Face detection closed")

    def display_camera_stream(self):
        while self.running:
            if self.img is not None:
                # Convert the frame to a PIL Image
                img = Image.fromarray(self.img)
                img_tk = ImageTk.PhotoImage(image=img)

                # Display the image in the tkinter label
                self.video_label.config(image=img_tk)
                self.video_label.image = img_tk
        else:
            print("No image to display")

        print("Video stream closed")

    def start(self):
        print("Starting the Face Detector...")
        self.window.mainloop()
        self.running = True

    def stop(self):
        self.running = False
        self.cap.release()
        self.window.destroy()
        print("Face Detector closed")


if __name__ == "__main__":
    root = tk.Tk()
    app = FaceDetector(root, "Resources")
    app.running = True
    app.start()