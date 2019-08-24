import cv2

# import kinect
import picam
from face_detect import face_detect
import os


DATASET_PATH = os.path.join(os.getcwd(), "face/dataset")

count = 0
while True:
    # ret, img = cam.read()
    img = picam.get_image()
    faces = face_detect(img)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 1)
        count += 1
        # Save the captured image into the datasets folder
        print("face detected ..., waitting for save")
        cv2.imwrite(
            DATASET_PATH + "/face." + str("t5l") + "." + str(count) + ".jpg",
            img[y + 1 : y + h - 1, x + 1 : x + w - 1],
        )
        print("Save done")
        cv2.imshow("image", img)
    cv2.imshow("image", img)
    k = cv2.waitKey(1) & 0xFF  # Press 'ESC' for exiting video
    if k == 27:
        break

picam.detroy()
cv2.destroyAllWindows()
