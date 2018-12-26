def preprocess(img):
    from skimage.filters import sobel
    from skimage.transform import rescale
    img = img[:,150:650]
    img = rescale(img, 1/4)
    img = sobel(img)
    return img


if __name__ == "__main__":
    from skimage import io
    from time import time
    from os import listdir, sep, makedirs
    from os.path import isdir
    t0 = time()
    path = r"..\datasets\leapGestRecog\leapGestRecog"
    path2 = r"..\datasets\leapGestRecog\preprocessed"
    for d in listdir(path):
        if int(d):
            new_path = path + sep + d
            print("reading " + new_path)
            for d2 in listdir(new_path):
                y_path = int(d2[:2])
                if y_path in [1, 3, 5, 6, 7]:
                    last_path = new_path + sep + d2
                    if not isdir(path2+sep+d+sep+d2):
                        makedirs(path2+sep+d+sep+d2)
                    for d3 in listdir(last_path):
                        io.imsave(path2+sep+d+sep+d2+sep+d3, preprocess(io.imread(last_path + sep + d3, as_grey=True)))
    print(time()-t0)