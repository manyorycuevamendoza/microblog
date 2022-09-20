from app import app
from datetime import datetime
import re
from flask import render_template, request
from app.models import User, Review, Estudiante#importamos los modelos que vamos a utilizar en rutad
from app import db
import requests
import json
from flask_cors import CORS, cross_origin
#from 
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Manyory'}
    return render_template('index.html', title='Home', user=user)



@app.route("/hello/<name>")#el name luego se pasa como parametro a la funcion
def hello_there(name):
    now = datetime.now()
    formatted_now = now.strftime("%A, %d %B, %Y at %X")

    # Filter the name argument to letters only using regular expressions. URL arguments
    # can contain arbitrary text, so we restrict to safe characters only.
    match_object = re.match("[a-zA-Z]+", name)

    if match_object:
        clean_name = match_object.group(0)
    else:
        clean_name = "Friend"

    content = "Hello there, " + clean_name + "! It's " + formatted_now
    return content

#----indexdinamico-------
@app.route('/indexdinamico',methods=['GET'])
def indexdinamico(): # index dinamico es para que se pueda acceder a la pagina desde cualquier parte
    #localhost:5000/indexdinamico?title=CursoPlataformas&username=usuarioUTECCS2031
    #Hola, usuarioUTECCS2031
    args=request.args
    title=args.get('title')
    username=args.get('username')
    user={'username':username}
    return render_template('index.html',title=title,user=user)

#-----User routes-----
##añade usuario
@app.route("/add/user", methods=['GET'])
#localhost:5000/add/user?usernameee=cueva&password=76591212&email=cueva@utec.edu.pe
#Falta parámetro username
def addUser():
        #usamos el try para poder recuperarnos de algun errro
    try:
        #esta ruta espera tres parametros
        args = request.args
        username = args.get("username")
        password = args.get("password")
        email = args.get("email")
        #el usuario podria no mandar los parametros, hay que verificar que sean validos
        if (username == None):
            return "Falta parametro username"
        elif (password == None):
            return "Falta parametro password"
        elif (email == None):
            return "Falta parametro email"
        
        if (not verifyPassword(password)):
            return "Contrasena invalida"
        #creamos un nuevo usuario de clase User 
        newUser = User(username=username, password=password, email=email)
        #agregamos el usuario a la sesion actual de la db
        db.session.add(newUser)
        #mandamos los cambios para que persistan en la db
        db.session.commit()
    #en caso ocurra un error podemos recuperarnos sin romper el flujo del programa    
    except Exception as error:
        print("Invalid user", error)
        return "Invalid user"       
    return "User added"


@app.route("/addNumbers", methods=["GET"])
def add():
    #http://localhost:5000/addNumbers?val1=2&val2=hola
    #val2 no es un numero
    #http://localhost:5000/addNumbers?val1=2&val2=3
    #5
    args = request.args
    try: #es para que no se caiga el programa si no se ingresa un numero, osea manejar el error
        val1 = int(args.get("val1"))
    except Exception as error:#viene de psycotescrud.py
        print(error)
        return "val1 no es un numero"
    try:
        val2 = int(args.get("val2"))
    except Exception as error:
        print(error)
        return "val2 no es un numero"
    return str(val1+val2)
#mostar usuarios
@app.route("/users")
#http://localhost:5000/users
#se observara todos los usuarios que estan en la base de datos
def getAllUsers():
    #podemos pedir la informacion de varias filas de la tabla
    #al mismo tiempo usando 'query.all()', esto devuelve una lista
    users = User.query.all()
    print(users)
    userStrings = ""
    for user in users:
        userStrings += user.username + " " + user.password + " " + user.email + "<br>"#el br es el cambio de linea en html
    return userStrings


 #-----------Reviews   
@app.route("/reviews/add", methods=["GET"] )
def addReview():
    args = request.args# reuqest es para obtener los datos que se envian por la url
    rating = args.get("rating")
    if rating >5 or rating <0:
        return "ingrese un rating entre 0 y 5"
    description = args.get("description")
    newReview = Review(rating=rating, description=description)
    db.session.add(newReview)
    db.session.commit()
    return "Review added"
@app.route("/reviews")
def getReviews():
    #http://localhost:5000/reviews/1
    # Rating: 4/5 Description: Buena
    reviews = Review.query.all()
    print(reviews)
    reviewString = ""
    for review in reviews:
        reviewString += "Rating: " + str(review.rating) + "/5. Description: " + review.description + "<br>"
    return reviewString
@app.route("/reviews/<id>/pid")#se coloca <id> para que se pueda ingresar un id ya que es dinamico y se puede acceder desde cualquier parte
def getReview(id,pid):
    print(pid)
    #query nos permite filtrar datos basado en ciertas condiciones
    #aqui estamos filtrando la fila que tenga el mismo id que se paso en el URL
    #la funcion first() coge el primer valor del resultado
    review = Review.query.filter(Review.id==id).first()
    print(review)
    if review == None:
        return "no existe"
    return "Rating: " + str(review.rating) + "/5. Description: " + review.description
#Esta ruta se comunica con un API externo, nationalize,
#que retorna un objeto JSON con probabilidades que el nombre
#dado venga de un pais especifico
#este es un ejemplo de un request
#https://api.nationalize.io/?name=jose
#y un ejemplo de la respuesta
# {
#   "name": "jose",
#   "country": [
#     {
#       "country_id": "VE",
#       "probability": 0.05786648552663837
#     },
#     {
#       "country_id": "ES",
#       "probability": 0.05710861497406078
#     },
#     {
#       "country_id": "SV",
#       "probability": 0.05705595515479477
#     }
#   ]
# }


@app.route('/consolidarPaises')# esta ruta es para consolidar los paises de los usuarios y mostrarlos en una tabla html
def consolidarPaises():
    #names=["pedro","jose","miguel","john","paul","george","ringo"]
    estudiantes=Estudiante.query.all()
    paises={}
    #for name in names:
    for estudiante in estudiantes:
        name=estudiante.nombre
        url = "https://api.nationalize.io/?name=" + name
        result=requests.get(url).json()
        pais=result["country"][0]["country_id"]
        if pais in paises:
            paises[pais]+=1
        else:
            paises[pais]=1
    return paises
####Estudiante###########
@app.route("/estudiantes")
def getEstudiantes():
    estudiantes= Estudiante.query.all()
    estudianteEstring=""
    for estudiante in estudiantes:
        estudianteEstring += "Nombre: " + estudiante.nombre + " Apellido: " + estudiante.apellido + "<br>"
    return estudianteEstring

@app.route("/estudiantes/create", methods=["GET"])
def createEstudiante():
    args = request.args
    codigo=args.get("codigo")
    nombre=args.get("nombre")
    apellido=args.get("apellido")

    newEstudiante = Estudiante(codigo=codigo, nombre=nombre, apellido=apellido)

    db.session.add(newEstudiante)
    db.session.commit()
    return "Estudiante agregado"

def verifyPassword(password):
    return len(password)>=10
    