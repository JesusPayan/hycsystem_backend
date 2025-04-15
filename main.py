from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from bd_config import db,app
from flask_cors import CORS
import os
import logging
from routes import Role, User

app.register_blueprint(Role.role_bp, url_prefix='/api')
app.register_blueprint(User.user_bp, url_prefix='/api')

logging.basicConfig(level=logging.DEBUG)

def home():
     return jsonify({"message": "Bienvenido a la API de Streaming"}),200
if __name__ == "__main__":
    # db.create_all()
    # app.app_context().push()
    app.run(debug=True)