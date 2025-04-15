# 📌 Modelo de Datos Relacional
# 📂 Tabla: Usuarios
# Guarda la información de los usuarios del sistema (técnicos, recepcionistas, administradores, vendedores).

# sql
# Copiar
# Editar
# CREATE TABLE Usuarios (
#     id_usuario INT PRIMARY KEY AUTO_INCREMENT,
#     nombre VARCHAR(100) NOT NULL,
#     correo VARCHAR(100) UNIQUE NOT NULL,
#     telefono VARCHAR(15) UNIQUE NOT NULL,
#     contraseña VARCHAR(255) NOT NULL,
#     rol ENUM('Administrador', 'Técnico', 'Recepcionista', 'Vendedor') NOT NULL,
#     estado ENUM('Activo', 'Inactivo') DEFAULT 'Activo',
#     fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# 📂 Tabla: Clientes
# Guarda la información de los clientes del taller.

# sql
# Copiar
# Editar
# CREATE TABLE Clientes (
#     id_cliente INT PRIMARY KEY AUTO_INCREMENT,
#     nombre VARCHAR(100) NOT NULL,
#     telefono VARCHAR(15) UNIQUE NOT NULL,
#     correo VARCHAR(100) UNIQUE NULL,
#     direccion TEXT NULL,
#     fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
# );
# 📂 Tabla: Equipos
# Registra los equipos ingresados para reparación.

# sql
# Copiar
# Editar
# CREATE TABLE Equipos (
#     id_equipo INT PRIMARY KEY AUTO_INCREMENT,
#     id_cliente INT NOT NULL,
#     tipo ENUM('Celular', 'Computadora', 'Cámara', 'Otro') NOT NULL,
#     marca VARCHAR(50) NOT NULL,
#     modelo VARCHAR(50) NOT NULL,
#     numero_serie VARCHAR(100) UNIQUE NULL,
#     descripcion_problema TEXT NOT NULL,
#     FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
# );
# 📂 Tabla: OrdenesServicio
# Gestiona las órdenes de reparación y su estado.

# sql
# Copiar
# Editar
# CREATE TABLE OrdenesServicio (
#     id_orden INT PRIMARY KEY AUTO_INCREMENT,
#     id_equipo INT NOT NULL,
#     id_cliente INT NOT NULL,
#     id_tecnico INT NOT NULL,
#     estado ENUM('Recibido', 'Diagnóstico', 'Reparación en proceso', 'Listo para entrega', 'Entregado') DEFAULT 'Recibido',
#     fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     fecha_entrega_estimada TIMESTAMP NULL,
#     fecha_entrega_real TIMESTAMP NULL,
#     costo_total DECIMAL(10,2) DEFAULT 0.00,
#     FOREIGN KEY (id_equipo) REFERENCES Equipos(id_equipo),
#     FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
#     FOREIGN KEY (id_tecnico) REFERENCES Usuarios(id_usuario)
# );
# 📂 Tabla: DetalleOrdenes
# Registra los costos de insumos y el tiempo estimado de reparación.

# sql
# Copiar
# Editar
# CREATE TABLE DetalleOrdenes (
#     id_detalle INT PRIMARY KEY AUTO_INCREMENT,
#     id_orden INT NOT NULL,
#     descripcion TEXT NOT NULL,
#     costo DECIMAL(10,2) NOT NULL,
#     tiempo_estimado INT NOT NULL COMMENT 'Tiempo en minutos',
#     FOREIGN KEY (id_orden) REFERENCES OrdenesServicio(id_orden)
# );
# 📂 Tabla: Inventario
# Controla los insumos y accesorios disponibles.

# sql
# Copiar
# Editar
# CREATE TABLE Inventario (
#     id_producto INT PRIMARY KEY AUTO_INCREMENT,
#     nombre VARCHAR(100) NOT NULL,
#     descripcion TEXT NULL,
#     cantidad INT NOT NULL DEFAULT 0,
#     precio_compra DECIMAL(10,2) NOT NULL,
#     precio_venta DECIMAL(10,2) NOT NULL,
#     categoria ENUM('Insumo', 'Accesorio') NOT NULL,
#     proveedor VARCHAR(100) NULL
# );
# 📂 Tabla: Ventas
# Registra las ventas de accesorios y otros productos.

# sql
# Copiar
# Editar
# CREATE TABLE Ventas (
#     id_venta INT PRIMARY KEY AUTO_INCREMENT,
#     id_cliente INT NOT NULL,
#     id_vendedor INT NOT NULL,
#     fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     total DECIMAL(10,2) NOT NULL,
#     FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente),
#     FOREIGN KEY (id_vendedor) REFERENCES Usuarios(id_usuario)
# );
# 📂 Tabla: DetalleVentas
# Registra los productos vendidos en cada venta.

