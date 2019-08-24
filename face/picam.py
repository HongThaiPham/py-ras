import cv2

RESOLUTIONX = 640
RESOLUTIONY = 480


cam = cv2.VideoCapture(0)
cam.set(3, RESOLUTIONX)  # set video width
cam.set(4, RESOLUTIONY)  # set video height


def get_image():
    ret, img = cam.read()
    return img


def detroy():
    cam.release()

