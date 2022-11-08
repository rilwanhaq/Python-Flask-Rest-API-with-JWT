from array import array
from flask import Blueprint, request, jsonify
from flask_restful import Resource, reqparse, abort
import json
import bcrypt
import validators
from website import models
from bson import json_util
from json.decoder import JSONDecodeError
from flask_jwt_extended import create_access_token, create_refresh_token
from datetime import datetime, timedelta, timezone

# setting expiration time for JWT token
# dt = datetime.now(timezone.utc) + timedelta(days=1, hours=0, minutes=1, seconds=0)
# print(dt)
expires = timedelta(days=1, hours=0, minutes=1, seconds=0)
# print(expires)

auth = Blueprint("auth", __name__)
# input_from_client = reqparse.RequestParser()
# input_from_client.add_argument("name", type=str, default=None, help="Name of the user")

# @auth.route('/')
# def hometes():
#     return "testing"


@auth.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', '')
    password = request.json.get('password', '')
    try:
        array = models.adminCol.find_one({'email': email})
        if array is None:
            return jsonify({'error': 'Invalid email address'}), 401
        # converting array to json serialization format
        page = json.loads(json_util.dumps(array))
        # print(page['_id'])
        # print(page['password'])
        # password = bcrypt.hashpw(password.encode(),bcrypt.gensalt(10))
        # print(password)
        if (bcrypt.checkpw(password.encode(), array['password'])):
            refresh_token = create_refresh_token(
                identity=page['_id'], expires_delta=expires)
            access_token = create_access_token(identity=page['_id'])

            return jsonify({
                "user": {
                    "email": email,
                    "message": "login successful"
                },
                "access_token": access_token,
                "refresh_token": refresh_token
            }), 200
        return jsonify({
            "error": "Invalid email address or password"
        }), 401
    except JSONDecodeError as e:
        print(jsonify({"error": e}))
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        # print(jsonify({"error":e}))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(jsonify({"error": e}))
        return jsonify({"error": e}), 500


@auth.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    name = request.json['name']
    password = request.json['password']
    args = request.json
    # print(args)
    if len(password) < 6:
        return jsonify({'error': 'password must be at least 8 characters long'}), 400

    if len(name) < 3:
        return jsonify({'error': 'username must be at least 3 characters long'}), 400

    if email == "":
        return jsonify({'error': 'Enter email address'}), 400

    if not validators.email(email):
        return jsonify({'error': 'Invalid email address'}), 400

    if not name.isalnum():
        return jsonify({'error': 'username should be alphabetic'}), 400
    try:
        array = models.adminCol.find_one({'email': email})
        if array is not None:
            return jsonify({'error': 'email already exists'}), 400
        if array == None:
            password = bcrypt.hashpw(password.encode(), bcrypt.gensalt(10))
            # print(password)
            args['password'] = password
            print(args['password'])
            print(args)
            # insert_data = json.loads(json_util.dumps(args))
            # dbresponse = models.adminCol.insert_one(insert_data)
            dbresponse = models.adminCol.insert_one(args)
            return jsonify(
                {
                    "status": "200",
                    "message": "Successfully created",
                    "user": {
                        "username": name,
                        "email": email
                    }
                }), 200

        # page = json.loads(json_util.dumps(array))
        # print(page)
        # return jsonify(page),200
    except JSONDecodeError as e:
        print(jsonify({"error": e}))
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        # print(jsonify({"error":e}))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(jsonify({"error": e}))
        return jsonify({"error": e}), 500
