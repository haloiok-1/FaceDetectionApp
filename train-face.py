import os
import pickle
import numpy as np
from PIL import Image
import cv2

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "Resources\Persons")

face_cascades = cv2.CascadeClassifier("Resources/Cascades/data/haarcascade_frontalface_alt2.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()

current_id = 0
label_ids = {}
x_train = []
y_labels = []

for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg") or file.endswith("PNG"):
            path = os.path.join(root, file)
            label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()
            print(path, label)

            if label in label_ids:
                pass
            else:
                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]
            print(label_ids.values())
            pil_image = Image.open(path).convert("L")
            size = (550, 550)
            final_image = pil_image.resize(size)
            image_array = np.array(pil_image, "uint8")
            print(len(image_array))
            faces = face_cascades.detectMultiScale(image_array, scaleFactor=2, minNeighbors=5)

            for (x, y, w, h) in faces:
                roi = image_array[y:y + h, x:x + w]
                x_train.append(roi)
                y_labels.append(id_)

# print(y_labels)
print(x_train)
'''
with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

if len(x_train) == 0 or len(y_labels) == 0:
    print("Training data is empty. Please provide more data.")
    exit()

if not isinstance(x_train, np.ndarray) or not isinstance(y_labels, np.ndarray):
    print("Training data is not a NumPy array.")
    exit()

if x_train.ndim != 2 or y_labels.ndim != 1:
    print("Training data has incorrect dimensions.")
    exit()

if len(x_train) < 2 or len(y_labels) < 2:
    print("Not enough training data.")
    exit()

print(f"First face: {x_train[0]}, Label: {y_labels[0]}")
print(f"Second face: {x_train[1]}, Label: {y_labels[1]}")

'''
recognizer.train(x_train, np.array(y_labels))
recognizer.save("trainner.yml")
