import cv2

# import kinect
import picam
from face_detect import face_detect
import os
from datetime import datetime
import time
from gdrive import upload_dataset, writeImageToGDrive, getFolderfromGDrive


current_milli_time = lambda: int(round(time.time() * 1000))


DATASET_PATH = os.path.join(os.getcwd(), "face/dataset")
BORDER_WIDTH = 1


def get_path_file(name):
    folder_name = "face_" + datetime.now().strftime("%Y%m%d")
    directory = os.path.join(DATASET_PATH, folder_name)
    if not os.path.exists(directory):
        os.makedirs(directory)
    return {"name": name, "path": os.path.join(directory, name)}


def save_image(image, name):
    file_path = get_path_file(name)
    cv2.imwrite(file_path["path"], image)
    # time.sleep(1)
    # writeImageToGDrive(name, file_path["path"], getFolderfromGDrive(file_path["name"]))
    print("Save done")


print("1. Collect data")
print("2. Upload dataset to GDrive")
you_choice = int(input("Select 1 or 2"))
if you_choice == 1:
    while True:
        img = picam.get_image()
        # img = kinect.get_image()
        faces = face_detect(img)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), BORDER_WIDTH)
            cv2.imshow("image", img)
            # Save the captured image into the datasets folder
            print("face detected ..., waitting for save")

            save_image(
                image=img[
                    y + BORDER_WIDTH : y + h - BORDER_WIDTH,
                    x + BORDER_WIDTH : x + w - BORDER_WIDTH,
                ],
                name="face." + str(current_milli_time()) + ".jpg",
            )
        cv2.imshow("image", img)
        k = cv2.waitKey(1) & 0xFF  # Press 'ESC' for exiting video
        if k == 27:
            picam.detroy()
            cv2.destroyAllWindows()
            break
elif you_choice == 2:
    upload_dataset()