# sql
# Copiar
# Editar
# CREATE TABLE DetalleVentas (
#     id_detalle INT PRIMARY KEY AUTO_INCREMENT,
#     id_venta INT NOT NULL,
#     id_producto INT NOT NULL,
#     cantidad INT NOT NULL,
#     precio_unitario DECIMAL(10,2) NOT NULL,
#     subtotal DECIMAL(10,2) NOT NULL,
#     FOREIGN KEY (id_venta) REFERENCES Ventas(id_venta),
#     FOREIGN KEY (id_producto) REFERENCES Inventario(id_producto)
# );
# 📂 Tabla: NotificacionesWhatsApp
# Registra los mensajes enviados a los clientes sobre el estado de su reparación.

# sql
# Copiar
# Editar
# CREATE TABLE NotificacionesWhatsApp (
#     id_notificacion INT PRIMARY KEY AUTO_INCREMENT,
#     id_orden INT NOT NULL,
#     id_cliente INT NOT NULL,
#     mensaje TEXT NOT NULL,
#     fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
#     FOREIGN KEY (id_orden) REFERENCES OrdenesServicio(id_orden),
#     FOREIGN KEY (id_cliente) REFERENCES Clientes(id_cliente)
# );
# 📂 Relaciones Clave
# Clientes pueden tener múltiples equipos registrados.

# Equipos están ligados a órdenes de servicio.

# Órdenes de servicio tienen detalles de costos y tiempos.

# Usuarios pueden ser técnicos, recepcionistas o vendedores.
# Ventas están ligadas a clientes y vendedores.
# Inventario gestiona insumos y accesorios.
# Notificaciones WhatsApp informan a los clientes sobre el estado de su reparación.
from flask import Flask, jsonify
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Boolean, Date, create_engine
from sqlalchemy.orm import relationship, backref
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
from contextlib import contextmanager
from sqlalchemy import engine, create_engine,text
import mysql.connector
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from bd_config import db
import logging
logging.basicConfig(level=logging.DEBUG)
class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    #users = db.relationship('User', backref='role', lazy=True)
    permissions = db.Column(db.String(255), nullable=False)
    create_timestamp = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    @staticmethod
    def get_roles():
        sqlString = text("SELECT * FROM view_roles;")
        result = db.session.execute(sqlString)
        role_list = result.fetchall()  # Asignamos los resultados correctamente
        logging.info(f"Role -> get_roles")
        return role_list
        
                
    @staticmethod
    def save_role(Role):
        db.session.add(Role)
        db.session.flush()
        db.session.commit()
        return Role.id
    def save_roles(roles):
        db.session.add_all(roles)
        db.session.flush()
        db.session.commit()
    
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    uuid = db.Column(db.String(120),unique=True ,nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('Role.id'), nullable=False)
    # role = db.relationship('Role', backref='users', lazy=True)
    create_timestamp = db.Column(db.DateTime, nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
    delete_timestamp = db.Column(db.DateTime, nullable=True)
    last_login = db.Column(db.DateTime, nullable=True)
    @staticmethod
    def all_users():
        sqlString = text("select * from users_vw;")
        result = db.session.execute(sqlString)
        user_list = result.fetchall()  # Asignamos los resultados correctamente
        logging.info(f"User -> get_users")
        return user_list
    def save_user(User):
        db.session.add(User)
        db.session.flush()
        db.session.commit()
        return User.id
    def save_users(users):
        db.session.add_all(users)
        db.session.flush()
        db.session.commit()
        
class Client(db.Model):
    __tablename__ = "Client"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    name = db.Column(db.String(120), nullable = False)
    phone = db.Column(db.String(120), nullable = False)
    email = db.Column(db.String(120), nullable = True)
    address = db.Column(db.String(120), nullable = True)
    create_timestamp = db.Column(db.DateTime, nullable = False)
    @staticmethod
    def get_clients():
        sqlString = text("select * from clients_view;")
        result = db.session.execute(sqlString)
        client_list = result.fetchall()  # Asignamos los resultados correctamente
        logging.info(f"Client -> get_clients")
        return 200,client_list
    @staticmethod
    def get_client_by_name(client_name):
        sqlString = text("SELECT * FROM clients_view WHERE client_name = :client_name")
        result = db.session.execute(sqlString, {'client_name': client_name})
        client_list = result.fetchall()
        logging.info(f"Client -> get_client_by_name")
        return client_list
    def save_client(Client):
        db.session.add(Client)
        db.session.flush()
        db.session.commit()
        return Client.id

class Login(db.Model):
    __tablename__ = "Login"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    time_stamp = db.Column(db.DateTime, nullable = False)

class RepairTrackingStep(db.Model):
    __tablename = "DeviceTrackingStep"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    description = db.Column(db.String (120),nullable = False)
    color = db.Column(db.String(120), nullable = True)
class Device(db.Model):
    __tablename__ = "Device"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    device_brand = db.Column(db.String(120), nullable = False)
    device_model = db.Column(db.String(120),nullable = False)
class Device_details(db.Model):
    __tablename = "Device_detail"
    id = db.Column(db.Integer, primary_key = True, nullable = False)
    device_id = db.Column(db.Integer, db.ForeignKey('Device.id'), nullable = False)
    # device = db.relationship('Device', backref='Device_details', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
   # user = db.relationship('User', backref='Device_details', lazy=True)
    create_timestamp = db.Column(db.DateTime, nullable = False)
    device_serial_number = db.Column(db.String(120), nullable = False)
    device_description = db.Column(db.String(120), nullable = False)

class RepairServiceOrder(db.Model):
    __tablename__ = "RepairServiceOrder"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    device_id = db.Column(db.Integer, db.ForeignKey('Device.id'), nullable = False)
    #device_detais = db.relationship('Device_details', backref='RepairServiceOrder', lazy=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable = False)
    #client = db.relationship('Client', backref='RepairServiceOrder', lazy=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    #user = db.relationship('User', backref='RepairServiceOrder', lazy=True)
    RepairServiceOrderStatus = db.Column(db.Integer, nullable = False)
    create_timestamp = db.Column(db.DateTime, nullable = False)  
    start_timestamp = db.Column(db.DateTime, nullable = True)
    end_timestamp = db.Column(db.DateTime, nullable = True)
    total_cost = db.Column(db.Float, nullable = False)
class RepairServiceOrderDetails(db.Model):
    __tablename__ = "RepairServiceOrderDetails"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    repair_service_order_id = db.Column(db.Integer, db.ForeignKey('RepairServiceOrder.id'), nullable = False)
    #repair_service_order = db.relationship('RepairServiceOrder', backref='RepairServiceOrderDetails', lazy=True)
    DevicePart_id = db.Column(db.Integer, db.ForeignKey('DevicePart.id'), nullable = False)
    cost = db.Column(db.Float, nullable = False)
    time_stamp = db.Column(db.DateTime, nullable = False)
class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)
    name = db.Column(db.String(120), nullable = False)

