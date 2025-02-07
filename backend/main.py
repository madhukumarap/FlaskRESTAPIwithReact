from flask import Flask, request, jsonify
from flask_restx import Api, Resource, fields
from config import DevConfig
from models import Recipe
from exts import db
from flask_migrate import Migrate
app = Flask(__name__)
app.config.from_object(DevConfig)
db.init_app(app)
migrate = Migrate(app,db)
api = Api(app, doc='/docs')

# Serializer
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
        return {'message': 'hello world'}

@api.route('/recipes')
class RecipeResource(Resource):
    @api.marshal_list_with(recipe_model)
    def get(self):
        recipes = Recipe.query.all()
        return [recipe.to_dict() for recipe in recipes], 200

    @api.marshal_with(recipe_model)
    def post(self):
        data = request.get_json()
        recipe = Recipe(title=data.get('title'), description=data.get('description'))
        recipe.save()
        return recipe.to_dict(), 201  # Fixed issue

@api.route('/recipes/<int:id>')
class SingleRecipeResource(Resource):  # Renamed class to avoid conflict
    @api.marshal_with(recipe_model)
    def get(self, id):
        recipe = Recipe.query.get_or_404(id)
        return recipe.to_dict(), 200
    @api.marshal_with(recipe_model)
    def delete(self, id):
        recipe = Recipe.query.get_or_404(id)
        recipe.delete()
        return {"message": "Recipe deleted"}, 200
    @api.marshal_with(recipe_model)
    def put(self, id):
        
        recipe = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe.update(data.get('title'), data.get('description'))
        return recipe.to_dict(), 200

# Shell context
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Recipe': Recipe}

if __name__ == '__main__':
    app.run(debug=True)
