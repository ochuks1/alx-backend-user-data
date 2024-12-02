#!/usr/bin/env python3
""" Main 2: Test the BasicAuth class """

from api.v1.auth.basic_auth import BasicAuth

basic_auth = BasicAuth()

# Test extract_base64_authorization_header
print(basic_auth.extract_base64_authorization_header(None))  # None
print(basic_auth.extract_base64_authorization_header(89))  # None
print(basic_auth.extract_base64_authorization_header("Holberton School"))  # None
print(basic_auth.extract_base64_authorization_header("Basic Holberton"))  # Holberton
print(basic_auth.extract_base64_authorization_header("Basic SG9sYmVydG9u"))  # SG9sYmVydG9u

# Test decode_base64_authorization_header
print(basic_auth.decode_base64_authorization_header(None))  # None
print(basic_auth.decode_base64_authorization_header("SG9sYmVydG9u"))  # Holberton

# Test extract_user_credentials
print(basic_auth.extract_user_credentials("user:password"))  # ('user', 'password')
print(basic_auth.extract_user_credentials("user-password"))  # (None, None)

# Test user_object_from_credentials
print(basic_auth.user_object_from_credentials("email", "password"))  # None or User object
