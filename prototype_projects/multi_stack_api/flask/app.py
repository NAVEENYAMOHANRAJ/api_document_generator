from flask import Flask, Blueprint

app = Flask(__name__)
users = Blueprint("users", __name__)


@app.route("/health")
def health():
    return {"status": "ok"}


@users.route("/flask-users", methods=["GET", "POST"])
def users_collection():
    return {}


@users.get("/flask-users/<user_id>")
def user_detail(user_id):
    return {"id": user_id}
