from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from psycopg2 import IntegrityError
import psycopg2
import os


app = Flask(__name__)
CORS(app, origins='https://codegenius-aktham.github.io', supports_credentials=True)

load_dotenv()

# Conexion con la base de datos.
def conexion_db():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    try:
        # Conexion con la base de datos construida en render donde se hizo el despliegue.
        conn = psycopg2.connect(
            host = os.getenv('DB_HOST'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
        )
        return conn # Retorno de la conexion.
    except Exception as error:
        print(f"error de conexion con la base de datos : {error}.")
        return None
    except IntegrityError as error:
        conn.rollback() # Se deshacen los cambios si la conexion falla.
        return jsonify({'error' : 'error de integridad con la base de datos.'}),400