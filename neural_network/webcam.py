def show_webcam(model):
    import cv2
    from skimage.transform import resize, rescale
    from time import sleep
    from skimage import io
    from skimage.filters import sobel
    from skimage.color import rgb2gray
    import numpy as np
    cam = cv2.VideoCapture(0)
    x = []
    i = 0
    emoji = "???"
    font = cv2.FONT_HERSHEY_COMPLEX
    bottomLeftCornerOfText = (30, 30)
    fontScale = 1
    fontColor = (255, 255, 255)
    lineType = 2
    while True:
        i += 1
        # récupération image webcam
        ret_val, img_cam = cam.read()
        img_cam = cv2.flip(img_cam, 2)
        img = img_cam[:, :, :]

        # mise à la bonne dimension
        img = img[..., [2, 1, 0]]  # bgr -> rgb
        img = rgb2gray(img)

        img = rescale(img, 0.25)
        # sobel et masquage
        img = sobel(img)

        img2 = io.imread(r"C:\Users\megam\Desktop\projets\deep-learning-sign-language\datasets\webcam\a_palm\1545929568.3351197.png", as_grey=True)
        x.append(img)
        # vectorisation
        #x = [img]
        if i == 10:
            i = 0

            height = x[0].shape[0]
            width = x[0].shape[1]
            x = np.array(x)
            x = x.reshape(x.shape[0], 1, height, width).astype('float32')
            x = x / 255.0

            # prédiction
            pred = model.predict(x)
            x = []
            print(pred)
            y = [np.argmax(pred[j]) for j in range(len(pred))]
            y.sort()
            print(y)
            y = y[5]
            # affichage
            #print(pred, y)
            #print(y)

            if y == 0:
                emoji = u'✋'
                emoji = "paume"
            elif y == 1:
                emoji = u'👊'
                emoji = "poing"
            elif y == 2:
                emoji = u'👍'
                emoji = "pouce"
            elif y == 3:
                emoji = u'☝️'
                emoji = "index"
            elif y == 4:
                emoji = u'👌'
                emoji = "ok"

        cv2.putText(img_cam, emoji, bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
        cv2.imshow("img", img_cam)
        cv2.imshow("sobel", rescale(img, 4))
        cv2.imshow("working image", rescale(img2, 4))
        #io.imshow(new_img)
        #io.show()
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.release()


def main():
    from keras.models import load_model
    model = load_model('model.h5')
    show_webcam(model)


if __name__ == "__main__":
    main()
