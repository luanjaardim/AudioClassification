import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import numpy as np
import tensorflow as tf
from utils import getEveryFile, getSpectrogramFromImage
layers = tf.keras.layers
models = tf.keras.models

# Train the model and save it to a file for posterior use
# @extractor_type: 'HOG' or 'LBP'
# @model_name: name of the model to be saved, need to be a '.keras' file
def train_and_save_model(extractor_type = 'HOG', model_name = 'spectrogram_model.keras'):
    typeDir = 'HOG/' if extractor_type == 'HOG' else 'LBP/'

    # Get the paths to the images
    train_files = getEveryFile(typeDir=typeDir)

    # Load the train data and labels
    train_data, train_label = zip(*[getSpectrogramFromImage(path) for path in train_files])
    train_data = np.array(train_data)
    train_label = np.array(train_label)

    # Every image has the same shape, 496x293 pixels
    input_shape = (293, 496)

    # Create a Sequential model
    model = models.Sequential([
        # Add a Flatten layer to flatten the input into a 1D tensor
        layers.InputLayer(shape=input_shape),
        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(32, activation='relu'),
        # Add a Dense layer with 5 units for output, as we have only 5 classes
        layers.Dense(5)
    ])

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])

    # Train the model
    model.fit(train_data, train_label, epochs=10, verbose=2, batch_size=64)
    model.save('models/' + extractor_type + '_' + model_name + '.keras')

    # Return information about the model
    model.summary()
    print('\n\nModel saved as ' + extractor_type + '_' + model_name + '.keras in the models/ directory')

