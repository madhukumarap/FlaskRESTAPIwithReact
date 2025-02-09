import unittest
from main import create_app
from config import TestConfig
from exts import db

class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)  
        self.client = self.app.test_client()

        with self.app.app_context():
            # db.init_app(self.app)
            db.create_all()
            # db.session.commit()

    def test_hello_word(self):
        response = self.client.get('/hello')
        json = response.json
        self.assertEqual(json, {"message": "hello world"})

    def test_signup(self):
        signup_response = self.client.post('/auth/signup', json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "test",
        })
        self.assertEqual(signup_response.status_code, 201)

    def test_login(self):
        self.client.post('/auth/signup', json={
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "test",
        })
        
        login_response = self.client.post('/auth/login', json={
            "username": "testuser",
            "password": "test",
        })
        self.assertEqual(login_response.status_code, 200)

    def test_all_recipe(self):
        get_all_recipe = self.client.get('/recipes/recipes')
        status_code = get_all_recipe.status_code
        json_data = get_all_recipe.json
        self.assertEqual(status_code, 200)
        self.assertIsInstance(json_data, list)

    def test_get_one_recipe(self):
        id = 5
        get_one_recipe = self.client.get(f'/recipes/recipes/{id}')
        status_code = get_one_recipe.status_code
        print(status_code)
        self.assertEqual(status_code, 404)

    def test_create_recipe(self):
        self.client.post("/auth/signup", json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "password",
        })

        login_response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "password"
        })
        access_token = login_response.json["access_token"]

        create_recipe_response = self.client.post(
            "/recipes/recipes",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        self.assertEqual(create_recipe_response.status_code, 201)

    def test_update_recipe(self):
        self.client.post("/auth/signup", json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "password",
        })

        login_response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "password"
        })
        access_token = login_response.json["access_token"]

        create_recipe_response = self.client.post(
            "/recipes/recipes",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        recipe_id = create_recipe_response.json["id"]  # Use dynamic ID

        update_response = self.client.put(
            f"/recipes/recipes/{recipe_id}",
            json={"title": "Updated Cookie", "description": "Updated description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )

        self.assertEqual(update_response.status_code, 200)

    def test_delete_recipe(self):
        self.client.post("/auth/signup", json={
            "username": "testuser",
            "email": "testuser@test.com",
            "password": "password",
        })

        login_response = self.client.post("/auth/login", json={
            "username": "testuser",
            "password": "password"
        })
        access_token = login_response.json["access_token"]

        create_recipe_response = self.client.post(
            "/recipes/recipes",
            json={"title": "Test Cookie", "description": "Test description"},
            headers={"Authorization": f"Bearer {access_token}"},
        )
        recipe_id = create_recipe_response.json["id"]  # Use dynamic ID

        delete_response = self.client.delete(
            f"/recipes/recipes/{recipe_id}",
            headers={"Authorization": f"Bearer {access_token}"},
        )

        self.assertEqual(delete_response.status_code, 200)

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.session.commit()

if __name__ == '__main__':
    unittest.main()
