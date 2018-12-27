def show_webcam(model):
    import cv2
    from skimage.transform import resize, rescale
    from time import sleep
    from skimage import io
    from skimage.filters import sobel
    from skimage.color import rgb2gray
    import numpy as np
    cam = cv2.VideoCapture(0)
    while True:
        # récupération image webcam
        ret_val, img_cam = cam.read()
        img = img_cam[:, :, :]

        # mise à la bonne dimension
        img = img[..., [2, 1, 0]]  # bgr -> rgb
        img = rgb2gray(img)[60:420, :]

        # print(img.shape)  # (360, 640) -> (60, 122)
        img = resize(img, (60, 107))
        # print(img.shape)
        new_img = np.zeros((60, 122))
        new_img[:, new_img.shape[1] // 2 - img.shape[1] // 2:new_img.shape[1] // 2 + img.shape[1] // 2 + 1] = img

        # sobel et masquage
        new_img = sobel(new_img)

        strip1 = new_img.shape[1] // 2 - img.shape[1] // 2
        new_img[:, strip1 - 1:strip1 + 1] = 0
        strip2 = new_img.shape[1] // 2 + img.shape[1] // 2
        new_img[:, strip2:strip2 + 2] = 0

        new_img[:, :new_img.shape[1] // 4] = 0
        new_img[:, 3*new_img.shape[1] // 4:] = 0

        # vectorisation
        x = [new_img]
        height = x[0].shape[0]
        width = x[0].shape[1]
        x = np.array(x)
        x = x.reshape(x.shape[0], 1, height, width).astype('float32')
        x = x.astype('float32')
        x = x / 255.0

        # prédiction
        pred = model.predict(x)
        y = np.argmax(pred[0])

        # affichage
        print(pred)
        #print(y)
        font = cv2.FONT_HERSHEY_COMPLEX
        bottomLeftCornerOfText = (30, 30)
        fontScale = 1
        fontColor = (255, 255, 255)
        lineType = 2

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
        cv2.imshow("sobel", rescale(new_img, 4))
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
