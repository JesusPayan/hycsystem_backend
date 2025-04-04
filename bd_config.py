from flask import Flask,Blueprint,blueprints,jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import logging



app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/hycsystem_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# db = SQLAlchemy(app)
db = SQLAlchemy()
if db:
#    print("Conectado con la base de datos")
   logging.info("Conectado con la base de datos")
   db.init_app(app)
   with app.app_context():
        db.create_all()
        # app.app_context().push()
        # app.run(debug=True)
else:
   print("Error al conectar con la base de datos")
