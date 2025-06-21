from flask import Flask, request, jsonify # Importacion de la libreria Flask
from datetime import datetime # Importacion de la libreria datetime para manejo de fechas y horas.
import sqlite3 # Importacion de la libreria SQLite3 para manejo de la base de datos.
from flask_cors import CORS # Importacion de Flask-CORS para manejar las solicitudes de origen cruzado.
import os # Importacion para manejar rutas de archivos

# Identificador de la aplicacion.
app = Flask(__name__)
CORS(app) # Habilitar CORS para toda la aplicación Flask.

# Define la ruta relativa a la base de datos.
# Esto asume que 'reservas_fp.db' estará en la misma carpeta que este script.
DATABASE_NAME = 'reservas_fp.db'
# Obtiene la ruta absoluta del directorio actual del script
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# Une la ruta base con el nombre del archivo de la base de datos
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

# Conexion a la base de datos de usuario y reservas.
def conexion_db():
    # Conexión a la base de datos usando la ruta definida arriba.
    # Si la base de datos no existe, SQLite la creará automáticamente en esta ruta.
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn

# Función para inicializar la base de datos (crear tablas si no existen)
def init_db():
    # Asegúrate de que el directorio para la base de datos exista
    db_directory = os.path.dirname(DATABASE_PATH)
    if not os.path.exists(db_directory):
        os.makedirs(db_directory)
        print(f"Directorio creado para la base de datos: {db_directory}")

    conn = conexion_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY PRIMARY KEY AUTOINCREMENT,
            nombre_usuario TEXT NOT NULL,
            apellido_usuario TEXT NOT NULL,
            cedula_usuario TEXT UNIQUE NOT NULL
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reservas (
            id INTEGER PRIMARY PRIMARY KEY AUTOINCREMENT,
            fecha_reserva TEXT NOT NULL,
            hora_reserva TEXT NOT NULL,
            hora_termino TEXT NOT NULL,
            estado_reserva TEXT NOT NULL,
            UNIQUE(fecha_reserva, hora_reserva)
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Base de datos '{DATABASE_PATH}' y tablas verificadas/creadas.")


# Llamar a init_db al inicio para asegurar que las tablas existen
# Esto es importante para que la DB se cree o verifique cada vez que la app se inicia.
init_db()


# Ingreso y enrutador del registro.
@app.route('/register', methods = ['POST'])
def registro_usuario():
        # Convierte la informacion en un archivo Json.
        data = request.get_json()

        # Ingreso de datos solicitados.
        nombre_usuario = data.get('nombre','').strip()
        apellido_usuario = data.get('apellido','').strip()
        cedula_usuario = data.get('cedula','').strip()

        # Validador de campos ingresados.
        if not all([nombre_usuario,apellido_usuario,cedula_usuario]):
            return jsonify({"error" : "Todos los campos deben estar completos."}),400

        # Toma la conexion con la base de datos.
        conn = conexion_db()
        try:
            # Creacion de un cursor para manejar la base de datos.
            cursor = conn.cursor()
            # Ingreso de datos a la base de datos.
            cursor.execute('''
                        INSERT INTO usuarios(nombre_usuario,apellido_usuario,cedula_usuario)
                        VALUES (?,?,?)
                    ''',(nombre_usuario,apellido_usuario,cedula_usuario))
            # Se suben los cambios a la base de datos.
            conn.commit()
            return jsonify({"mensaje" : "Usuario ingresado con éxito."}),201 # 201 Created
        # Manejo de errores por si la cedula se repite.
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: usuarios.cedula_usuario" in str(error):
                return jsonify({"error" : "La cédula ya está registrada"}),409 # 409 Conflict
            return jsonify({"error" : f"Error de integridad: {str(error)}"}),500
        # Si se presenta un error en el programa se marca en el manejo de errores.
        except Exception as error:
            return jsonify({"error" : f"Error inesperado en el programa: {str(error)}."}),500
        finally:
            conn.close() # Se cierra la base de datos.


# Ingreso y enrutador de las reservas.
@app.route('/reservation', methods = ['POST'])
def registro_reserva():
        # Convierte la informacion en un archivo Json.
        data = request.get_json()

        # Ingreso de datos solicitados.
        fecha_reserva = data.get('fecha','').strip()
        hora_reserva = data.get('hora','').strip()
        hora_termino = data.get('termino','').strip()
        estado_reserva = data.get('estado','').strip()

        # Validador de campos ingresados.
        if not all([fecha_reserva,hora_reserva,hora_termino,estado_reserva]):
            return jsonify({"error" : "Todos los campos deben estar completos."}),400
        try:
            datetime.strptime(fecha_reserva,"%d/%m/%Y")
            datetime.strptime(hora_reserva,"%H:%M")
            datetime.strptime(hora_termino,"%H:%M")
        except ValueError:
            return jsonify({"error" : "La fecha o las horas no tienen un formato válido (DD/MM/YYYY y HH:MM)."}),400

        # Toma la conexion con la base de datos.
        conn = conexion_db()
        try:
            # Creacion del cursor para manejo de la base de datos.
            cursor = conn.cursor()
            # Ingreso de la informacion a la base de datos.
            cursor.execute('''
                        INSERT INTO reservas(fecha_reserva,hora_reserva,hora_termino,estado_reserva)
                        VALUES(?,?,?,?)
                        ''',(fecha_reserva,hora_reserva,hora_termino,estado_reserva))
            # Se suben los cambios a la base de datos.
            conn.commit()
            return jsonify({"mensaje" : "Reserva ingresada con éxito."}),201 # 201 Created
        # Manejo de errores por si las fechas de reserva y la hora de la reserva de la cancha son las mismas-
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: reservas.fecha_reserva, reservas.hora_reserva" in str(error):
                return jsonify({"error" : "Ya existe una reserva para esa fecha y hora."}),409 # 409 Conflict
            return jsonify({"error" : f"Error de integridad: {str(error)}"}),500
        # Si se presenta un error en el programa se marca en el manejo de errores.
        except Exception as error:
            return jsonify({"error" : f"Error inesperado en el programa: {str(error)}"}),500
        finally:
            conn.close() # Se cierra la base de datos.

# Nuevo endpoint para obtener todos los usuarios
@app.route('/users', methods=['GET'])
def get_users():
    conn = conexion_db()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, nombre_usuario, apellido_usuario, cedula_usuario FROM usuarios ORDER BY nombre_usuario")
        users = cursor.fetchall()
        # Convertir Rows a diccionarios para jsonify
        users_list = [dict(user) for user in users]
        return jsonify(users_list), 200
    except Exception as error:
        return jsonify({"error": f"Error al obtener usuarios: {str(error)}"}), 500
    finally:
        conn.close()

# Nuevo endpoint para eliminar un usuario por cédula
@app.route('/users/<string:cedula>', methods=['DELETE'])
def delete_user(cedula):
    conn = conexion_db()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM usuarios WHERE cedula_usuario = ?", (cedula,))
        conn.commit()
        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado."}), 404
        return jsonify({"mensaje": "Usuario eliminado con éxito."}), 200
    except Exception as error:
        return jsonify({"error": f"Error al eliminar usuario: {str(error)}"}), 500
    finally:
        conn.close()

# Asegúrate de que tu aplicación se ejecute solo cuando el script es el principal
if __name__ == '__main__':
    # La aplicación se ejecutará en http://127.0.0.1:5000 por defecto
    app.run(debug=True)
