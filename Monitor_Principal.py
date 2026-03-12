import eventlet
eventlet.monkey_patch() # Siempre al principio para evitar errores de hilos

import Ice
import os
import threading
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Diccionario global para guardar los datos de los nodos
nodos_activos = {}

# --- RUTA PARA EL DASHBOARD (Página principal) ---
@app.route('/')
def index():
    return render_template('index.html')

# --- RUTA PARA RECIBIR DATOS DEL AGENTE (Salto de Firewall) ---
@app.route('/api/reportar', methods=['POST'])
def reportar_desde_agente():
    global nodos_activos
    data = request.json
    # Guardamos los datos que vienen del Agente_Sistema.py
    nodos_activos[data['nombre']] = {
        "cpu": data['cpu'],
        "ram": data['ram'],
        "uptime": data['uptime'],
        "tipo": "ICE (Vía HTTP)"
    }
    return jsonify({"status": "ok"})

# --- RUTA PARA EL PROFESOR (Cuando entra al link) ---
@app.route('/reportar_web', methods=['POST'])
def reportar_web():
    data = request.json
    nodos_activos[data['nombre']] = {
        "cpu": 0,
        "ram": f"{data['cores']} Cores",
        "uptime": data['plataforma'],
        "tipo": "Web (Profesor)"
    }
    return jsonify({"status": "ok"})

# --- RUTA PARA ACTUALIZAR EL DASHBOARD ---
@app.route('/metrics')
def metrics():
    return jsonify(nodos_activos)

if __name__ == '__main__':
    # Render usa el puerto que le asigne la variable PORT
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)