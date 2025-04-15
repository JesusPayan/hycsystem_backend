from flask import Blueprint, request, jsonify
import json
from services.Role import RoleService
from utils import createFile
import io,os,tempfile,base64, csv, json
import logging
import pandas as pd
from models import Role
import datetime as date_time

role_bp = Blueprint('Role', __name__)
message = ''
code = 200
@role_bp.route('/roles', methods=['GET'])
def get_roles():
    code,message = RoleService.get_roles()
    logging.info(f"Routes -> get_roles message")
    return jsonify ({"message": f"{message}"}), code
@role_bp.route('/role', methods=['POST'])
def add_role():
    if request:
        data = request.get_json()
        logging.info(f"Routes -> add_role data: {data}")
        code,message = RoleService.create_role(data)
    else:
        message = "No se ha enviado ningun dato"
        code = 404
    logging.info(f"Entrando a la ruta para agregar un role {data}")
    return jsonify ({"message": f"{message}"}), code
@role_bp.route('/roles', methods=['POST'])
def add_roles():
    if request.files:
        new_role = ''
        new_roles = []
        file = request.files['file']
        roles_dataframe = pd.read_csv(io.StringIO(file.stream.read().decode("utf-8")))
        
        logging.info(f"Routes -> add_roles")
        if roles_dataframe.empty:
            message = "No se han encontrado roles en el archivo"
            code = 404
        else:
            create_timestamp = date_time.datetime.now()

            for index,row in roles_dataframe.iterrows():

                name = row.get('Descripcion')
                buy = '"'"True"'"' if 1  else '"False"'
                repair = '"True"' if 1  else '"False"'
                sale = '"True"' if 1  else '"False"'
                reports = '"True"' if 1  else '"False"'
                users = '"True"' if 1  else '"False"'
                clients = '"True"' if 1  else '"False"'
                products = '"True"' if 1  else '"False"'
                devices = '"True"' if 1  else '"False"'
                inventory = '"True"' if 1  else '"False"'
                
                permission = '{"compras":'+str(buy)+',"reparaciones":'+str(repair)+',"ventas":'+str(sale)+',"reportes":'+str(reports)+',"usuarios":'+str(users)+',"clientes":'+str(clients)+',"productos":'+str(products)+',"dispositivos":'+str(devices)+',"inventario":'+str(inventory)+'}'""
                
                print(permission)
                logging.info(f"Routes -> add_roles permission: {permission}")
                new_role = Role(
                    name=name,
                    permissions=permission,
                    create_timestamp=str(date_time.datetime.now()),
                    active=True
                )
                #return jsonify ({"message": f"{permission}"}), code
                #new_role = Role(name=name,buy=buy,repair=repair,sale=sale,reports=reports,users=users,clients=clients,products=products,devices=devices,inventory=inventory,create_timestamp=create_timestamp.now())
                new_roles.append(new_role)

        code,message = RoleService.create_roles(new_roles)   
        return message, code