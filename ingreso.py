from flask import Flask, render_template, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
DB_CONFIG = {
    'host': 'http://localhost/phpmyadmin/index.php?route=/database/structure&db=usuarios-registro', # O la IP de tu servidor de base de datos
    'user': 'root',      # Tu usuario de MySQL (cambia si usas otro)
    'password': '',      # Tu contraseña de MySQL (cambia si tienes una)
    'database': 'usuarios-registro' # Asegúrate de que este sea el nombre correcto de tu DB
}

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return None

@app.route('/')
def index():
    """Renderiza el archivo HTML principal."""
    return render_template('index.html')

@app.route('/usuarios', methods=['GET'])
def get_usuarios():
    """Obtiene y devuelve la lista de usuarios desde la base de datos."""
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor(dictionary=True) # dictionary=True para obtener resultados como diccionarios
    try:
        # Asegúrate de que el nombre de la tabla sea 'usuarios_registro' si tiene un guion
        # MySQL/MariaDB a veces tiene problemas con guiones en nombres de tabla sin comillas.
        # Es más seguro usar guiones bajos o camelCase. Si 'usuarios-registro' falla, prueba 'usuarios_registro'.
        cursor.execute("SELECT id, nombre, apellido, cedula FROM `usuarios-registro`")
        usuarios = cursor.fetchall()
        return jsonify(usuarios)
    except mysql.connector.Error as err:
        return jsonify({"error": f"Error al ejecutar la consulta: {err}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

@app.route('/agregar_usuario', methods=['POST'])
def add_usuario():
    """Agrega un nuevo usuario a la base de datos."""
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido') # Nuevo campo
    cedula = data.get('cedula')     # Nuevo campo

    # Validación: Asegúrate de que todos los campos requeridos estén presentes
    if not nombre or not apellido or not cedula:
        return jsonify({"error": "Nombre, apellido y cédula son requeridos"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "No se pudo conectar a la base de datos"}), 500

    cursor = conn.cursor()
    try:
        # Consulta SQL actualizada para insertar nombre, apellido y cedula
        sql = "INSERT INTO `usuarios-registro` (nombre, apellido, cedula) VALUES (%s, %s, %s)"
        val = (nombre, apellido, cedula) # Valores en el orden correcto
        cursor.execute(sql, val)
        conn.commit()
        return jsonify({"message": "Usuario agregado exitosamente", "id": cursor.lastrowid}), 201
    except mysql.connector.Error as err:
        conn.rollback() # Deshacer la operación en caso de error
        return jsonify({"error": f"Error al agregar usuario: {err}"}), 500
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == '__main__':
    app.run(debug=True) # debug=True es para desarrollo; desactívalo en producción