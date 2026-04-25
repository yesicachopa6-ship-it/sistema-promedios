import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def obtener_conexion():
    # Esto usa la variable que pegaste en Render automáticamente
    url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(url)

def inicializar_base_de_datos():
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
        # Esto crea la tabla si no existe
        cur.execute('''
            CREATE TABLE IF NOT EXISTS registro_notas (
                id SERIAL PRIMARY KEY,
                nombre_aspirante TEXT NOT NULL,
                nota1 FLOAT,
                nota2 FLOAT,
                nota3 FLOAT,
                nota4 FLOAT,
                promedio FLOAT,
                fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        ''')
        conn.commit()
        cur.close()
        conn.close()
        print("Base de datos lista.")
    except Exception as e:
        print(f"Error al inicializar: {e}")

# Ejecutamos la creación al empezar
inicializar_base_de_datos()

@app.route('/')
def indice():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        nombre = request.form.get('nombre')
        n1 = float(request.form.get('nota1', 0))
        n2 = float(request.form.get('nota2', 0))
        n3 = float(request.form.get('nota3', 0))
        n4 = float(request.form.get('nota4', 0))
        
        promedio = (n1 + n2 + n3 + n4) / 4

        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO registro_notas (nombre_aspirante, nota1, nota2, nota3, nota4, promedio)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, n1, n2, n3, n4, promedio))
        conn.commit()
        cur.close()
        conn.close()

        return f"<h1>Promedio de {nombre}: {promedio:.2f}</h1><p>Guardado con éxito.</p><a href='/'>Volver</a>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run()
