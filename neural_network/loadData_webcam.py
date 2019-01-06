def load_data(path, test_dir):
    from os import listdir, sep
    from skimage import io
    import random

    X_test = []
    y_test = []
    X_train = []
    y_train = []

    for d in listdir(path):
        splited = d.split('_')
        new_path = path + sep + d
        if len(splited) == 2:
            for d2 in listdir(new_path):
                if splited[1] == 'palm':
                    y = 0
                elif splited[1] == 'index':
                    y = 3
                elif splited[1] == 'ok':
                    y = 4
                elif splited[1] == 'poing':
                    y = 1
                elif splited[1] == 'pouce':
                    y = 2
                img = io.imread(new_path+sep+d2, as_grey=True)
                if splited[0] in test_dir:
                    X_test.append(img)
                    y_test.append(y)
                else:
                    X_train.append(img)
                    y_train.append(y)

    c = list(zip(X_train, y_train))
    random.shuffle(c)
    X_train, y_train = zip(*c)

    c = list(zip(X_test, y_test))
    random.shuffle(c)
    X_test, y_test = zip(*c)


    histo = [0] * 5
    for i in y_test:
        histo[i] += 1
    print("test", histo)

    histo = [0] * 5
    for i in y_train:
        histo[i] += 1
    print("train", histo)

    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    from skimage import io
    from time import time
    t0 = time()
    io.use_plugin("imageio")

    path = "../datasets/webcam"
    X_train, y_train, X_test, y_test = load_data(path, 0.2)
    print(time()-t0)
    io.imshow(X_train[1])
    io.show()


