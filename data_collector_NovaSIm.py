from flask import Flask, request, jsonify, render_template
import sqlite3
import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tiempos.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crea la tabla si no existe
def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tiempos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo_entrada TEXT NOT NULL,
            llegada TEXT,
            procesamiento TEXT,
            entrada TEXT
        )
    ''')
    conn.commit()
    conn.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/registrar_tiempo', methods=['POST'])
def registrar_tiempo():
    try:
        data = request.get_json()
        tipo_entrada = data['tipo_entrada']
        tiempo = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        accion = data['accion']

        conn = get_db_connection()
        if accion == 'llegada':
            conn.execute('''
                INSERT INTO tiempos (tipo_entrada, llegada) VALUES (?, ?)
            ''', (tipo_entrada, tiempo))
        elif accion == 'procesamiento':
            conn.execute('''
                UPDATE tiempos SET procesamiento = ? WHERE id = (SELECT MAX(id) FROM tiempos)
            ''', (tiempo,))
        elif accion == 'entrada':
            conn.execute('''
                UPDATE tiempos SET entrada = ? WHERE id = (SELECT MAX(id) FROM tiempos)
            ''', (tiempo,))
        conn.commit()
        conn.close()

        return jsonify({'mensaje': f'Tiempo de {accion} registrado: {tiempo}'}), 201

    except Exception as e:
        return jsonify({'mensaje': f'Error al registrar el tiempo: {str(e)}'}), 500


@app.route('/obtener_tiempos', methods=['GET'])
def obtener_tiempos():
    conn = get_db_connection()
    tiempos = conn.execute('SELECT * FROM tiempos').fetchall()
    conn.close()
    return jsonify([dict(tiempo) for tiempo in tiempos]), 200

if __name__ == '__main__':
    create_table()
    app.run(debug=True)