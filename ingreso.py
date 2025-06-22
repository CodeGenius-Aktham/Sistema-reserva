from flask import Flask, request, jsonify # Importacion de la libreria Flask
from flask_cors import CORS
from datetime import datetime # Importacion de la libreria datetime para manejo de fechas y horas.
import sqlite3 # Importacion de la libreria MySQL Connector

# Identificador de la aplicacion.
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": [
    "https://codegenius-aktham.github.io",      # frontend
    "https://sistema-reserva.onrender.com"      # backend
]}})

# Conexion a la base de datos de usuario y reservas.
def conexion_db():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect("reservas_fp.db")
        return conn
    except sqlite3.Error as err:
        print(f"Error al conectar a la base de datos SQLite: {err}")
        return None

# Ingreso y enrutador del registro.
@app.route('/register', methods=['POST'])
def registro_usuario():
    """Registra un nuevo usuario en la base de datos."""
    # Convierte la informacion en un archivo Json.
    data = request.get_json()

    # Ingreso de datos solicitados.
    nombre_usuario = data.get('nombre', '').strip()
    apellido_usuario = data.get('apellido', '').strip()
    cedula_usuario = data.get('cedula', '').strip()

    # Validador de campos ingresados.
    if not all([nombre_usuario, apellido_usuario, cedula_usuario]):
        return jsonify({"error": "Todos los campos deben estar completos."}), 400

    # Toma la conexion con la base de datos.
    conn = conexion_db()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        # Creacion de un cursor para manejar la base de datos.
        cursor = conn.cursor()
        # Ingreso de datos a la base de datos. (Usando ? para SQLite y backticks para la tabla)
        cursor.execute('''
            INSERT INTO usuarios(nombre_usuario, apellido_usuario, cedula_usuario)
            VALUES (?,?,?)
        ''', (nombre_usuario, apellido_usuario, cedula_usuario))
        # Se suben los cambios a la base de datos.
        conn.commit()
        return jsonify({"mensaje": "Usuario ingresado con éxito.", "id": cursor.lastrowid}), 201 # Devuelve el ID generado
    # Manejo de errores por si la cedula se repite.
    except sqlite3.Error as error:
        # El mensaje de error de MySQL será diferente. Ajusta la comprobación.
        if "UNIQUE constraint failed: usuarios.cedula_usuario" in str(error):
            return jsonify({"error": "La cédula ya está registrada."}), 400
        return jsonify({"error": f"Error de integridad: {str(error)}"}), 400
    # Si se presenta un error en el programa se marca en el manejo de errores.
    except Exception as error:
        return jsonify({"error": f"Error inesperado en el programa: {str(error)}."}), 500
    finally:
        conn.close() # Cierre de la base de datos.


# Ingreso y enrutador de las reservas.
@app.route('/reservation', methods=['POST'])
def registro_reserva():
    """Registra una nueva reserva en la base de datos."""
    # Convierte la informacion en un archivo Json.
    data = request.get_json()

    # Ingreso de datos solicitados.
    fecha_reserva = data.get('fecha', '').strip()
    hora_reserva = data.get('hora', '').strip()
    hora_termino = data.get('termino', '').strip()
    estado_reserva = data.get('estado', '').strip()

    # Validador de campos ingresados.
    if not all([fecha_reserva, hora_reserva, hora_termino, estado_reserva]):
        return jsonify({"error": "Todos los campos deben estar completos."}), 400

    # Toma la conexion con la base de datos.
    conn = conexion_db()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        # Creacion del cursor para manejo de la base de datos.
        cursor = conn.cursor()
        # Ingreso de la informacion a la base de datos.
        cursor.execute('''
            INSERT INTO reservas(fecha_reserva, hora_reserva, hora_termino, estado_reserva)
            VALUES(?,?,?,?)
        ''', (fecha_reserva, hora_reserva, hora_termino, estado_reserva))
        # Se suben los cambios a la base de datos.
        conn.commit()
        return jsonify({"mensaje": "reserva ingresada con exito."}), 200
    except sqlite3.IntegrityError as error:
        if "UNIQUE constraint failed: reservas.fecha_reserva, reservas.hora_reserva" in str(error):
            return jsonify({"error": "Ya existe una reserva para esa fecha y hora."}), 400
        return jsonify({"error": "error de integridad"}), 400
    except Exception as error:
        return jsonify({"error": f"error inesperado en el programa : {str(error)}"}), 500
    finally:
        conn.close() # Se cierra la base de datos.



