from keras.models import load_model
from loadData_realData import load_real_data
from sklearn import metrics
import numpy as np
from keras.utils import np_utils

x, y = load_real_data("../image_test")

height = x[0].shape[0]
width = x[0].shape[1]
num_pixels = height**2
num_classes = 5

x = np.array(x)
x = x.reshape(x.shape[0], 1, height, width).astype('float32')
x = x.astype('float32')
x = x / 255.0
y = np_utils.to_categorical(y)


model = load_model('model.h5')
y_pred = model.predict(x)

matrix = metrics.confusion_matrix(y.argmax(axis=1), y.argmax(axis=1))
print(matrix)