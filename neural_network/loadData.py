def load_data_from_file(path, p=0.2):
    from os import listdir, sep
    from skimage import io
    from skimage.transform import resize

    x = []
    y = []
    to_categ = {1:0, 3:1, 5:2, 6:3, 7:4}
    for d in listdir(path):
        if int(d) < 5:
            new_path = path + sep + d
            print("reading " + new_path)
            for d2 in listdir(new_path):
                y_path = int(d2[:2])
                if y_path in [1, 3, 5, 6, 7]:
                    last_path = new_path + sep + d2

                    for d3 in listdir(last_path):
                        y.append(to_categ[y_path])
                        #x.append(rescale(io.imread(last_path + sep + d3, as_grey=True), 0.25))
                        x.append(resize(io.imread(last_path + sep + d3, as_grey=True), (224, 224)))

    X_test = x[:int(len(x) * p)]
    y_test = y[:int(len(y) * p)]
    X_train = x[int(len(x) * p):]
    y_train = y[int(len(y) * p):]

    histo = [0]*5
    for i in y_test:
        histo[i]+=1
    print(histo)

    return X_train, y_train, X_test, y_test


if __name__ == "__main__":
    from skimage import io
    from time import time
    t0 = time()
    path = r"..\datasets\leapGestRecog\leapGestRecog"

    X_train, y_train, X_test, y_test = load_data_from_file(path)

    print(time()-t0)
    print(len(X_train), len(X_test))
    io.imshow(X_train[0])
    io.show()
    print(y_test[0])
# [7, 6, 5, 3, 1]