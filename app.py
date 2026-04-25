import os from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# CONFIGURACIÓN - ¡PON TU CLAVE REAL AQUÍ!
DB_CONFIG = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "CHOPA", 
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Recogemos los datos de la web
        m = [request.form[f'm{i}'] for i in range(1, 4)]
        n = [int(request.form[f'n{i}']) for i in range(1, 10)]

        conn = get_db_connection()
        cur = conn.cursor()
        
        # Llamamos a la función de Postgres
        cur.execute("SELECT * FROM calcular_promedio_materias(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", 
                    (m[0], n[0], n[1], n[2], m[1], n[3], n[4], n[5], m[2], n[6], n[7], n[8]))
        
        resultados = cur.fetchall()
        cur.close()
        conn.close()
        
        return render_template('index.html', resultados=resultados)
    except Exception as e:
        # Esto quita los caracteres que traban a Windows
        error_limpio = str(e).encode('ascii', 'ignore').decode('ascii')
        print(f"DEBUG: {error_limpio}")
        return f"<h1>Error detectado</h1><p>{error_limpio}</p><a href='/'>Volver</a>"

if __name__ == '__main__':
    app.run(debug=True)
