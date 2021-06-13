
from flask import request, jsonify
from flask_bcrypt import check_password_hash
from flask_jwt_extended import create_access_token
from flask_restful import Resource

from app import bcrypt, db


# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
class Login(Resource):
    def post(self):
        if request.is_json:
            email = request.json["email"]
            password = request.json["password"]
        else:
            email = request.form["username"]
            password = request.form["password"]

        test = db.users.find_one({"email": email})
        if test:
            if check_password_hash(test["password"], password):
                access_token = create_access_token(identity=email)
                return jsonify(
                        message="Login Succeeded!",
                        access_token=access_token,
                    status=201)

        return jsonify(message="Bad Email or Password", status= 401)



# Create a route to authenticate your users and return JWTs. The
# create_access_token() function is used to actually generate the JWT.
class Register(Resource):
    def post(self):
        if request.is_json:
            email = request.json["email"]
            password = request.json["password"]
        else:
            email = request.form["username"]
            password = request.form["password"]
        test = db.users.find_one({"email": email})

        if test:
            return jsonify(message="User Already Exist" , status =409)
        else:
            user_info = dict(
                email=email,
                password=bcrypt.generate_password_hash(password),
            )
            # print(user_info)
            db.users.insert_one(user_info)
            return jsonify(message="User added successfully", status=201)


