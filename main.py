import cv2
import numpy as np
import pickle

print("Everything is imported")


def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2

    # Top left
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)

    # Top right
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)

    # Bottom left
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)

    # Bottom right
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)


cap = cv2.VideoCapture(0)

face_cascades = cv2.CascadeClassifier("Resources/Cascades/data/haarcascade_frontalface_alt.xml")

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels = {}
with open("labels.pickle", "rb") as f:
    og_labels = pickle.load(f)
    lables = {v: k for k, v in og_labels.items()}

while (True):
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascades.detectMultiScale(gray, scaleFactor=2, minNeighbors=5)

    for (x, y, w, h) in faces:
        # print(x, y, w, h)
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = gray[y:y + h, x:x + w]

        id_, conf = recognizer.predict(roi_gray)
        if 55 <= conf <= 90:
            # print(id_)
            # print(lables[id_])
            font = cv2.FONT_HERSHEY_SIMPLEX
            confRounded = round(conf, 1)
            name = ((lables[id_]) + " " + str(confRounded) + "%")
            color = (100, 255, 100)
            stroke = 1
            cv2.putText(img, name, (x, y - 5), font, 0.5, color, stroke, cv2.LINE_AA)

        color = (255, 0, 0)
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(img, (x, y), (end_cord_x, end_cord_y), color, stroke)
        # draw_border(img, (x, y), (end_cord_x, end_cord_y), color, stroke, 4, 10)

    cv2.imshow("Video", img)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
