from app import app
from datetime import datetime
import re
from flask import render_template, request
from app.models import User, Review
from app import db
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
@app.route("/add/user", methods=['GET'])
#localhost:5000/add/user?usernameee=cueva&password=76591212&email=cueva@utec.edu.pe
#Falta parámetro username
def addUser():
    args = request.args
    username = args.get("username")
    password = args.get("password")
    email = args.get("email")

    if(username==None):
        return "Falta parametro username"
    elif(password==None):
        return "Falta parametro password"
    elif(email==None):
        return "Falta parametro email"

    if(not verifyPassword(password)):
        return "Password no valida"
    #returnString = "Username: " + username + " Password: " + password + "Email: " + email
    newUser = User(username=username, password=password, email=email)
    db.session.add(newUser)
    db.session.commit()
    return "User added"


@app.route("/addNumbers", methods=["GET"])
def add():
    #http://localhost:5000/addNumbers?val1=2&val2=hola
    #val2 no es un numero
    args = request.args
    try: #es para que no se caiga el programa si no se ingresa un numero
        val1 = int(args.get("val1"))
    except Exception as error:
        print(error)
        return "val1 no es un numero"
    try:
        val2 = int(args.get("val2"))
    except Exception as error:
        print(error)
        return "val2 no es un numero"
    return str(val1+val2)

@app.route("/users")
#http://localhost:5000/users
#se observara todos los usuarios que estan en la base de datos
def getAllUsers():
    users = User.query.all()
    print(users)
    userStrings = ""
    for user in users:
        userStrings += user.username + " " + user.password + " " + user.email + "<br>"
    return userStrings


 #-----------Reviews   
@app.route("/reviews/add", methods=["GET"])
def addReview():
    args = request.args
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
    review = Review.query.filter(Review.id==id).first()
    print(review)
    if review == None:
        return "no existe"
    return "Rating: " + str(review.rating) + "/5. Description: " + review.description

def verifyPassword(password):
    return len(password)>=10

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


@app.route('/consolidarPaises')
def consolidarPaises():
    estudiantes=Estudiante.query.all()
    paises={}
    for estudiante in estudiantes:
        name=estudiante.nombre
        url="https://api.nationalize.io/?name="+name
        result=requests.get(url).json()
        pais=result['country'][0]['country_id']
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
    