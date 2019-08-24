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


# def main():
#     # cam = init_cam()
#     count = 0
#     while True:
#         # ret, img = cam.read()
#         img = kinect.get_image()

#         # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         # faces = face_detector.detectMultiScale(gray, 1.3, 5)
#         # for (x, y, w, h) in faces:
#         #     cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
#         #     count += 1
#         #     # Save the captured image into the datasets folder
#         #     print("face deteted ..., waitting for save")
#         #     cv2.imwrite(
#         #         DATASET_PATH + "/face." + str("t5l") + "." + str(count) + ".jpg",
#         #         img[y + 1 : y + h - 1, x + 1 : x + w - 1],
#         #     )
#         #     print("save done")
#         #     cv2.imshow("image", img)
#         cv2.imshow("image", img)
#         k = cv2.waitKey(1) & 0xFF  # Press 'ESC' for exiting video
#         if k == 27:
#             break

#     cam.release()
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     main()
