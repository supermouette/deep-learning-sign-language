def show_webcam(model):
    import cv2
    from skimage.transform import resize, rescale
    from time import sleep, time
    from skimage import io
    from skimage.filters import sobel
    from skimage.color import rgb2gray
    import numpy as np
    from os import makedirs
    cam = cv2.VideoCapture(0)

    path = "../datasets/webcam/"+str(time())
    makedirs(path)

    while True:
        # récupération image webcam
        ret_val, img_cam = cam.read()
        img_cam = cv2.flip(img_cam, 2)
        img = img_cam[:, :, :]

        # mise à la bonne dimension
        img = img[..., [2, 1, 0]]  # bgr -> rgb

        new_img = rescale(rgb2gray(img), 0.25)

        # sobel et masquage
        new_img = sobel(new_img)

        io.imsave(path+"/"+str(time())+".png", new_img)
        cv2.imshow("img", img_cam)
        cv2.imshow("sobel", rescale(new_img, 4))

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()


def main():
    #from keras.models import load_model
    #model = load_model('model.h5')
    show_webcam("")


if __name__ == "__main__":
    main()
