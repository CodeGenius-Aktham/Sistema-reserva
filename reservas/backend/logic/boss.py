from flask import Flask, request, jsonify # Importacion de la libreria Flask.
from flask_cors import CORS # Comunicacion entre el backend y el fronted.
from backend.data import conexion # Importamos el modulo de la conexion con la base de datos.
import psycopg2 # Importacion de la libreria que maneja la base de datos.
import datetime # Importacion de la libreria 'datetime' para usarña en la conversion a str.
import pandas as pd # Importacion de pandas para visualizar los datos.

# Identificador de la pagina para el jefe de la aplicacion.
app = Flask(__name__)
CORS(app, origins="https://codegenius-aktham.github.io", supports_credentials=True) # URL del fronted con credenciales para hacer peticiones.


def conexion_db():
    return conexion.conexion_db()


# Ingreso y enrutador para eliminacion de usuarios.
@app.route('/delete', methods = ["POST"])
def eliminar_datos():
    # Convierte la informacion a un archivo Json.
    data = request.get_json() 
    # Ingreso del campo de eliminacion de usuario.
    eliminar_usuario = int(data.get('eliminar','').strip())

    # Validaddor de campo ingresado.
    if not eliminar_usuario:
        return jsonify({"error" : "El campo debe estar completo"}),400

    # Recibe la conexion con la base de datos.
    conn = conexion_db()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500
    
    try:
        cursor = conn.cursor() # Cursor para manejo de la base de datos.
        # Consulta para la busqueda del usuario y consultar si se encuntra o no.
        cursor.execute('''SELECT * FROM usuarios WHERE id = %s''',(eliminar_usuario,))
        if cursor.fetchone() is None:
            return jsonify({"error" : "Usuario no encontrado."}),400
        # Eliminacion de datos tanto en la reserva como en la tabla de registro.
        cursor.execute('''DELETE FROM reservas WHERE id = %s''',(eliminar_usuario,))
        cursor.execute('''DELETE FROM usuarios WHERE id = %s''', (eliminar_usuario,))
        # Se suben los cambios.
        conn.commit() 
        return jsonify({"mensaje" : "Usuario y reserva eliminado con exito."}),200

    # Manejo de errores.
    except psycopg2.IntegrityError:
        conn.rollback() # Se deshacen los cambios si la conexion falla.
        return jsonify({"error" : "Error de integridad al eliminar los datos.."}),400
    except Exception as error:
        return jsonify({"error" : f"Se detecto un error inesperado : {str(error)}"}),400
    finally:
        cursor.close() # se cierra el cursor de la base de datos.
        conn.close() # Cierre de la base de datos.


# Consulta de datos y enrutador para la visualizacion de datos.
@app.route('/show', methods = ["GET"])
def visualizar_datos():
    conn = conexion_db() # Recibe la conexion con la base de datos.
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500
    
    try:
        # Lector de la query en SQL
        df = pd.read_sql_query('''
                SELECT
                    usuarios.id,
                    usuarios.nombre_usuario,
                    usuarios.apellido_usuario,
                    usuarios.cedula_usuario,
                    reservas.fecha_reserva,
                    reservas.hora_reserva,
                    reservas.hora_termino,
                    reservas.estado_reserva,
                FROM usuarios
                JOIN reservas ON usuarios.id = reservas.usuario_id
                ORDER BY reservas.fecha_reserva DESC;
                ''',conn)
        # Conversión segura de campos de tipo tiempo o fecha
        for columna in ["fecha_reserva", "hora_reserva", "hora_termino"]:
            # se revisa cada columna en la consulta.
            if columna in df.columns:
                # se aplica la conversion a cada columna con los parametros adecuados. (La conversion es a un string.)
                df[columna] = df[columna].apply(
                    lambda x: x.strftime("%H:%M:%S") if isinstance(x, datetime.time)
                    else (x.strftime("%Y-%m-%d") if isinstance(x, datetime.date) else str(x))
                )
        # Resultado del lector y conversion a una archivo Json.
        resultado = df.to_dict(orient='records')
        # Retorno de los resultados de las tablas.
        return jsonify({"resultado" : resultado}),200
    # Manejo de errores.
    except Exception as error:
        return jsonify({"error" : f"error inesperado en el programa : {str(error)}"})
    finally:
        conn.close() # Cierre de la base de datos.