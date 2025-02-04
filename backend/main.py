from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
app = Flask(__name__)
app.config.from_object(DevConfig)
api = Api(app,doc='/docs')

@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {'message': 'hello world '}

if __name__ == '__main__':
    app.run(debug=True)
