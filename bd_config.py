from flask import Flask,Blueprint,blueprints,jsonify
from flask_sqlalchemy import SQLAlchemy
import mysql.connector



app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3306/HYCSYSTEM_DB'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

print("Iniciando el sistema para la gestion de cuentas de Streaming")
db = SQLAlchemy(app)
if db:
   print("Conectado con la base de datos")
   db.init_app(app)
else:
   print("Error al conectar con la base de datos")