import cv2


def takePhoto(objectName):
    box_name = "img/" + objectName
    video_path = "http://192.168.11.22:8080/video"
    capture = cv2.VideoCapture(video_path)
    img_counter = 1

    while True:
        ret, frame = capture.read()

        if not ret:
            message = "Fail to take frame"
            break

        cv2.imshow('frame', frame)
        k = cv2.waitKey(1)

        if k & 0xFF == ord('q'):
            break
        
        if  k%256 == 32:
            img_name = "{}_{}.png".format(box_name, img_counter)
            cv2.imwrite(img_name, frame)
            print("Screenshot taken")
            img_counter += 1

    capture.release()
    cv2.destroyAllWindows()

    return img_name
