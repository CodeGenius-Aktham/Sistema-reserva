from flask import Flask, request, jsonify
from datetime import datetime
import sqlite3
from flask_cors import CORS # Importa la extensión CORS

# Identificador de la aplicacion.
app = Flask(__name__)
CORS(app) # Habilita CORS para toda la aplicación Flask

# Ruta absoluta a la base de datos.
# Es buena práctica que esta ruta sea configurable (e.g., desde una variable de entorno)
# o relativa al directorio de la aplicación para mayor portabilidad.
DATABASE = r"C:\Users\POWER\reservas_fp.db"

# Conexion a la base de datos de usuario y reservas.
def conexion_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Funcion para inicializar la base de datos y crear tablas si no existen.
def init_db():
    conn = conexion_db()
    cursor = conn.cursor()
    # Crear tabla de usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL,
            apellido_usuario TEXT NOT NULL,
            cedula_usuario TEXT NOT NULL UNIQUE
        )
    ''')
    # Crear tabla de reservas
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha_reserva TEXT NOT NULL,
            hora_reserva TEXT NOT NULL,
            hora_termino TEXT NOT NULL,
            estado_reserva TEXT NOT NULL,
            UNIQUE(fecha_reserva, hora_reserva)
        )
    ''')
    conn.commit()
    conn.close()

# Endpoint para verificar la conexion a la base de datos
@app.route('/check_db_connection', methods=['GET'])
def check_db_connection():
    try:
        conn = conexion_db()
        conn.cursor() # Intenta obtener un cursor para verificar la conexión
        conn.close()
        return jsonify({"status": "success", "message": "Conexión a la base de datos exitosa."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": f"Error al conectar con la base de datos: {str(e)}."}), 500

# Ingreso y enrutador del registro.
@app.route('/register', methods=['POST'])
def registro_usuario():
    data = request.get_json()

    nombre_usuario = data.get('nombre', '').strip()
    apellido_usuario = data.get('apellido', '').strip()
    cedula_usuario = data.get('cedula', '').strip()

    if not all([nombre_usuario, apellido_usuario, cedula_usuario]):
        return jsonify({"error": "Todos los campos deben estar completos."}), 400

    conn = conexion_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO usuarios(nombre_usuario, apellido_usuario, cedula_usuario)
            VALUES (?, ?, ?)
        ''', (nombre_usuario, apellido_usuario, cedula_usuario))
        conn.commit()
        return jsonify({"mensaje": "Usuario ingresado con éxito."}), 200
    except sqlite3.IntegrityError as error:
        if "UNIQUE constraint failed: usuarios.cedula_usuario" in str(error):
            return jsonify({"error": "La cédula ya está registrada."}), 400
        return jsonify({"error": "Error de integridad: " + str(error)}), 400
    except Exception as error:
        return jsonify({"error": f"Error inesperado en el programa: {str(error)}."}), 500
    finally:
        conn.close()

# Ingreso y enrutador de las reservas.
@app.route('/reservation', methods=['POST'])
def registro_reserva():
    data = request.get_json()

    fecha_reserva = data.get('fecha', '').strip()
    hora_reserva = data.get('hora', '').strip()
    hora_termino = data.get('termino', '').strip()
    estado_reserva = data.get('estado', '').strip()

    if not all([fecha_reserva, hora_reserva, hora_termino, estado_reserva]):
        return jsonify({"error": "Todos los campos deben estar completos."}), 400

    try:
        # Validación de formato de fecha y hora
        datetime.strptime(fecha_reserva, "%d/%m/%Y")
        datetime.strptime(hora_reserva, "%H:%M")
        datetime.strptime(hora_termino, "%H:%M")
    except ValueError:
        return jsonify({"error": "La fecha o las horas no tienen un formato válido (DD/MM/YYYY y HH:MM)."}), 400

    conn = conexion_db()
    try:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO reservas(fecha_reserva, hora_reserva, hora_termino, estado_reserva)
            VALUES(?, ?, ?, ?)
        ''', (fecha_reserva, hora_reserva, hora_termino, estado_reserva))
        conn.commit()
        return jsonify({"mensaje": "Reserva ingresada con éxito."}), 200
    except sqlite3.IntegrityError as error:
        if "UNIQUE constraint failed: reservas.fecha_reserva, reservas.hora_reserva" in str(error):
            return jsonify({"error": "Ya existe una reserva para esa fecha y hora."}), 400
        return jsonify({"error": "Error de integridad: " + str(error)}), 400
    except Exception as error:
        return jsonify({"error": f"Error inesperado en el programa: {str(error)}"}), 500
    finally:
        conn.close()

# Esto asegura que la base de datos se inicialice cuando el script se ejecute directamente
if __name__ == '__main__':
    init_db() # Llama a la función para crear las tablas si no existen
    app.run(debug=True) # Inicia el servidor Flask en modo depuración
