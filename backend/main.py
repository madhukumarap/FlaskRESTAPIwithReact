from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from exts import db
app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
api = Api(app,doc='/docs')
#serializer
recipe_model = api.model(
    'Recipe',
    {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String()
    }
)
@api.route('/hello')
class HelloResource(Resource):
    def get(self):
        return {'message': 'hello world '}

@api.route('/recipes')
class RecipeResource(Resource):
    def get(self):
        receipes = Recipe.query.all()
        return jsonify(receipes)
    def post(self):
        data = request.json
        recipe = Recipe(title=data['title'], description=data['description'])
        recipe.save()
        return jsonify(recipe)
@api.route('/recipes/<int:id>')
@app.shell_context_processor
class RecipeResource(Resource):
    def get(self,id):
        pass
    def delete(self,id):
        pass
    def put(self,id):
        pass
    
def make_shell_context():
    return {'db': db, 'Recipe': Recipe} # we dict
if __name__ == '__main__':
    app.run(debug=True)
