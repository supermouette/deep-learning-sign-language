"""
Simply display the contents of the webcam with optional mirroring using OpenCV
via the new Pythonic cv2 interface.  Press 'q' to quit and 's' to take a screenshoot (save as image_x in the current folder).
"""

import cv2
import numpy as np

def show_webcam(mirror=False):
    count = 0
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img = cv2.flip(img, 1)
        cv2.imshow('my webcam', img)
        if cv2.waitKey(25) & 0xFF == ord('s'):
            printscreen_pil = cam.grab()
            ret, image1 = cam.retrieve()
            cv2.imwrite("./image_" + str(count) + ".bmp", image1)
            count += 1
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break  # q to quit
    cv2.destroyAllWindows()

def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
