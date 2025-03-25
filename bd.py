from flask import Flask,Blueprint,blueprints,jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector
import logging


app = Flask(__name__)
uri = 'mysql+pymysql://root:root@localhost:3306/HYCSYSTEM_DB'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/HYCSYSTEM_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

logging.basicConfig(level=logging.DEBUG)
db = SQLAlchemy(app)
try:
   logging.debug("Conectando con la base de datos")
   if db:
      logging.debug(f"Conectado con la base de datos")
      db.init_app(app)
      db.create_all()
except Exception as e:
   #logging.error(f"Error al conectar con la base de datos {e.with_traceback()}")
   db = None
