import socket

def is_rabbitmq_running(ip, ports=(5672, 15672), timeout=5):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
                print(f"RabbitMQ service is running on {ip}:{port}")
            except (socket.timeout, ConnectionRefusedError):
                print(f"RabbitMQ service is not running on {ip}:{port}")

# Replace with your RabbitMQ server IP
rabbitmq_server_ip = '172.31.15.87'

is_rabbitmq_running(rabbitmq_server_ip)
