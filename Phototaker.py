import cv2
import os
import shutil

print("Everything is imported")

photoid = 0
nameOfPerson = input("Name der Person, der diese Fotos gehören" + "\n")
cap = cv2.VideoCapture(0)
timer = 0

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "Resources/faces")

face_cascades = cv2.CascadeClassifier("Resources/Cascades/data/haarcascade_frontalface_default.xml")


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


os.chdir(image_dir)
os.mkdir(nameOfPerson)
print("Created Folder successfully")
os.chdir(nameOfPerson)

while (True):
    success, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascades.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

    # Foto aufnehmen und speichern
    timer += 1
    if timer > 10:
        cv2.imwrite(nameOfPerson + str(photoid) + ".png", gray)
        photoid += 1
        timer = 0
        print("Photo saved")

    # Position fürs facetracking
    for (x, y, w, h) in faces:
        # print(x, y, w, h)
        roi_gray = gray[y:y + h, x:x + w]
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(img, (x, y), (end_cord_x, end_cord_y), (255, 255, 255), 1)
        draw_border(img, (x, y), (end_cord_x, end_cord_y), (0, 255, 0), 2, 10, 10)
        cv2.putText(img, "Photos: " + str((photoid - 1)), (x, y - 5), cv2.FONT_HERSHEY_COMPLEX_SMALL, 0.5, (255, 255, 255),1)

    cv2.imshow("Video", img)
    if cv2.waitKey(1) & 0xFF == ord("q") or photoid > 400:
        break

cv2.destroyAllWindows()

print("breaked successfull" + "\n")

if input("Willst du die Fotos behalten?" + "\n") == "Yes":
    print("saved")
    pass

else:
    os.chdir('..')
    shutil.rmtree(nameOfPerson, ignore_errors=True)
    print("Everything deleted")
