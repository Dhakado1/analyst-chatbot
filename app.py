
import os

from flask import Flask, render_template, request, jsonify, session
from dotenv import load_dotenv

# Load .env before importing modules that need environment variables
load_dotenv()

from database import init_db
from llm import process_user_query


app = Flask(__name__)

app.secret_key = os.getenv(
    "FLASK_SECRET_KEY",
    "super_secret_key"
)

init_db()
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message")

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        context = session.get("context", {})

        response, new_context, generated_sql = process_user_query(
            user_message,
            context
        )

        session["context"] = new_context

        return jsonify({
            "response": response,
            "sql": generated_sql
        })

    except Exception as e:
        import traceback

        print("\n========== CHAT ERROR ==========")
        traceback.print_exc()
        print("================================\n")

        return jsonify({
            "error": str(e)
        }), 500

@app.route("/clear", methods=["POST"])
def clear():
    session.pop("context", None)
    return jsonify({"status": "success"})

if __name__ == "__main__":
    app.run(debug=False, port=5000)