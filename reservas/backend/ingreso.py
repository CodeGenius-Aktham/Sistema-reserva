from flask import Flask, request, jsonify # Importacion de la libreria Flask.
from flask_cors import CORS # Comunicacion entre el backend y el fronted.
from psycopg2 import IntegrityError # Importacion de la libreria que es el adaptador de postgresql y sus errores.
from dotenv import load_dotenv # Ayuda a cargar las variables de entorno del archivo .env
import psycopg2 # Importacion de la libreria que maneja la base de datos.
import os # Libreria para manejar el archivo .env
import time


# Identificador de la aplicacion.
app = Flask(__name__)
CORS(app, origins="https://codegenius-aktham.github.io", supports_credentials=True) # URL del fronted con credenciales para hacer peticiones.

load_dotenv()

# Conexion a la base de datos de usuario y reservas.
def conexion_db():
    """Establece y devuelve una conexión a la base de datos postgressql."""
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
    # Manejo de errores.
    except Exception as error:
        print(f"error de conexion con la base de datos : {error}.")
        return None
    except IntegrityError as error:
        conn.rollback() # Se deshacen los cambios si la conexion falla.
        return jsonify({'error' : 'error de integridad con la base de datos.'}),400


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
        # Ingreso de datos a la base de datos. (Usando %s que es el placeholder para postgresql.)
        cursor.execute('''
            INSERT INTO usuarios(nombre_usuario, apellido_usuario, cedula_usuario)
            VALUES (%s,%s,%s)
            RETURNING id
        ''', (nombre_usuario, apellido_usuario, cedula_usuario))
        # Se busca el nuevo id generado con el ingreso.
        nuevo_id = cursor.fetchone()[0]
        # Se suben los cambios a la base de datos.
        conn.commit()
        return jsonify({"mensaje": "Usuario ingresado con éxito.", "id": nuevo_id}), 201 # Devuelve el ID generado
    # Manejo de errores por si la cedula se repite.
    except psycopg2.errors.UniqueViolation:
        # El mensaje de error de postgresql será diferente. Ajusta la comprobación.
        conn.rollback()
        return jsonify({"error": "La cédula ya está registrada."}), 400
    # Si se presenta un error en el programa se marca en el manejo de errores.
    except Exception as error:
        return jsonify({"error": f"Error inesperado en el programa: {str(error)}."}), 500
    finally:
        cursor.close() # Cierre del cursor de la base de datos.
        conn.close() # Cierre de la conexion de la base de datos.


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
    

    # Usamos el id generado para usarlo en la consulta a la base de datos con la que sabremos quien hizo la reserva.
    try:
        usuario_id = int(data['usuario_id'])
    except KeyError as error:
        return jsonify({'error' : f'No se encontro el Id del usuario : {str(error)}'}),400
    except ValueError:
        return jsonify({'error' : 'El Id del usuario debe ser numerico'}),400

    try:
        # Creacion del cursor para manejo de la base de datos.
        cursor = conn.cursor()
        # Busqueda del campo "usuario_id".
        usuario_id = data.get('usuario_id')
        referencia = f'referencia_{usuario_id}_{int(time.time)}'
        # Ingreso de la informacion a la base de datos.
        cursor.execute('''
            INSERT INTO reservas(fecha_reserva, hora_reserva, hora_termino, estado_reserva, usuario_id,referencia)
            VALUES(%s,%s,%s,%s,%s,%s)
        ''', (fecha_reserva, hora_reserva, hora_termino, estado_reserva, usuario_id,referencia))
        # Se suben los cambios a la base de datos.
        conn.commit()
        return jsonify({"mensaje": "reserva ingresada con exito."}), 200
    # Error si la reserva ya esta registrada.
    except psycopg2.errors.UniqueViolation:
            conn.rollback() # Elimina la accion si la reserva ya existe.
            return jsonify({"error": "Ya existe una reserva para esa fecha y hora."}), 400
    # Error en el programa.
    except Exception as error:
        return jsonify({"error": f"error inesperado en el programa : {str(error)}"}), 500
    finally:
        cursor.close() # Se cierra el cursor base de datos.
        conn.close() #  Se cierra la base de datos.



