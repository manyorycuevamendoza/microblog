from datetime import datetime
from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer)
    description = db.Column(db.String(120))
    
    def __repr__(self):
        return '<Review {} {}>'.format(self.rating, self.description)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    author = db.Column(db.String(120))


    def __repr__(self):
        return '<Book {} {}>'.format(self.title, self.author)

class Practica(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(120))
    apellido = db.Column(db.String(120))

    def __repr__(self):
        return '<Practica {} {}>'.format(self.nombre, self.apellido)

"""Diseñar una clase Usuario en Flask-SQLAlchemy que tenga las siguientes propiedades: id, username, 
password, email. Implementar la clase de manera apropiada para que el id sea la llave primaria y se 
calcule automáticamente, y los tipos de datos apropiados para las demás columnas. 
Implementar un servidor de Flask que permite interactuar al cliente de la siguientes maneras: 
• Agregar un usuario: El cliente manda una solicitud GET con los parámetros y valores adecuados. 
Además, verificar que la contraseña tenga por lo menos longitud 8 y que tenga un número y una 
letra. 
• Actualizar un usuario: El cliente manda una solicitud GET con el nombre de usuario como 
parámetro de la ruta, y parámetros de la URL a actualizar (ej. 
localhost:5000/users/update/<username>?password=contrasena123). La solicitud puede o no 
tener varios parámetros a actualizar 
• Solicitar un usuario: El cliente manda una solicitud GET con el nombre de usuario como 
parámetro de la ruta (ej. localhost:5000/users/<username>). El servidor devuelve toda la 
información del usuario menos el id. 
• Borrar un usuario: El cliente manda una solicitud GET con el nombre del usuario como 
parámetro de la ruta (ej. localhost:5000/users/delete/<username>) """

class clase(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(8))
    email = db.Column(db.String(120))

    def __repr__(self):
        return '<clase {} {} {}>'.format(self.username, self.password, self.email)


class Estudiante(db.Model):
    id=db.Column(db.Integer, primary_key=True) 
    codigo=db.Column(db.String(8), index=True,unique=True)
    nombre=db.Column(db.String(20), index=True,unique=True)
    apellido=db.Column(db.String(20))

    def __repr__(self):
        return '<Estudiante {} {}>'.format(self.nombre,self.apellido)