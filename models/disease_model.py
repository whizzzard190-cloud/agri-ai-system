import tensorflow as tf
from tensorflow.keras import layers, models
import os

MODEL_PATH = "models/disease_model.h5"


def create_model(input_shape=(128, 128, 3)):
    model = models.Sequential([

        # BLOCK 1
        layers.Conv2D(32, (3, 3), activation='relu', input_shape=input_shape),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        # BLOCK 2
        layers.Conv2D(64, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        # BLOCK 3
        layers.Conv2D(128, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        # BLOCK 4 (NEW – improves accuracy)
        layers.Conv2D(256, (3, 3), activation='relu'),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        layers.Flatten(),

        # DENSE LAYERS
        layers.Dense(256, activation='relu'),
        layers.Dropout(0.5),  # prevents overfitting

        layers.Dense(22, activation='softmax')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0005),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model


def train_model():
    train_dir = "datasets/disease/"

    # AUGMENTATION (BIG ACCURACY BOOST)
    datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rescale=1./255,
        rotation_range=20,
        zoom_range=0.2,
        shear_range=0.2,
        horizontal_flip=True,
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

    # CALLBACKS (SMART TRAINING)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(patience=3, restore_best_weights=True),
        tf.keras.callbacks.ReduceLROnPlateau(patience=2)
    ]

    history = model.fit(
        train_data,
        validation_data=val_data,
        epochs=10,
        callbacks=callbacks
    )

    model.save(MODEL_PATH)

    # SAVE METRICS
    import json
    with open("models/training_history.json", "w") as f:
        history_dict = {k: [float(x) for x in v] for k, v in history.history.items()}
        json.dump(history_dict, f)


def predict_disease(image_path):
    model = tf.keras.models.load_model(MODEL_PATH)

    class_names = sorted(os.listdir("datasets/disease"))

    img = tf.keras.preprocessing.image.load_img(image_path, target_size=(128, 128))
    img_array = tf.keras.preprocessing.image.img_to_array(img) / 255.0
    img_array = tf.expand_dims(img_array, axis=0)

    prediction = model.predict(img_array)

    predicted_class = prediction.argmax()
    confidence = float(prediction.max()) * 100

    disease_name = class_names[predicted_class]

    return disease_name, round(confidence, 2)