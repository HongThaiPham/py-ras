from mtcnn.mtcnn import MTCNN

detector = MTCNN()


def mymtcnn(img):
    faces = detector.detect_faces(img)
    if len(faces) <= 0:
        return None
    box = []

    for fuck in faces:
        if fuck["confidence"] > 0.7:
            box.append(fuck["box"])

    return box


def main():
    mymtcnn()


if __name__ == "__main__":
    main()
