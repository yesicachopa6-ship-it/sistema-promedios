import os
from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def inicializar_tabla():
    try:
        # Esto conecta Python con tu base de datos de Render automáticamente
        conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS registro_notas (
                id SERIAL PRIMARY KEY,
                nombre_aspirante TEXT NOT NULL,
                nota1 FLOAT,
                nota2 FLOAT,
                nota3 FLOAT,
                nota4 FLOAT,
                promedio FLOAT
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Tabla lista para usar.")
    except Exception as e:
        print(f"Error al conectar: {e}")

# Ejecutamos la creación de la tabla apenas arranca la web
inicializar_tabla()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    nombre = request.form.get('nombre')
    n1 = float(request.form.get('nota1', 0))
    n2 = float(request.form.get('nota2', 0))
    n3 = float(request.form.get('nota3', 0))
    n4 = float(request.form.get('nota4', 0))
    promedio = (n1 + n2 + n3 + n4) / 4

    # Guardamos en la base de datos
    conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
    cur = conn.cursor()
    cur.execute("INSERT INTO registro_notas (nombre_aspirante, nota1, nota2, nota3, nota4, promedio) VALUES (%s, %s, %s, %s, %s, %s)",
                (nombre, n1, n2, n3, n4, promedio))
    conn.commit()
    cur.close()
    conn.close()

    return f"<h1>Resultado para {nombre}</h1><p>Promedio: {promedio}</p><a href='/'>Volver</a>"

if __name__ == '__main__':
    app.run()
