import cv2
import os
import datetime

# declare constant
HAAR_PATH = "/home/leo/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
DATASET_PATH = "/home/leo/leo/py-ras/face/dataset/"

print("app running ...")
print("openning camera ...")


# init cam
cam = cv2.VideoCapture(0)
cam.set(3, 640)  # set video width
cam.set(4, 480)  # set video height
face_detector = cv2.CascadeClassifier(HAAR_PATH)

count = 0
while True:
    ret, img = cam.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        count += 1
        # Save the captured image into the datasets folder
        print("face deteted ..., waitting for save")
        cv2.imwrite(
            DATASET_PATH + "/face." + str("t5l") + "." + str(count) + ".jpg",
            img[y + 1 : y + h - 1, x + 1 : x + w - 1],
        )
        print("save done")
        cv2.imshow("image", img)
    cv2.imshow("image", img)
    k = cv2.waitKey(100) & 0xFF  # Press 'ESC' for exiting video
    if k == 27:
        break

cam.release()
cv2.destroyAllWindows()
