from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.utils import np_utils
from keras import backend as K
from keras.models import model_from_json

import numpy as np
"""
Je n'ai pas encore nettoyer le fichier :/"

"""



K.set_image_dim_ordering('th')
from loadData import load_data_from_file

from time import time

t0 = time()


seed = 7
np.random.seed(seed)
train_file = r"../dataset/sign-language-mnist/sign_mnist_train.csv"
test_file = r"../dataset/sign-language-mnist/sign_mnist_test.csv"
X_train, y_train = load_data_from_file(train_file)
X_test, y_test = load_data_from_file(test_file)


height = X_train[0].shape[0]
num_pixels = height**2
num_classes = 25

X_train = np.array(X_train)
X_test = np.array(X_test)
X_train = X_train.reshape(X_train.shape[0], 1, height, height).astype('float32')
X_test = X_test.reshape(X_test.shape[0], 1 ,height, height).astype('float32')

print(X_train.shape)


X_train = X_train.astype('float32')
X_test = X_test.astype('float32')
X_train = X_train / 255.0
X_test = X_test / 255.0

y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)

print(X_train.shape)


model = Sequential()

#------- network definition
"""
model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer= 'normal' , activation= 'relu' ))
model.add(Dense(num_classes, kernel_initializer= 'normal' , activation= 'softmax' ))
"""
#-------


model.add(Convolution2D(32, (5, 5), input_shape=(1,height, height), padding='same', activation='relu', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))
model.add(Convolution2D(32, (5, 5), input_shape=(1,height, height), padding='same', activation='relu', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))
model.add(Convolution2D(64, (5, 5), activation='relu', padding='same', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.3))
model.add(Convolution2D(128, (5, 5), activation='relu', padding='same', kernel_constraint=maxnorm(3)))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu', kernel_constraint=maxnorm(3)))
model.add(Dropout(0.4))
model.add(Dense(num_classes, activation='softmax'))

"""
model.add(Convolution2D(32, (5, 5), input_shape=(1, height, height), activation='relu'))
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Dropout(0.2))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(num_classes, activation='softmax'))
"""


epochs = 15
lrate = 0.015
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
model.summary()
#exit()
print("took "+str(time()-t0)+" seconds")

# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=epochs, batch_size=32, verbose=2)
# Final evaluation of the model
"""
pred = model.predict(X_test)
pred2 = model.predict(X_train)
s=0
s2=0
print(pred)
for i in range(pred.shape[0]):
    if pred[i,0]>0.5 :
        s+=1
    if pred2[i,0]>0.5 :
        s2+=1
print(s, s2)

scores = model.evaluate(X_test, y_test)
scores2 = model.evaluate(X_train,y_train)
#print("Accuracy: %.2f%%" % (scores[1]*100))



for i in range(len(scores)):
    print(model.metrics_names[i]+' : '+str(scores[i]))

for i in range(len(scores2)):
    print(model.metrics_names[i]+' : '+str(scores2[i]))

model.save("model2.h5")
"""
print("took "+str(time()-t0)+" seconds")