from flask import Flask, jsonify
from faker import Faker
from flask_cors import CORS  # Important pour autoriser les requêtes cross-origin

app = Flask(__name__)
CORS(app)  # Active le CORS pour autoriser les requêtes depuis le frontend
faker = Faker()

@app.route('/')
def generate_password():
    password = faker.password(length=12, special_chars=True, digits=True, upper_case=True, lower_case=True)
    return jsonify({'password': password})

if __name__ == '__main__':
    app.run(debug=True)
