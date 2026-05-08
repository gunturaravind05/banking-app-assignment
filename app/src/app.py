from flask import Flask
import os

app = Flask(__name__)

@app.route("/")
def home():
    return {
        "application": "banking-app",
        "status": "running"
    }

@app.route("/health")
def health():
    return {
        "status": "healthy"
    }

@app.route("/db")
def db():
    return {
        "db_host": os.getenv("DB_HOST"),
        "db_name": os.getenv("DB_NAME")
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)