import numpy as np 
import pandas as pd
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

train_dataset_path = 'robot1_positions.csv'
valid_dataset_path = 'robot1_positions.csv' #bad practise to use same file.

column_names = ['or_x','or_y','or_z','or_w','us1','us2','us3','us4','us5','us6',
                'gt_x','gt_y']

train_dataset = pd.read_csv(train_dataset_path, names=column_names)

train_label_x = train_dataset.pop('gt_x')
train_label_y = train_dataset.pop('gt_y')
train_labels = pd.concat([train_label_x, train_label_y], axis=1)

valid_dataset = pd.read_csv(valid_dataset_path, names=column_names)

valid_label_x = valid_dataset.pop('gt_x')
valid_label_y = valid_dataset.pop('gt_y')
valid_labels = pd.concat([valid_label_x, valid_label_y], axis=1)
print(train_dataset.keys())
print(len(train_dataset.keys()))

def build_model():
    model = keras.Sequential([
        layers.Dense(64, activation='relu', input_shape=[len(train_dataset.keys())]),
        layers.Dense(64, activation='relu'),
        layers.Dense(2)

    ])
    optimizer = tf.keras.optimizers.RMSprop(0.001)
    model.compile(loss='mse',
                    optimizer=optimizer,
                    metrics=['mae', 'mse'])
    return model

model = build_model()
print(model.summary())

EPOCHS = 10
history = model.fit(
    train_dataset, train_labels,
    epochs = EPOCHS, validation_split = 0.2, verbose=1)

model.save("saved_model")

