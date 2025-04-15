from models import User
import datetime as date_time

import logging
from flask import Blueprint, request, jsonify
import json
import io,os,tempfile,base64, csv, json

def create_user(data_user):
    if data_user:
        try:
            User.save_user(data_user)
            return 201,"Usuario creado con exito"
        except Exception as e:
            return 500,f"Error al crear el usuario {e}"
        
def get_users():
    try:
        users = User.all_users()
        return 200,users
    except Exception as e:
        return 500,f"Error al obtener los usuarios {e}"

def create_users(data_users):
    if data_users:
        try:
            User.save_users(data_users)
            return 201,"Usuarios creados con exito"
        except Exception as e:
            return 500,f"Error al crear los usuarios {e}"