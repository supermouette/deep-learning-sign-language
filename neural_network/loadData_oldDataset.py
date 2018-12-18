def load_data_from_file(path):
    import numpy as np
    x = []
    y = []
    with open(path, 'r') as f:
        for line in f:
            line = line.strip('\n')
            if not line.startswith("label"):
                px = line.split(',')
                y.append(int(px[0]))
                x.append([int(i) for i in px[1:]])
                x[-1] = np.reshape(x[-1], [int((len(px)-1)**0.5)]*2)
    return x, y


if __name__ == "__main__":
    from skimage import io
    from time import time
    t0 = time()
    train_file = r"C:\Users\megam\Desktop\Nouveau dossier\dataset\sign-language-mnist\sign_mnist_train.csv"
    test_file = r"C:\Users\megam\Desktop\Nouveau dossier\dataset\sign-language-mnist\sign_mnist_test.csv"
    train_x, train_y = load_data_from_file(train_file)
    test_x, test_y = load_data_from_file(test_file)
    print(time()-t0)
    io.imshow(train_x[0])
    io.show()
    io.imshow(test_x[0])
    io.show()
