import cv2

def preprocess_image(path):
    img = cv2.imread(path)
    img = cv2.resize(img, (128, 128))
    return img