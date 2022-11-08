from calendar import c
from email.mime import message
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import jwt
from website import models
import json
from bson import json_util
from json.decoder import JSONDecodeError


routes = Blueprint("routes", __name__)


@routes.route('/get')
@jwt_required()
def get():
    arr = models.employeeCol.find()
    page = json.loads(json_util.dumps(arr))
    return jsonify({
        "user": page
    }), 200


@routes.route("/post", methods=['POST'])
@jwt_required()
def post():
    args = request.json
    try:
        if (models.employeeCol.find_one({"Email": args['Email']}) != None):
            return jsonify({
                "message": 'email already exists',
            }), 400
        if(models.employeeCol.find_one({"Phone": args['Phone']}) != None):
            return jsonify({
                "message": 'Phone already exists',
            }), 400
        check_data = models.employeeCol.find_one({"Email": args['Email']})
        if check_data is None:
            dpresponse = models.employeeCol.insert_one(args)
            return jsonify({
                "status": "success",
                "message": "successfully added",
                "user": {
                    "Emp_id": args["Emp_id"],
                    "Name": args["Name"],
                    "Email": args["Email"],
                    "Phone": args["Phone"],
                    "DOB": args["Dob"],
                    "Salary": args["Salary"],
                    "Designation": args["Designation"]
                }
            })
    except JSONDecodeError as e:
        print(jsonify({"error": e}))
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        # print(jsonify({"error":e}))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(jsonify({"error": e}))
        return jsonify({"error": e}), 500


@routes.route("/update", methods=['PUT'])
@jwt_required()
def update():
    args = request.json
    try:
        if (models.employeeCol.find_one({"Email": args["Email"]})) == None:
            return jsonify({
                "message": 'Email doesnt exists',
            }), 404
        check_data = models.employeeCol.find_one({"Email": args['Email']})
        if check_data['Email'] == args['Email']:
            # print(args)
            dpresponse = models.employeeCol.update_one(
                {"Email": args['Email']}, {"$set": args})
            return jsonify({
                "status": "success",
                "message": "successfully updated",
                "user": args
            }), 200
    except JSONDecodeError as e:
        print(jsonify({"error": e}))
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        # print(jsonify({"error":e}))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(jsonify({"error": e}))
        return jsonify({"error": e}), 500


@routes.route("/delete", methods=['DELETE'])
@jwt_required()
def delete():
    args = request.json
    try:
        if (models.employeeCol.find_one({"Email": args["Email"]})) == None:
            return jsonify({
                "message": 'Email doesnt exists',
            }), 404
        check_data = models.employeeCol.find_one({"Email": args['Email']})
        if check_data['Email'] == args['Email']:
            # print(args)
            dpresponse = models.employeeCol.delete_one(
                {"Email": args['Email']})
            return jsonify({
                "status": "success",
                "message": "successfully deleted",
                "user": args
            }), 200
    except JSONDecodeError as e:
        print(jsonify({"error": e}))
        return jsonify({"error": str(e)}), 400
    except TypeError as e:
        # print(jsonify({"error":e}))
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(jsonify({"error": e}))
        return jsonify({"error": e}), 500


@routes.route("/token/refresh", methods=['POST'])
@jwt_required(refresh=True)
def refreshToken():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return jsonify({
        "access_token": access
    }), 200
