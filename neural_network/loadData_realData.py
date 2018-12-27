def load_real_data(path):
    from os import listdir, sep
    from skimage import io
    from skimage.transform import rescale
    from skimage.transform import resize
    from skimage.filters import sobel
    import numpy as np
    from skimage.filters import gaussian

    x = []
    y = []
    to_categ = {1: 0, 3: 1, 5: 2, 6: 3, 7: 4}
    for d in listdir(path):
        splited = d.split(' ')
        if len(splited) == 2:
            new_path = path + sep + d
            if splited[0] == 'Paume':
                y.append(0)
            elif splited[0] == 'doigt':
                y.append(3)
            elif splited[0] == 'Ok':
                y.append(4)
            elif splited[0] == 'poing':
                y.append(1)
            elif splited[0] == 'pouce':
                y.append(2)

            img = io.imread(new_path, as_grey=True)
            # 3456*4606
            # 122*60
            img = gaussian(img)
            img = resize(img, (60, int(60 * 0.75)))
            new_img = np.zeros((60, 122))
            new_img[:, new_img.shape[1] // 2 - img.shape[1] // 2:new_img.shape[1] // 2 + img.shape[1] // 2 + 1] = img
            new_img = sobel(new_img)
            strip1 = new_img.shape[1] // 2 - img.shape[1] // 2
            new_img[:, strip1 - 1:strip1 + 1] = 0
            strip2 = new_img.shape[1] // 2 + img.shape[1] // 2
            new_img[:, strip2:strip2 + 2] = 0
            x.append(new_img)
    return x,y


if __name__ == "__main__":
    from skimage import io
    from time import time
    t0 = time()
    io.use_plugin("imageio")

    path = "../image_test"
    x, y = load_real_data(path)
    print(len(x), len(y))
    print(time()-t0)
    io.imshow(x[1])
    io.show()