# Identificador de la aplicacion.
app = Flask(__name__)


# Conexion a la base de datos de usuario y reservas.
def conexion_db():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    try:
        conn = sqlite3.connect(r"C:\Users\POWER\reservas_fp.db")
        return conn
    except sqlite3.Error as err:
        print(f"Error al conectar a la base de datos SQLite: {err}")
        return None

# Ingreso y enrutador del registro.
@app.route('/register', methods=['POST'])
def registro_usuario():
    """Registra un nuevo usuario en la base de datos."""
    # Convierte la informacion en un archivo Json.
    data = request.get_json()

    # Ingreso de datos solicitados.
    nombre_usuario = data.get('nombre', '').strip()
    apellido_usuario = data.get('apellido', '').strip()
    cedula_usuario = data.get('cedula', '').strip()

    # Validador de campos ingresados.
    if not all([nombre_usuario, apellido_usuario, cedula_usuario]):
        return jsonify({"error": "Todos los campos deben estar completos."}), 400

    # Toma la conexion con la base de datos.
    conn = conexion_db()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        # Creacion de un cursor para manejar la base de datos.
        cursor = conn.cursor()
        # Ingreso de datos a la base de datos. (Usando ? para SQLite y backticks para la tabla)
        cursor.execute('''
            INSERT INTO usuarios(nombre_usuario, apellido_usuario, cedula_usuario)
            VALUES (?,?,?)
        ''', (nombre_usuario, apellido_usuario, cedula_usuario))
        # Se suben los cambios a la base de datos.
        conn.commit()
        return jsonify({"mensaje": "Usuario ingresado con éxito.", "id": cursor.lastrowid}), 201 # Devuelve el ID generado
    # Manejo de errores por si la cedula se repite.
    except sqlite3.Error as error:
        # El mensaje de error de MySQL será diferente. Ajusta la comprobación.
        if "UNIQUE constraint failed: usuarios.cedula_usuario" in str(error):
            return jsonify({"error": "La cédula ya está registrada."}), 400
        return jsonify({"error": f"Error de integridad: {str(error)}"}), 400
    # Si se presenta un error en el programa se marca en el manejo de errores.
    except Exception as error:
        return jsonify({"error": f"Error inesperado en el programa: {str(error)}."}), 500
    finally:
        conn.close() # Cierre de la base de datos.


# Ingreso y enrutador de las reservas.
@app.route('/reservation', methods=['POST'])
def registro_reserva():
    """Registra una nueva reserva en la base de datos."""
    # Convierte la informacion en un archivo Json.
    data = request.get_json()

    # Ingreso de datos solicitados.
    fecha_reserva = data.get('fecha', '').strip()
    hora_reserva = data.get('hora', '').strip()
    hora_termino = data.get('termino', '').strip()
    estado_reserva = data.get('estado', '').strip()

    # Validador de campos ingresados.
    if not all([fecha_reserva, hora_reserva, hora_termino, estado_reserva]):
        return jsonify({"error": "Todos los campos deben estar completos."}), 400

    # Toma la conexion con la base de datos.
    conn = conexion_db()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500

    try:
        # Creacion del cursor para manejo de la base de datos.
        cursor = conn.cursor()
        # Ingreso de la informacion a la base de datos.
        cursor.execute('''
            INSERT INTO reservas(fecha_reserva, hora_reserva, hora_termino, estado_reserva)
            VALUES(?,?,?,?)
        ''', (fecha_reserva, hora_reserva, hora_termino, estado_reserva))
        # Se suben los cambios a la base de datos.
        conn.commit()
        return jsonify({"mensaje": "reserva ingresada con exito."}), 200
    except sqlite3.IntegrityError as error:
        if "UNIQUE constraint failed: reservas.fecha_reserva, reservas.hora_reserva" in str(error):
            return jsonify({"error": "Ya existe una reserva para esa fecha y hora."}), 400
        return jsonify({"error": "error de integridad"}), 400
    except Exception as error:
        return jsonify({"error": f"error inesperado en el programa : {str(error)}"}), 500
    finally:
        conn.close() # Se cierra la base de datos.

