import subprocess
import random
import socket

def is_rabbitmq_running(ip, ports=(5672, 15672), timeout=5):
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            try:
                s.connect((ip, port))
                print(f"RabbitMQ service is running on {ip}:{port}")
                return True
            except (socket.timeout, ConnectionRefusedError):
                print(f"RabbitMQ service is not running on {ip}:{port}")
                return False

def get_random_online_node():
    timeout=2

    online_nodes = []
    offline_nodes = []

    # List of node IP addresses
    node_list = [
        '172.30.0.140',
        '172.30.0.177',
        '172.30.1.201',
        '10.0.0.203',
        '172.31.15.87'
    ]

    for node in node_list:
        try:
            response = subprocess.run(['ping', '-c', '1', '-W', str(timeout), node], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if response.returncode == 0:
                print(f"Node {node} is GOOD.")
                if is_rabbitmq_running(node):
                    online_nodes.append(node)
                else:
                    offline_nodes.append(node)
            else:
                print(f"Node {node} is BAD.")
                offline_nodes.append(node)
        except Exception as e:
            offline_nodes.append(node)
            print(f"Error pinging node {node}: {e}")

    print("Good Nodes: ------------------")
    print(online_nodes)
    print("Bad Nodes: ------------------")
    print(offline_nodes)

    if online_nodes:
        random_online_node = random.choice(online_nodes)
        return random_online_node
    else:
        print("No online nodes found.")
        return None

ip_addr = get_random_online_node()
print("Your IP Address")
print("------------------")
print(ip_addr)
