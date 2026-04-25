from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hola():
    return "<h1>¡El servidor está funcionando, Chopa!</h1><p>Si leés esto, el problema es el archivo HTML o la carpeta templates.</p>"

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
