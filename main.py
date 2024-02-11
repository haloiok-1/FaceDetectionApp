import cv2
import numpy as np
import pickle

print("Everything is imported")

cap = cv2.VideoCapture(0)

face_cascades = cv2.CascadeClassifier("Resources/Cascades/data/haarcascade_frontalface_default.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
print("Training data loaded")

labels = {}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    lables = {v: k for k, v in og_labels.items()}

    # print only the names in the labels
    print("Labels loaded: \n", lables)

while (True):
    success, img = cap.read()

    #flip the frame
    img = cv2.flip(img, 1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascades.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # print(x, y, w, h)
        roi_gray = gray[y:y + h, x:x + w]

        id_, conf = recognizer.predict(roi_gray)
        if 55 <= conf <= 90:
            font = cv2.FONT_HERSHEY_SIMPLEX
            confRounded = round(conf, 1)
            name = ((lables[id_]) + " " + str(int(confRounded)) + "%")
            color = (100, 255, 100)
            stroke = 1

            # refomating the name
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




    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
