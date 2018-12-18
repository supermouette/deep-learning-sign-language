def load_data_from_file(path):
    from os import listdir, sep
    from skimage import io
    from skimage.transform import rescale

    x = []
    y = []
    to_categ = {1:0, 3:1, 5:2, 6:3, 7:4}
    for d in listdir(path):
        if int(d) < 5:
            new_path = path + sep + d
            print("reading " + d)
            for d2 in listdir(new_path):
                y_path = int(d2[:2])
                if y_path in [1, 3, 5, 6, 7]:
                    last_path = new_path + sep + d2
                    for d3 in listdir(last_path):
                        y.append(to_categ[y_path])
                        x.append(rescale(io.imread(last_path + sep + d3, as_grey=True), 0.5))
    return x, y


if __name__ == "__main__":
    from skimage import io
    from time import time
    t0 = time()
    path = r"C:\Users\megam\Desktop\projets\deep-learning-sign-language\datasets\leapGestRecog\leapGestRecog"

    x, y = load_data_from_file(path)

    print(time()-t0)
    print(len(x), len(y))
    io.imshow(x[0])
    io.show()
    print(y[0])
# [7, 6, 5, 3, 1]