from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_augmentor():
    return ImageDataGenerator(
        rotation_range=10,
        zoom_range=0.1,
        horizontal_flip=True
    )