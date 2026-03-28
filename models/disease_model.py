import tensorflow as tf
from tensorflow.keras import layers, models
import os

MODEL_PATH = "models/disease_model.h5"


def create_model(input_shape=(128, 128, 3)):
    model = models.Sequential([
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),

        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.MaxPooling2D(2, 2),

        layers.Flatten(),
        layers.Dense(128, activation='relu'),
        layers.Dense(16, activation='softmax')  # adjust based on dataset
    ])

    model.compile(optimizer='adam',
                  loss='categorical_crossentropy',
                  metrics=['accuracy'])

    return model


def train_model():
    train_dir = "datasets/disease/"

    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        validation_split=0.2
    )

    train_data = datagen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=16,
        class_mode='categorical',
        subset='training'
    )

    val_data = datagen.flow_from_directory(
        train_dir,
        target_size=(128, 128),
        batch_size=16,
        class_mode='categorical',
        subset='validation'
    )

    model = create_model()

    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=5
    )

    model.save(MODEL_PATH)

    # SAVE METRICS
    import json
    with open("models/training_history.json", "w") as f:
        json.dump(history.history, f)


def predict_disease(image_path):
    model = tf.keras.models.load_model(MODEL_PATH)

    # LOAD CLASS NAMES
    import os
    class_names = sorted(os.listdir("datasets/disease"))

    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = tf.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    predicted_class = prediction.argmax()
    confidence = float(prediction.max()) * 100

    disease_name = class_names[predicted_class]

    return disease_name, round(confidence, 2)