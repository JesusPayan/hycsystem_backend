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
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    users = db.relationship('User', backref='role', lazy=True)
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    uuid = db.Column(db.String(120),unique=True ,nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship('Role', backref='users', lazy=True)
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
    __tablename = "Device_Detail"
    id = db.Column(db.Integer, primary_key = True, nullable = False)

