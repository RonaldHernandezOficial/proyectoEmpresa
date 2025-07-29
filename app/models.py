# Modelo para los roles de usuario
from . import db #El punto se reconoce como el archivo "__init__.py" igual el application

#dependencia para fecha y hora
from datetime import datetime

#crear los modelos 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date, Text, DECIMAL
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

# Crear una instancia de Base


# Modelo para los roles de usuario
class Rol(db.Model):
    __tablename__ = 'Rol'
    id = Column(Integer, primary_key= True)
    tipoRol = Column(String(45), nullable = False)

class Usuario(db.Model):
    __tablename__ = 'Usuario'
    idUsu = Column(Integer, primary_key = True)
    nombreUsuario = Column(String(45), nullable = False)
    apellidoUsuario = Column(String(45), nullable = False)
    telefonoUsuario = Column(String(45), nullable = False)
    emailUsuario= Column(String(45), nullable = False)
    contrasenaUsuario = Column(String(45), nullable = False)
    idRolFk = Column(Integer, ForeignKey('Rol.id'))
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())
    rol = db.relationship('Rol', backref='usuarios')
    
class Garantias(db.Model):
    __tablename__ = 'Garantia'
    idGarantia = Column(Integer, primary_key = True)
    fechaGarantia = Column(Date, nullable = False)
    descripcionGarantia = Column(Text, nullable = False)
    tipoGarantia = Column(String(255), nullable = False)
    estadoGarantia = Column(String(255), nullable = False)
    idUsuFk = Column(Integer, ForeignKey('Usuario.idUsu'))
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

class Contrato(db.Model):
    __tablename__ = 'Contrato'
    idContrato = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tipoContrato = db.Column(db.String(50), nullable=False)
    descripcionContrato = db.Column(db.Text, nullable=False)
    idGarantiaFk = db.Column(db.Integer, db.ForeignKey('Garantia.idGarantia'))
    idUsuFk = db.Column(db.Integer, db.ForeignKey('Usuario.idUsu'))

class Pqrs(db.Model):
    __tablename__ = 'Pqrs'
    idPqrs = db.Column(db.Integer, primary_key=True)
    tipoPqrs = db.Column(db.String(255), nullable=False)
    descripcionPqrs = db.Column(db.Text, nullable=False)
    estadopqrs = db.Column(db.Text, nullable=False)
    idGarantiaFk = db.Column(db.Integer, db.ForeignKey('Garantia.idGarantia'))
    idContratoFk = db.Column(db.Integer, db.ForeignKey('Contrato.idContrato'))
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

    reseñas = db.relationship('Reseñas', backref='pqr', lazy=True)

class Reseñas(db.Model):
    __tablename__='Reseñas'
    idReseña = Column(Integer, primary_key = True)
    nombre = Column(String(100), nullable = False)
    correo = Column(String(100), nullable = False)
    comentarios = Column(Text, nullable = False)
    calificacion = Column(String(50), nullable = False)
    idUsuFk = Column(Integer, ForeignKey('Usuario.idUsu'))
    idPqrFk = Column(Integer, ForeignKey('Pqrs.idPqrs'))
    fecha_creacion = db.Column(db.DateTime, default=db.func.now())

class ReporteVentas(db.Model):
    __tablename__ = 'ReporteVentas'
    idReporte = db.Column(db.Integer, primary_key=True, autoincrement=True)
    edificio = db.Column(db.String(100), nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    descripcion = db.Column(db.Text)
    estado = db.Column(db.Enum('Realizado', 'Pendiente', 'Cancelado'), default='Pendiente')
    acciones_realizadas = db.Column(db.Text)
    fotos = db.Column(db.LargeBinary)  # O String si usas rutas de imagen
    fecha_creacion = db.Column(db.DateTime, server_default=db.func.now())
    fecha_actualizacion = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())
    idUsuFk = db.Column(db.Integer, db.ForeignKey('Usuario.idUsu'))
    usuario = db.relationship('Usuario', backref='reportes')