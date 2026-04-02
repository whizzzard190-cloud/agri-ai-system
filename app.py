from flask import Flask, render_template, request, redirect, session
from utils.db_helper import create_tables, get_connection
from models.crop_model import predict_crop
from models.disease_model import predict_disease
from utils.recommendation import get_recommendations
from models.chatbot import get_bot_response
import os

app = Flask(__name__)
app.secret_key = "secret123"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return redirect("/login")


# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Users (username, email, password) VALUES (?, ?, ?)",
                       (username, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# LOGIN
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE username=? AND password=?",
                       (username, password))
        user = cursor.fetchone()

        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            return "Invalid Credentials"

    return render_template("login.html")


# DASHBOARD
@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    if request.method == "POST":
        user_id = session["user_id"]

        # Crop Inputs
        N = float(request.form["N"])
        P = float(request.form["P"])
        K = float(request.form["K"])
        ph = float(request.form["ph"])
        temperature = float(request.form["temperature"])
        humidity = float(request.form["humidity"])
        rainfall = float(request.form["rainfall"])

        input_data = [N, P, K, ph, temperature, humidity, rainfall]
        crop_prediction = predict_crop(input_data)
    

        # Image Upload
        file = request.files["image"]

        # VALIDATION
        if not file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            return "Only image files are allowed!"

        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        disease_prediction, confidence = predict_disease(filepath)

        # SAVE TO DATABASE
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO Predictions (user_id, crop_prediction, disease_prediction)
        VALUES (?, ?, ?)
        """, (user_id, crop_prediction, str(disease_prediction)))

        conn.commit()
        conn.close()
        recs = get_recommendations(crop_prediction, disease_prediction)
        return render_template("result.html",
                       crop=crop_prediction,
                       disease=disease_prediction,
                       confidence=confidence,
                       recs=recs)

    return render_template("dashboard.html")
@app.route("/chatbot", methods=["POST"])
def chatbot():
    user_msg = request.form["message"]
    response = get_bot_response(user_msg)
    return response
# LOGOUT
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
@app.route("/admin")
def admin():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Predictions")
    data = cursor.fetchall()

    conn.close()

    return render_template("admin.html", data=data)

if __name__ == "__main__":
    create_tables()
    app.run(debug=True, port=5000)