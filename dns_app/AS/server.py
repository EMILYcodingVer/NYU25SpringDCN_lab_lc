import socket
import os

# Persistent storage (simulated by a file)
DNS_RECORD_FILE = 'dns_records.txt'

def register_dns_record(hostname, ip):
    with open(DNS_RECORD_FILE, 'a') as f:
        f.write(f"{hostname} {ip}\n")

def resolve_dns_query(hostname):
    with open(DNS_RECORD_FILE, 'r') as f:
        for line in f:
            registered_hostname, ip = line.strip().split()
            if registered_hostname == hostname:
                return ip
    return None

def handle_registration_request(data, addr):
    hostname = data.get('NAME')
    ip = data.get('VALUE')
    if hostname and ip:
        register_dns_record(hostname, ip)
        return "Registration Successful"
    return "Invalid Registration Request"

def handle_dns_query(data, addr):
    hostname = data.get('NAME')
    ip = resolve_dns_query(hostname)
    if ip:
        response = f"TYPE=A\nNAME={hostname}\nVALUE={ip}\nTTL=10\n"
        return response
    else:
        return "Host not found"

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('0.0.0.0', 53533))

    print("Authoritative Server listening on port 53533...")
    while True:
        data, addr = server_socket.recvfrom(1024)
        print(f"Received data: {data.decode()}")  # 这个地方打印接收到的数据
        data = data.decode().strip().split('\n')
        data_dict = {item.split('=')[0]: item.split('=')[1] for item in data}

        if "NAME" in data_dict:
            if "VALUE" in data_dict:
                response = handle_registration_request(data_dict, addr)
            else:
                response = handle_dns_query(data_dict, addr)

            server_socket.sendto(response.encode(), addr)

if __name__ == '__main__':
    start_server()
