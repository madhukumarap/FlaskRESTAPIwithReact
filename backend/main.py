from flask import Flask, jsonify
from flask_restx import Api
from config import DevConfig
from models import Recipe
from exts import db
from flask_migrate import Migrate
from flask_jwt_extended  import JWTManager
from recipes import recipe_ns
from auth import auth_ns
from flask_cors import CORS
def create_app(DevConfig):

    app = Flask(__name__)
    app.config.from_object(DevConfig)
    CORS(app)
    db.init_app(app)
    migrate = Migrate(app,db)
    JWTManager(app)
    api = Api(app, doc='/docs')
    api.add_namespace(recipe_ns)
    api.add_namespace(auth_ns)
    @app.route('/hello', methods=['GET'])
    def hello():
        return jsonify({"message": "hello world"}), 200  # Ensure response is JSON

    # Shell context
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'Recipe': Recipe}
    return app
