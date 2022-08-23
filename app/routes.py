from app import app
from datetime import datetime
import re
from flask import render_template, request
from app.models import User, Review
from app import db

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Jose'}
    return render_template('index.html', title='Home', user=user)
@app.route("/hello/<name>")
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
@app.route("/add/user", methods=['GET'])
def addUser():
    args = request.args
    username = args.get("username")
    password = args.get("password")
    email = args.get("email")
    #returnString = "Username: " + username + " Password: " + password + "Email: " + email
    newUser = User(username=username, password=password, email=email)
    db.session.add(newUser)
    db.session.commit()
    return "User added"
@app.route("/users")
def getAllUsers():
    users = User.query.all()
    userStrings = ""
    for user in users:
        userStrings += user.username + " " + user.password + " " + user.email + "<br>"
    return userStrings
@app.route("/reviews/add")
def addReview():
    newReview = Review(rating=3, description="Very good movie.")
    db.session.add(newReview)
    db.session.commit()
    return "Review added"