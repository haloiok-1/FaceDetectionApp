import os
import pickle
import numpy as np
from PIL import Image
import cv2


class Trainer:
    def __init__(self, image_dir, cascade_path):
        self.amount_of_photos = 0
        self.image_dir = image_dir
        self.face_cascades = cv2.CascadeClassifier(cascade_path)
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.current_id = 0
        self.label_ids = {}
        self.x_train = []
        self.y_labels = []
        self.trainingStatus = 0

    def load_images(self):
        print("Loading images...")
        for root, dirs, files in os.walk(self.image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg") or file.endswith("PNG"):
                    self.amount_of_photos = len(files)
                    path = os.path.join(root, file)
                    label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
                    # print(path, label)

                    if label in self.label_ids:
                        pass
                    else:
                        self.label_ids[label] = self.current_id
                        self.current_id += 1

                    id_ = self.label_ids[label]
                    pil_image = Image.open(path).convert("L")
                    size = (550, 550)
                    final_image = pil_image.resize(size)
                    image_array = np.array(final_image, "uint8")
                    # print(len(image_array))
                    faces = self.face_cascades.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5,
                                                                minSize=(30, 30))

                    for (x, y, w, h) in faces:
                        roi = np.array(image_array[y:y + h, x:x + w])
                        self.x_train.append(roi)
                        self.y_labels.append(id_)

                    # convert the image to a numpy array
                    image_array = np.array(pil_image, "uint8")

                    # update the training status for the GUI
                    self.trainingStatus += 1
                    # print all known labels as strings




    def check_data(self):
        if len(self.x_train) == 0 or len(self.y_labels) == 0:
            print("Training data is empty. Please provide more data.")
            return False

        if len(self.x_train) < 2 or len(self.y_labels) < 2:
            print("Not enough training data.")
            return False

        self.trainingStatus += 1

    def train(self):
        self.recognizer.train(self.x_train, np.array(self.y_labels))
        self.recognizer.save("trainner.yml")
        print("Training complete")

        self.trainingStatus += 1

    def save_labels(self):
        with open("labels.pickle", "wb") as f:
            pickle.dump(self.label_ids, f)
        print("Labels saved")

        self.trainingStatus += 1

    def process(self):
        self.load_images()
        self.check_data()
        self.train()
        self.save_labels()

    def getTrainingStatus(self):
        return self.trainingStatus

    def getAmountOfPhotos(self):
        return self.amount_of_photos


if __name__ == "__main__":
    recognizer = Trainer("Resources/Persons", "Resources/Cascades/data/haarcascade_frontalface_alt.xml")
    recognizer.process()
