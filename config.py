import os
basedir = os.path.abspath(os.path.dirname(__file__))#saca la ruta absoluta del directorio donde se encuentra el archivo config.py

class Config(object):
    #cuando accdemos a una ruta local 
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'postgresql://postgres:76591212@localhost:5432/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = False