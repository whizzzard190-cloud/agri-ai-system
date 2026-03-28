import sqlite3

DB_NAME = "database.db"

def get_connection():
    return sqlite3.connect(DB_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    # Users Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        email TEXT,
        password TEXT
    )
    """)

    # Crop Data Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CropData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nitrogen REAL,
        phosphorus REAL,
        potassium REAL,
        ph REAL,
        temperature REAL,
        humidity REAL,
        rainfall REAL,
        crop_label TEXT
    )
    """)

    # Disease Data Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS DiseaseData (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_path TEXT,
        disease_label TEXT
    )
    """)

    # Predictions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        crop_prediction TEXT,
        disease_prediction TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Model Metrics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ModelMetrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model_name TEXT,
        accuracy REAL,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Chatbot Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ChatbotLogs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        message TEXT,
        response TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("All tables created successfully.")