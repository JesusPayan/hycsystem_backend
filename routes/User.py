from flask import Blueprint, request, jsonify
import json
from services.User import UserService
from utils import createFile
import io,os,tempfile,base64, csv, json
import logging
import pandas as pd
from models import User, Role
import datetime as date_time

user_bp = Blueprint('User', __name__)
message = ''
code = 200

@user_bp.route('/users', methods=['GET'])
def get_users():
    code,message = UserService.get_users()
    logging.info(f"Routes -> get_roles message")
    return jsonify ({"message": f"{message}"}), code
@user_bp.route('/users', methods=['POST'])
def add_users():
    if request.files:
        logging.info(f"Routes -> add_users request.files")
        file = request.files['file']
        new_users = []
        users_dataframe = pd.read_csv(io.StringIO(file.stream.read().decode("latin-1")))
        if users_dataframe.empty:
            message = "No se han encontrado usuarios en el archivo"
            code = 404
        else:
            create_timestamp = date_time.datetime.now()
            for index,row in users_dataframe.iterrows():
                missing_field = ''
                create_timestamp = date_time.datetime.now()
                if row.get('Nombre') != "": 
                 user_name = row.get('Nombre')
                else:
                 missing_field = 'Nombre'
                if row.get('Correo') != "":
                    email = row.get('Correo')
                else:
                    missing_field = 'Correo'
                if row.get('Rol') != "":
                    role = row.get('Rol')
                else:
                    missing_field = 'Rol'
                if missing_field != '':
                    message = f"El campo {missing_field} no se ha encontrado en el archivo"
                    code = 404
                    return jsonify ({"message": f"{message}"}), code
                
                obj_role = Role.query.filter_by(name=role).first()
                if obj_role.id:
                    obj_role_id = obj_role.id
                else:
                    obj_role_id = 3
                
                password = "ADMIN1234" if row.get('Rol') == 'Administrador' or row.get('Rol') == 'Gerente' else "USER1234"
                password = password.encode('utf-8')
                password = base64.b64encode(password).decode('utf-8')
                uuid = row.get('UUID')
                uuid = str(email.split("@")[0]).toupper()
                active = True
                new_user = User(
                    username=user_name,
                    email=email,
                    password=password,
                    uuid=uuid,
                    role_id=obj_role_id,
                    create_timestamp=create_timestamp,
                    active=active
                )
                new_users.append(new_user)
                logging.info(f"Routes -> add_users new_user: {new_user}")
                code,message = UserService.create_users(new_users)
    return jsonify ({"message": f"{message}"}), code