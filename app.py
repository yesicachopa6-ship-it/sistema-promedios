import os
from flask import Flask, render_template, request
import psycopg2

# ESTA LÍNEA ES LA QUE ESTABA MAL:
app = Flask(__name__)

def obtener_conexion():
    return psycopg2.connect(os.environ.get('DATABASE_URL'))

@app.route('/')
def inicio():
    return render_template('index.html')

@app.route('/calcular', methods=['POST'])
def calcular():
    try:
        nombre = request.form.get('nombre') or "Aspirante"
        n1 = float(request.form.get('nota1') or 0)
        n2 = float(request.form.get('nota2') or 0)
        n3 = float(request.form.get('nota3') or 0)
        n4 = float(request.form.get('nota4') or 0)
        promedio = (n1 + n2 + n3 + n4) / 4

        conn = obtener_conexion()
        cur = conn.cursor()
        cur.execute("INSERT INTO registro_notas (nombre_aspirante, nota1, nota2, nota3, nota4, promedio) VALUES (%s, %s, %s, %s, %s, %s)",
                    (nombre, n1, n2, n3, n4, promedio))
        conn.commit()
        cur.close()
        conn.close()

        return f"<h1>Resultado para {nombre}</h1><p>Promedio: {promedio:.2f}</p><a href='/'>Volver</a>"
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
