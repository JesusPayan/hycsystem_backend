from flask import Blueprint, request, jsonify
import json
from services.Role import RoleService
#from utils import createFile
import io,os,tempfile,base64, csv, json
import logging
import pandas as pd
from models import Client
import datetime as date_time

message = ''
code = 200

client_bp = Blueprint('Client', __name__)

@client_bp.route('/client', methods=['POST'])
def add_client():
    if request:
        data = request.get_json()
        logging.info(f"Routes -> add_client data: {data}")
        code,message = RoleService.create_client(data)
    else:
        message = "No se ha enviado ningun dato"
        code = 404    
    return jsonify ({"message": f"{message}"}), code    

@client_bp.route('/clients', methods=['GET'])
def get_clients():
    code,message = Client.get_clients()
    logging.info(f"Routes -> get_clients message")
    return jsonify ({"message": f"{message}"}), code
@client_bp.route('/client/<string:client_name>', methods=['GET'])
def get_client(client_name):
    code,message = Client.get_client(client_name)
    logging.info(f"Routes -> get_client message")
    return jsonify ({"message": f"{message}"}), code