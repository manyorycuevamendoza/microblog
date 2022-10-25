from flask import Flask #para crear programas
from config import Config
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)#inicializar la aplicacion
app.config.from_object(Config)#algo adicional para flask
db = SQLAlchemy(app)#tipo de base de datos que se va a usar

from app import routes, models
