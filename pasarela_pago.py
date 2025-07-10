from flask import Flask,request,jsonify
from flask_cors import CORS
from psycopg2 import IntegrityError
from dotenv import load_dotenv
import hashlib, hmac
import psycopg2
import os


app = Flask(__name__)
CORS(app, origins="https://codegenius-aktham.github.io", supports_credentials=True)

load_dotenv()

def conexion_db():
    try:
        conn = psycopg2.connect (
            host = os.getenv('DB_HOST'),
            dbname = os.getenv('DB_NAME'),
            user = os.getenv('DB_USER'),
            password = os.getenv('DB_PASSWORD'),
            port = os.getenv('DB_PORT'),
            sslmode = os.getenv('DB_SSL')
        )
        return conn
    except Exception as error:
        print(f"Error con la conexion de la base de datos : {error}")
        return
    except IntegrityError as error:
        conn.rollback()
        return jsonify({'error' : f'error de integridad en la base de datos : {str(error)}.'}),400


@app.route('/consultation', methods = ['GET'])
def pagos_canchas():
    data = request.get_json()
    transaccion_id = data.get('transaction_id')
    if not transaccion_id:
        return jsonify({'error' : 'falta el id del usuario'}),400
    url_pruebas = f'https://sandbox.wompi.co/v1/transactions/{transaccion_id}'
    headers = {"Authorization": f"Bearer {os.getenv('API_KEY')}"}
    try:
        respuesta = request.get(url_pruebas,headers=headers)
        peticion_json = respuesta.json()
        transaccion_id = peticion_json['data']['id']
        status = peticion_json['data']['status']
        payment = peticion_json['data']['payment_method_type']
        amount = peticion_json['data']['amount_in_cents']
        reference = peticion_json['data']['refence']

        return jsonify({
            'id' : transaccion_id,
            'status' : status,
            'payment' : payment,
            'amount' : amount,
            'reference' : reference
        })
    
    except Exception as error:
        return jsonify({'error' : f'error en el pago de la reserva : {str(error)}'}),400


@app.route('/webhook-wompi', methods = ['POST'])
def recibir_webhook():
    data = request.data
    conn = conexion_db()
    if conn is None:
        return jsonify({'error' : 'no se puede conectar con la base de datos.'}),400
    try:
        encode = os.getenv('API_KEY').encode('utf-8')
        firma_local = hmac.new(encode,data, hashlib.sha256).hexdigest()
        firma_wompi = request.headers.get('X-Checksum-SHA256')
        if firma_local == firma_wompi:
            cursor = conn.cursor()
            payload = request.get_json()
            reference = payload.get("data", {}).get("reference")
            status = payload.get("data", {}).get('status')
            cursor.execute('''UPDATE reservas SET estado_reserva = %s WHERE referencia = %s ''',(status,reference))
            conn.commit()
            return jsonify({'mensaje' : 'estado de la reserva actualizado'}),200
        else:
            return jsonify({'error': 'Firma inválida'}), 403
    except Exception as error:
        return jsonify({'error' : f'error en el pago de la reserva : {str(error)}'}),400
    finally:
        cursor.close()
        conn.close()
