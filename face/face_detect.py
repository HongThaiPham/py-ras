import cv2
import os


HAAR_PATH = os.path.join(os.getcwd(), "face/haarcascade_frontalface_default.xml")
face_detector = cv2.CascadeClassifier(HAAR_PATH)


def face_detect(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    return faces
