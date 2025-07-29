from flask import Blueprint, request, jsonify # Importacion de la libreria Flask.
from reservas.backend.data import conexion # Importamos el modulo de la conexion con la base de datos.
import psycopg2 # Importacion de la libreria que maneja la base de datos.
import datetime # Importacion de la libreria 'datetime' para usarña en la conversion a str.

boss_admin = Blueprint('panel_boss',__name__)

def conexion_db():
    return conexion.conexion_db()


# Ingreso y enrutador para eliminacion de usuarios.
@boss_admin.route('/delete', methods = ["POST"])
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
        cursor.execute('''SELECT * FROM usuarios WHERE user_id = %s''',(eliminar_usuario,))
        if cursor.fetchone() is None:
            return jsonify({"error" : "Usuario no encontrado."}),400
        # Eliminacion de datos tanto en la reserva como en la tabla de registro.
        cursor.execute('''DELETE FROM reservas WHERE user_id = %s''',(eliminar_usuario,))
        cursor.execute('''DELETE FROM usuarios WHERE user_id = %s''', (eliminar_usuario,))
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
@boss_admin.route('/show', methods = ["GET"])
def visualizar_datos():
    conn = conexion_db() # Recibe la conexion con la base de datos.
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos."}), 500
    
    try:
        cursor = conn.cursor()
        # Lector de la query en SQL
        cursor.execute('''
                SELECT
                    usuarios.user_id,
                    usuarios.nombre_usuario,
                    usuarios.apellido_usuario,
                    usuarios.cedula_usuario,
                    reservas.fecha_reserva,
                    reservas.hora_inicio,
                    reservas.hora_termino,
                    reservas.estado_reserva
                FROM usuarios
                JOIN reservas ON usuarios.user_id = reservas.user_id
                ORDER BY reservas.fecha_reserva DESC;
                ''',conn)
        reservas = cursor.fetchall()
        nombres_columnas = ["user_id", "nombre_usuario", "apellido_usuario", "cedula_usuario",
            "fecha_reserva", "hora_reserva", "hora_termino", "estado_reserva", "reserva_id"]
        reservas_list = []
        for row in reservas:
            reservas_dict = dict(zip(nombres_columnas,row))
            if 'fecha_reserva' in reservas_dict:
                reservas_dict['fecha_reserva'] = str(reservas_dict['fecha_reserva'])
            if 'hora_reserva' in reservas_dict:
                reservas_dict['hora_reserva'] = str(reservas_dict["hora_reserva"])
            if 'hora_termino' in reservas_dict:
                reservas_dict['hora_termino'] = str(reservas_dict["hora_termino"])
        reservas_list.append(reservas_dict),200
        return jsonify({"resultado" : reservas_dict}),200
    # Manejo de errores.
    except Exception as error:
        return jsonify({"resultado" : [], "error" : f"error inesperado en el programa : {str(error)}"})
    finally:
        conn.close() # Cierre de la base de datos.