import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis, QuadraticDiscriminantAnalysis
import joblib

MODEL_PATH_LDA = "models/lda_model.pkl"
MODEL_PATH_QDA = "models/qda_model.pkl"


def train_model():
    data = pd.read_csv("datasets/crop/crop_data.csv")

    X = data[["N", "P", "K","temperature", "humidity","ph", "rainfall"]]
    y = data["label"]

    lda = LinearDiscriminantAnalysis()
    qda = QuadraticDiscriminantAnalysis()

    lda.fit(X, y)
    qda.fit(X, y)

    joblib.dump(lda, MODEL_PATH_LDA)
    joblib.dump(qda, MODEL_PATH_QDA)


def predict_crop(input_data):
    import joblib
    import numpy as np

    lda = joblib.load("models/lda_model.pkl")

    # Convert to numpy + reshape
    input_array = np.array(input_data).reshape(1, -1)

    prediction = lda.predict(input_array)

    return prediction[0]