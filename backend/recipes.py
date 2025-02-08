from flask_restx import Resource, Namespace,fields
from flask import Flask, request, jsonify
from models import Recipe
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended  import JWTManager, create_access_token, create_refresh_token,jwt_required
recipe_ns = Namespace('recipes',description="A Name Space for Recipes")

recipe_model = recipe_ns.model(
    'Recipe',
    {
        'id': fields.Integer(),
        'title': fields.String(),
        'description': fields.String()
    }
)


@recipe_ns.route('/recipes')
class RecipeResource(Resource):
    @recipe_ns.marshal_list_with(recipe_model)
    def get(self):
        recipes = Recipe.query.all()
        return [recipe.to_dict() for recipe in recipes], 200

    @recipe_ns.marshal_with(recipe_model)
    @recipe_ns.expect(recipe_model)
    @jwt_required()
    def post(self):
        data = request.get_json()
        recipe = Recipe(title=data.get('title'), description=data.get('description'))
        recipe.save()
        return recipe.to_dict(), 201  # Fixed issue

@recipe_ns.route('/recipes/<int:id>')
class SingleRecipeResource(Resource):  # Renamed class to avoid conflict
    @recipe_ns.marshal_with(recipe_model)
    def get(self, id):
        recipe = Recipe.query.get_or_404(id)
        return recipe.to_dict(), 200
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def delete(self, id):
        recipe = Recipe.query.get_or_404(id)
        recipe.delete()
        return {"message": "Recipe deleted"}, 200
    @recipe_ns.marshal_with(recipe_model)
    @jwt_required()
    def put(self, id):
        
        recipe = Recipe.query.get_or_404(id)
        data = request.get_json()
        recipe.update(data.get('title'), data.get('description'))
        return recipe.to_dict(), 200
