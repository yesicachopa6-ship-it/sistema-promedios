import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

# 1. FUNCIÓN PARA CONECTAR A LA BASE DE DATOS
def obtener_conexion():
    url = os.environ.get('DATABASE_URL')
    return psycopg2.connect(url)

# 2. FUNCIÓN PARA CREAR LA TABLA AUTOMÁTICAMENTE
def inicializar_base_de_datos():
    try:
        conn = obtener_conexion()
        cur = conn.cursor()
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
        print(f"Error al inicializar base de datos: {e}")

# Llamamos a la creación de la tabla apenas arranca el servidor
inicializar_base_de_datos()

# 3. RUTA PRINCIPAL (CARGA EL FORMULARIO)
@app.route('/')
def indice():
    return render_template('index.html')

# 4. RUTA PARA CALCULAR Y GUARDAR
@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        # Obtenemos el nombre. Si está vacío, ponemos "Aspirante" para evitar errores.
        nombre = request.form.get('nombre')
        if not nombre:
            nombre = "Aspirante"
            
        # Obtenemos las notas y las convertimos a número
        n1 = float(request.form.get('nota1') or 0)
        n2 = float(request.form.get('nota2') or 0)
        n3 = float(request.form.get('nota3') or 0)
        n4 = float(request.form.get('nota4') or 0)
        
        promedio = (n1 + n2 + n3 + n4) / 4

        # Guardamos en Postgres
        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO registro_notas (nombre_aspirante, nota1, nota2, nota3, nota4, promedio)
            VALUES (%s, %s, %s, %s, %s, %s)
        ''', (nombre, n1, n2, n3, n4, promedio))
        conn.commit()
        cur.close()
        conn.close()

        # Respuesta visual rápida
        return f"""
        <div style="font-family: sans-serif; text-align: center; margin-top: 50px;">
            <h1>Resultado para {nombre}</h1>
            <p style="font-size: 24px;">El promedio es: <strong>{promedio:.2f}</strong></p>
            <p style="color: green;"> Guardado correctamente en la base de datos.</p>
            <br>
            <a href="/" style="text-decoration: none; background: #007bff; color: white; padding: 10px 20px; border-radius: 5px;">Calcular otro</a>
        </div>
        """
    except Exception as e:
        return f"<h1>Error al procesar:</h1><p>{str(e)}</p><a href='/'>Volver a intentar</a>"

if __name__ == '__main__':
    # Usar el puerto que nos da Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
