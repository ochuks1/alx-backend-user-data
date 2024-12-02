#!/usr/bin/env python3
"""
Flask app for user authentication service.
"""

from flask import Flask, jsonify, request, abort, make_response
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"])
def users():
    email = request.form.get("email")
    password = request.form.get("password")
    try:
        user = auth.register_user(email, password)
        return jsonify({"email": user.email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    if not auth.valid_login(email, password):
        abort(401)
    session_id = auth.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)
    return response


@app.route("/profile", methods=["GET"])
def profile():
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/sessions", methods=["DELETE"])
def logout():
    session_id = request.cookies.get("session_id")
    user = auth.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    auth.destroy_session(user.id)
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
