#!/usr/bin/env python3
""" Main 1: Test the Auth class """

from api.v1.auth.auth import Auth

a = Auth()

# Test require_auth method
print(a.require_auth(None, None))  # True
print(a.require_auth(None, []))  # True
print(a.require_auth("/api/v1/status/", []))  # True
print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))  # False
print(a.require_auth("/api/v1/status", ["/api/v1/status/"]))  # False
print(a.require_auth("/api/v1/users", ["/api/v1/status/"]))  # True
print(a.require_auth("/api/v1/users", ["/api/v1/status/", "/api/v1/stats"]))  # True
print(a.require_auth("/api/v1/stats", ["/api/v1/status/", "/api/v1/stats"]))  # False
print(a.require_auth("/api/v1/status/user", ["/api/v1/status/*"]))  # False

# Test authorization_header method
from flask import Flask, request
app = Flask(__name__)

@app.route('/')
def index():
    return str(a.authorization_header(request))

if __name__ == "__main__":
    app.run(debug=True)
