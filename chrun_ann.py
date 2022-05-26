# -*- coding: utf-8 -*-
"""chrun_ANN.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Muvh2CKuNoEVZvONwsbBh-kCmCWRw_AR
"""

# !pip install tensorflow-gpu

import tensorflow as tf

print(tf.__version__)

# Importing the libraries

import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LeakyReLU, PReLU, ELU, ReLU
from tensorflow.keras.layers import Dropout
import tensorflow as tf

# Importing the dataset
dataset = pd.read_csv('Churn_Modelling.csv')  # Loading dataset
X = dataset.iloc[:, 3:13]  # Removing RowNumber, CustomerId, Surname
y = dataset.iloc[:, 13]  # Taking only target variable

dataset.head()

# Printing Independent Feature
print(X)

# Printing the Output feature
print(y)

"""### Feature Engineering"""

# Create dummy variables
geography = pd.get_dummies(X["Geography"],
                           drop_first=True)  # get_dummies will put values in Geography in encoded values like: when
# france is present then france is 1 and [germany, spain] = 0 likewise.
gender = pd.get_dummies(X['Gender'], drop_first=True)

# Concatenate the Data Frames

X = pd.concat([X, geography, gender], axis=1)

# Drop Unnecessary columns, we already added encoded geography,gender in the dataset.
X = X.drop(['Geography', 'Gender'], axis=1)

# Splitting the dataset into the Training set and Test set


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

# Feature Scaling


sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

print(X_train)
print(X_train.shape)

# Part 2 - Now let's make the ANN!


# Initialising the ANN
classifier = Sequential()

# Adding the input layer
classifier.add(Dense(units=11, activation='relu'))

# Adding the first hidden layer
classifier.add(Dense(units=7, activation='relu'))

# Adding the second hidden layer
classifier.add(Dense(units=6, activation='relu'))

# Adding the output layer
classifier.add(Dense(units=1, activation='sigmoid'))

# import tensorflow
# opt = tensorflow.keras.optimizers.Adam(learning_rate=0.01)

# classifier.compile(optimizer=opt,loss='binary_crossentropy',metrics=['accuracy']) 
classifier.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Early stopping


early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    min_delta=0.0001,
    patience=20,
    verbose=1,
    mode="auto",
    baseline=None,
    restore_best_weights=False,
)

model_history = classifier.fit(X_train, y_train, validation_split=0.33, batch_size=10, epochs=1000,
                               callbacks=early_stopping)

# list all data in history

print(model_history.history.keys())

# summarize history for accuracy
plt.plot(model_history.history['accuracy'])
plt.plot(model_history.history['val_accuracy'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# summarize history for loss
plt.plot(model_history.history['loss'])
plt.plot(model_history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

# Part 3 - Making the predictions and evaluating the model

# Predicting the Test set results
y_pred = classifier.predict(X_test)
y_pred = (y_pred >= 0.5)

# Making the Confusion Matrix

cm = confusion_matrix(y_test, y_pred)
print(cm)

# Calculate the Accuracy
from sklearn.metrics import accuracy_score

score = accuracy_score(y_pred, y_test)

print(score)

# Get weights
print(classifier.get_weights())
