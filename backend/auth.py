from flask_restx import Resource, Namespace,fields
from flask import Flask, request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended  import (JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity)
from models import User
auth_ns = Namespace('auth',description="A Name Space for our authentication")
sing_model = auth_ns.model(
    'SignUp',
    {
        "username":fields.String(),
        "password":fields.String(),
        "email":fields.String()
    }
)
login_model = auth_ns.model(
    'Login',
    {
        "username":fields.String(),
        "password":fields.String()
    }
)
@auth_ns.route('/signup')
class SingUp(Resource):
    # @api.marshal_with(sing_model)
    @auth_ns.expect(sing_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        db_user = User.query.filter_by(username=username).first()
        if  db_user is not None:
            return jsonify({"message":f"user name alredy exits {username}"})
        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password')),  
        )
        print(new_user)
        new_user.save()
        return make_response(jsonify({
            "message":f"User {username} created successfully",
        }),201)

@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.username)
            refresh_token = create_refresh_token(identity=db_user.username)
            return jsonify({
                "access_token":access_token,
                "refresh_token":refresh_token
            })
@auth_ns.route('/refresh')
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_access_token = create_access_token(identity=current_user)
        return make_response(jsonify({
            "access_token":new_access_token
        }),200)