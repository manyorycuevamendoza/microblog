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
    user = {'username': 'Manyory Omar Diego'}
    return render_template('index.html', title='Home', user=user)
@app.route('/indexdinamico',methods=['GET'])
def indexdinamico():
    args=request.args
    title=args.get('title')
    username=args.get('username')
    user={'username':username}
    return render_template('index.html',title=title,user=user)
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
@app.route("/addNumbers", methods=["GET"])
def add():
    args = request.args
    val1 = int(args.get("val1"))
    val2 = int(args.get("val2"))
    return str(val1+val2)
@app.route("/users")
def getAllUsers():
    users = User.query.all()
    print(users)
    userStrings = ""
    for user in users:
        userStrings += user.username + " " + user.password + " " + user.email + "<br>"
    return userStrings
@app.route("/reviews/add", methods=["GET"])
def addReview():
    args = request.args
    rating = args.get("rating")
    description = args.get("description")
    newReview = Review(rating=rating, description=description)
    db.session.add(newReview)
    db.session.commit()
    return "Review added"
@app.route("/reviews")
def getReviews():
    reviews = Review.query.all()
    print(reviews)
    reviewString = ""
    for review in reviews:
        reviewString += "Rating: " + str(review.rating) + "/5. Description: " + review.description + "<br>"
    return reviewString