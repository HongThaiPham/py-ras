import cv2
import os
import datetime
from primesense import openni2
from primesense import _openni2 as c_api
import numpy as np
from face_detect import face_detect

# declare constant
DATASET_PATH = os.path.join(os.getcwd(), "face/dataset")
OPENNI_PATH = "E:\OpenNI_2.3.0.55\Windows\Astra OpenNI2 Development Instruction(x64)_V1.3\OpenNI2\OpenNI-Windows-x64-2.3.0.55"
OPENNI_DIST = os.path.join(OPENNI_PATH, "Redist")
RESOLUTIONX = 640
RESOLUTIONY = 480
FPS = 30


def init_cam():
    print("Initializing Kinect ...")
    openni2.initialize(OPENNI_DIST)
    dev = openni2.Device.open_any()
    stream = dev.create_color_stream()
    stream.set_video_mode(
        c_api.OniVideoMode(
            pixelFormat=c_api.OniPixelFormat.ONI_PIXEL_FORMAT_RGB888,
            resolutionX=RESOLUTIONX,
            resolutionY=RESOLUTIONY,
            fps=FPS,
        )
    )
    # stream.start()
    print("Cam running ...")
    return stream


def get_rgb(stream):
    """
    Returns numpy 3L ndarray to represent the rgb image.
    """
    bgr = np.frombuffer(
        stream.read_frame().get_buffer_as_uint8(), dtype=np.uint8
    ).reshape(RESOLUTIONY, RESOLUTIONX, 3)
    rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
    return rgb


def main():
    print("App running ...")
    rgb_stream = init_cam()
    rgb_stream.start()

    count = 0
    while True:
        img = get_rgb(rgb_stream)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detect(img)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
            count += 1
            # Save the captured image into the datasets folder
            print("face detected ..., waitting for save")
            cv2.imwrite(
                os.path.join(
                    DATASET_PATH, "face." + str("t5l") + "." + str(count) + ".jpg"
                ),
                img[y + 1 : y + h - 1, x + 1 : x + w - 1],
            )
            cv2.imshow("image", img)
            print("save done")
        cv2.imshow("image", img)

        # exit
        k = cv2.waitKey(1) & 0xFF  # Press 'ESC' for exiting video
        if k == 27:
            rgb_stream.close()
            break
    print("app stop ...")


if __name__ == "__main__":
    main()
