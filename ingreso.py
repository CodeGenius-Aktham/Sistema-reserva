from flask import Flask, request, jsonify # Importacion de la libreria Flask
from datetime import datetime # Importacion de la libreria datetime para manejo de fechas y horas.
import sqlite3 # Importacion de la libreria SQLite3 para manejo de la base de datos.


# Identificador de la aplicacion.
app = Flask(__name__)

# Conexion a la base de datos de usuario y reservas.
def conexion_db():
    conn = sqlite3.connect(r"C:\Users\POWER\reservas_fp.db") # Conexion en la base de datos
    conn.row_factory = sqlite3.Row 
    return conn

# Ingreso y enrutador del registro.
@app.route('/register', methods = ['POST'])
def registro_usuario():
        # Convierte la informacion en un archivo Json.
        data = request.get_json()

        # Ingreso de datos solicitados.
        nombre_usuario = data.get('nombre','').strip()
        apellido_usuario =  data.get('apellido','').strip()
        cedula_usuario = data.get('cedula','').strip()

        # Validador de campos ingresados.
        if not all([nombre_usuario,apellido_usuario,cedula_usuario]):
            return jsonify({"error" : "todos los campos deben estar completos."}),400

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
            return jsonify({"mensaje" : "usuario ingresado con exito."}),200
        # Manejo de errores por si la cedula se repite.
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: usuarios.cedula_usuario" in str(error):
                return jsonify({"error" : "La cedula ya esta registrada"}),400
            return jsonify({"error" : "error de integridad"}),400
        # Si se presenta un error en el programa se marca en el manejo de errores.
        except Exception as error:
            return jsonify({"error" : f"error inesperado en el programa : {str(error)}."}),500
        finally:
            conn.close() # Se cierra la base de datos.


# Ingresp y enrutador de las reservas.
@app.route('/reservation', methods = ['POST'])
def registro_reserva():
        # Convierte la informacion en un archivo Json.
        data = request.get_json()

        # Ingreso de datos soliciatados.
        fecha_reserva = data.get('fecha','').strip()
        hora_reserva = data.get('hora','').strip()
        hora_termino = data.get('termino','').strip()
        estado_reserva = data.get('estado','').strip()

        # Validador de campos ingresados.
        if not all([fecha_reserva,hora_reserva,hora_termino,estado_reserva]):
            return jsonify({"error" : "todos los campos deben estar completos."}),400
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
            return jsonify({"mensaje" : "reserva ingresada con exito."}),200
        # Manejo de errores por si las fechas de reserva y la hora de la reserva de la cancha son las mismas-
        except sqlite3.IntegrityError as error:
            if "UNIQUE constraint failed: reservas.fecha_reserva, reservas.hora_reserva" in str(error):
                return jsonify({"error" : "Ya existe una reserva para esa fecha y hora."}),400
            return jsonify({"error" : "error de integridad"}),400
        # Si se presenta un error en el programa se marca en el manejo de errores.
        except Exception as error:
            return jsonify({"error" : f"error inesperado en el programa : {str(error)}"}),500
        finally:
            conn.close() # Se cierra la base de datos.