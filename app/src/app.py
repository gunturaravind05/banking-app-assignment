from flask import Flask, request, jsonify
import os
import pymysql
from decimal import Decimal

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME", "bankdb")


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True,
    )


def init_db():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                balance DECIMAL(10,2) DEFAULT 0.00,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                account_id INT NOT NULL,
                type VARCHAR(20) NOT NULL,
                amount DECIMAL(10,2) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (account_id) REFERENCES accounts(id)
            )
        """)
    conn.close()


@app.route("/")
def home():
    return jsonify({
        "application": "banking-app",
        "status": "running",
        "features": [
            "create account",
            "view accounts",
            "deposit",
            "withdraw",
            "transaction history"
        ]
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy"})


@app.route("/init-db", methods=["POST"])
def initialize_database():
    init_db()
    return jsonify({"message": "database initialized"})


@app.route("/accounts", methods=["POST"])
def create_account():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    initial_balance = data.get("balance", 0)

    if not name or not email:
        return jsonify({"error": "name and email are required"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "INSERT INTO accounts (name, email, balance) VALUES (%s, %s, %s)",
            (name, email, initial_balance),
        )
        account_id = cursor.lastrowid
    conn.close()

    return jsonify({
        "message": "account created",
        "account_id": account_id
    }), 201


@app.route("/accounts", methods=["GET"])
def list_accounts():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, name, email, balance, created_at FROM accounts")
        accounts = cursor.fetchall()
    conn.close()

    for account in accounts:
        account["balance"] = float(account["balance"])

    return jsonify(accounts)


@app.route("/accounts/<int:account_id>", methods=["GET"])
def get_account(account_id):
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT id, name, email, balance, created_at FROM accounts WHERE id = %s",
            (account_id,),
        )
        account = cursor.fetchone()
    conn.close()

    if not account:
        return jsonify({"error": "account not found"}), 404

    account["balance"] = float(account["balance"])
    return jsonify(account)


@app.route("/transactions/deposit", methods=["POST"])
def deposit():
    data = request.get_json()

    account_id = data.get("account_id")
    amount = Decimal(str(data.get("amount", 0)))

    if amount <= 0:
        return jsonify({"error": "amount must be greater than zero"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "UPDATE accounts SET balance = balance + %s WHERE id = %s",
            (amount, account_id),
        )

        if cursor.rowcount == 0:
            conn.close()
            return jsonify({"error": "account not found"}), 404

        cursor.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)",
            (account_id, "deposit", amount),
        )
    conn.close()

    return jsonify({"message": "deposit successful"})


@app.route("/transactions/withdraw", methods=["POST"])
def withdraw():
    data = request.get_json()

    account_id = data.get("account_id")
    amount = Decimal(str(data.get("amount", 0)))

    if amount <= 0:
        return jsonify({"error": "amount must be greater than zero"}), 400

    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute(
            "SELECT balance FROM accounts WHERE id = %s",
            (account_id,),
        )
        account = cursor.fetchone()

        if not account:
            conn.close()
            return jsonify({"error": "account not found"}), 404

        if account["balance"] < amount:
            conn.close()
            return jsonify({"error": "insufficient balance"}), 400

        cursor.execute(
            "UPDATE accounts SET balance = balance - %s WHERE id = %s",
            (amount, account_id),
        )

        cursor.execute(
            "INSERT INTO transactions (account_id, type, amount) VALUES (%s, %s, %s)",
            (account_id, "withdraw", amount),
        )
    conn.close()

    return jsonify({"message": "withdrawal successful"})


@app.route("/transactions", methods=["GET"])
def list_transactions():
    conn = get_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT id, account_id, type, amount, created_at
            FROM transactions
            ORDER BY created_at DESC
        """)
        transactions = cursor.fetchall()
    conn.close()

    for transaction in transactions:
        transaction["amount"] = float(transaction["amount"])

    return jsonify(transactions)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)