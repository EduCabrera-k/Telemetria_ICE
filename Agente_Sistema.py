import psutil
import time
import requests
from datetime import datetime

# CONFIGURACIÓN
MI_NOMBRE = input("Tu nombre: ")
# Reemplaza esto con tu URL de Render cuando la tengas
URL_RENDER = "https://tu-proyecto-telemetria.onrender.com/api/reportar"

def correr_agente():
    print(f"🛰️ Agente iniciado. Reportando a {URL_RENDER}...")
    while True:
        try:
            mem = psutil.virtual_memory()
            payload = {
                "nombre": MI_NOMBRE,
                "cpu": psutil.cpu_percent(interval=1),
                "ram": f"{round(mem.used / (1024**3), 2)} / {round(mem.total / (1024**3), 2)} GB",
                "uptime": datetime.now().strftime("%H:%M:%S")
            }
            
            # Enviamos los datos por el puerto 443 (HTTPS) que la uni no bloquea
            res = requests.post(URL_RENDER, json=payload, timeout=5)
            if res.status_code == 200:
                print(f"✅ Métricas enviadas: CPU {payload['cpu']}%")
            
            time.sleep(2)
        except Exception as e:
            print(f"❌ Reintentando conexión... {e}")
            time.sleep(5)

if __name__ == "__main__":
    correr_agente()