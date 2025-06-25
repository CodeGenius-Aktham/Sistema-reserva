from flask import Flask, request, jsonify # Importacion de la libreria Flask
from flask_cors import CORS
from psycopg2 import IntegrityError # Importacion de la libreria SQLite3 para manejo de la base de datos.
import psycopg2
import pandas as pd # Importacion de pandas para visualizar los datos.

# Identificador de la pagina para el jefe de la aplicacion.
app = Flask(__name__)
CORS(app, origins=["https://codegenius-aktham.github.io"])

# Conexion con la base de datos.
def conexion_db():
    """Establece y devuelve una conexión a la base de datos SQLite."""
    try:
        conn = psycopg2.connect(
            host = "dpg-d1cpt6idbo4c73allepg-a.oregon-postgres.render.com",
            dbname = "usuarios_2vaw",
            user = "usuarios_2vaw_user",
            password = "caXbkri7k5AzKOSrY4C2LX52uINHgINx",
            port = "5432",
            sslmode = "require"
        )
        return conn
    except IntegrityError as err:
        conn.rollback()
        print(f"Error al conectar a la base de datos SQLite: {err}")
        return None

# Ingreso y enrutador para eliminacion de usuarios.
@app.route('/delete', methods = ["POST"])
def eliminar_datos():
    # Convierte la informacion a un archivo Json.
    data = request.get_json() 
    # Ingreso del campo de eliminacion de usuario.
    eliminar_usuario = data.get('eliminar','').strip()

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
        cursor.execute('''SELECT * FROM usuarios WHERE user_id = %s''',(eliminar_usuario,))
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
        conn.rollback()
        return jsonify({"error" : "Error de integridad al eliminar los datos.."}),400
    except Exception as error:
        return jsonify({"error" : f"Se detecto un error inesperado : {str(error)}"}),400
    finally:
        cursor.close()
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
                    usuarios.nombre_usuario,
                    usuarios.apellido_usuario,
                    usuarios.cedula_usuario,
                    reservas.fecha_reserva,
                    reservas.hora_reserva,
                    reservas.hora_termino,
                    reservas.estado_reserva
                FROM usuarios
                JOIN reservas ON usuarios.id = reservas.usuario_id
                ORDER BY reservas.fecha_reserva DESC;
                ''',conn)
        # Resultado del lector y conversion a una archivo Json.
        resultado = df.to_dict(orient='records')
        # Retorno de los resultados de las tablas.
        return jsonify({"resultado" : resultado}),200
    # Manejo de errores.
    except Exception as error:
        return jsonify({"error" : f"error inesperado en el programa : {str(error)}"})
    finally:
        conn.close() # Cierre de la base de datos.