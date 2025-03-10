from flask import Flask, request, jsonify
import socket
import requests

app = Flask(__name__)

@app.route('/fibonacci', methods=['GET'])
def get_fibonacci():

    hostname = request.args.get('hostname')
    fs_port = request.args.get('fs_port')
    number = request.args.get('number')
    as_ip = request.args.get('as_ip')
    as_port = request.args.get('as_port')


    if not all([hostname, fs_port, number, as_ip, as_port]):
        return jsonify({"error": "Missing parameters"}), 400


    print(f"Requesting Fibonacci number from: http://{hostname}:{fs_port}/fibonacci?number={number}")

    try:

        response = requests.get(f"http://{hostname}:{fs_port}/fibonacci?number={number}")
        
        if response.status_code == 200:
            return jsonify({"fibonacci_number": response.text}), 200
        else:
            return jsonify({"error": "Fibonacci server returned an error"}), response.status_code

    except requests.exceptions.RequestException as e:
        print(f"Error occurred while contacting Fibonacci Server: {e}")
        return jsonify({"error": "Could not contact Fibonacci server"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
