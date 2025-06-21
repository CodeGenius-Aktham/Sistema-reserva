from flask import Flask, request, jsonify # Importacion de la libreria Flask
import sqlite3 # Importacion de la libreria SQLite3 para manejo de la base de datos.
import pandas as pd # Importacion de pandas para visualizar los datos.

# Identificador de la pagina para el jefe de la aplicacion.
app = Flask(__name__)

# Conexion con la base de datos.
def conexion_db():
    conn = sqlite3.connect(r"C:\Users\POWER\reservas_fp.db") # Conexion en la base de datos
    conn.row_factory = sqlite3.Row 
    return conn

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
        cursor.execute('''SELECT * FROM usuarios WHERE user_id = ?''',(eliminar_usuario,))
        if cursor.fetchone() is None:
            return jsonify({"error" : "Usuario no encontrado."}),400
        # Eliminacion de datos tanto en la reserva como en la tabla de registro.
        cursor.execute('''DELETE FROM reservas WHERE user_id = ?''',(eliminar_usuario,))
        cursor.execute('''DELETE FROM usuarios Where user_id = ?''',(eliminar_usuario,))
        # Se suben los cambios.
        conn.commit()
        return jsonify({"mensaje" : "Usuario y reservar eliminado con exito."}),200

    # Manejo de errores.
    except sqlite3.IntegrityError:
        return jsonify({"error" : "Error de integridad al eliminar los datos.."}),400
    except Exception as error:
        return jsonify({"error" : f"Se detecto un error inesperado : {str(error)}"}),400
    finally:
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
                JOIN reservas ON usuarios.user_id = reservas.user_id
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