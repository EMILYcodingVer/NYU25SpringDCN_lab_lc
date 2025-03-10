from flask import Flask, request, jsonify
import socket
import json
import struct

app = Flask(__name__)

@app.route('/register', methods=['PUT'])
def register():
    data = request.get_json()
    hostname = data.get('hostname')
    ip = data.get('ip')
    as_ip = data.get('as_ip')
    as_port = data.get('as_port')

    if not (hostname and ip and as_ip and as_port):
        return "Bad Request: Missing parameters", 400

    # Send registration request to AS via UDP
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
    udp_socket.sendto(message.encode(), (as_ip, int(as_port)))
    udp_socket.close()

    return "Registration Successful", 201

@app.route('/fibonacci', methods=['GET'])
def fibonacci():
    number = request.args.get('number')

    if not number:
        return "Bad Request: Missing number", 400

    try:
        number = int(number)
    except ValueError:
        return "Bad Request: Invalid number format", 400

    fib_number = fibonacci_number(number)
    return jsonify({"fibonacci": fib_number}), 200

def fibonacci_number(n):
    if n <= 1:
        return n
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9090)