from flask import Flask, request, jsonify # Importacion de la libreria Flask.
from flask_cors import CORS # Comunicacion entre el backend y el fronted.
from backend.data import conexion # Importacion del modulo de la base de datos de la capa data.
import psycopg2 # Importacion de la libreria que maneja la base de datos.


app = Flask(__name__)
CORS(app, origins="https://codegenius-aktham.github.io", supports_credentials=True)

#Funcion que pasa la conexion con la base de datos.
def conexion_db():
    return conexion.conexion_db()


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
        # Ingreso de la informacion a la base de datos.
        cursor.execute('''
            INSERT INTO reservas(fecha_reserva, hora_reserva, hora_termino, estado_reserva, usuario_id)
            VALUES(%s,%s,%s,%s,%s)
        ''', (fecha_reserva, hora_reserva, hora_termino, estado_reserva, usuario_id))
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