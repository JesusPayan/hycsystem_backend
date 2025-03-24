from flask import Flask, jsonify
from bd_config import db
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Date, create_engine
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from contextlib import contextmanager
from sqlalchemy import engine, create_engine
import mysql.connector
import datetime

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    