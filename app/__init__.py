from flask import Flask
from flask_cors import CORS
from flask_mysqldb import MySQL


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

CORS(app, resources={r"/api/*": {"origins": "http://localhost"}})

conexion = MySQL(app)

from app.models import register
from app.models import ordenes
from app.models import devoluciones
from app.models import productos
from app.models import proveedores
from app.models import existencias
from app.models import productosRecividos
from app.models import categoriasPRO
from app.models import clientes
from app.models import ventas
from app.models import proveedoresMap