class DevicePart(db.Model):
    __tablename__ = "DevicePart"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)   
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(120), nullable = False)
    price = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    create_timestamp = db.Column(db.DateTime, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    ##category = db.relationship('Category', backref='DevicePart', lazy=True)

class Inventary(db.Model):
    __tablename__ = "Inventory"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)   
    name = db.Column(db.String(120), nullable = False)
    description = db.Column(db.String(120), nullable = False)
    price = db.Column(db.Float, nullable = False)
    cost = db.Column(db.Float, nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    create_timestamp = db.Column(db.DateTime, nullable = False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable = False)
    #category = db.relationship('Category', backref='Inventory', lazy=True)

class Sale(db.Model):
    __tablename__ = "Sale"    
    id = db.Column(db.Integer, primary_key = True, nullable =  False)   
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable = False)
    #user = db.relationship('User', backref='Sale', lazy=True)
    client_id = db.Column(db.Integer, db.ForeignKey('Client.id'), nullable = False)
    #client = db.relationship('Client', backref='Sale', lazy=True)
    total = db.Column(db.Float, nullable = False)
    create_timestamp = db.Column(db.DateTime, nullable = False)

class SaleDetails(db.Model):
    __tablename__ = "SaleDetails"
    id = db.Column(db.Integer, primary_key = True, nullable =  False)   
    sale_id = db.Column(db.Integer, db.ForeignKey('Sale.id'), nullable = False)
    #sale = db.relationship('Sale', backref='SaleDetails', lazy=True)
    device_part_id = db.Column(db.Integer, db.ForeignKey('DevicePart.id'), nullable = False)
    quantity = db.Column(db.Integer, nullable = False)
    price = db.Column(db.Float, nullable = False)
    subtotal = db.Column(db.Float, nullable = False)
# Base = declarative_base()
# engine = create_engine('mysql+pymysql://root:root@localhost:3306/HYCSYSTEM_DB')
# Base.metadata.create_all(engine)
