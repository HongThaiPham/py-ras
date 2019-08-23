import cv2
import os
import datetime

print('app running ...')
print('openning camera ...')

cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
face_detector = cv2.CascadeClassifier('/home/leo/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
# For each person, enter one numeric face id
#face_id = input('\n enter user id end press <return> ==>  ')

count = 0
while(True):
    ret, img = cam.read()
    #img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 1)
        count += 1
	#face_id = datetime.datetime.now()
        # Save the captured image into the datasets folder
        print('face deteted ..., waitting for save')
        cv2.imwrite("/home/leo/leo/py-ras/face/dataset/face." + str("t5l") + '.' + str(count) + ".jpg", img[y+1:y+h-1,x+1:x+w-1])
        print('save done')
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break
    elif count >= 30: # Take 30 face sample and stop video
         break

cam.release()
cv2.destroyAllWindows()
