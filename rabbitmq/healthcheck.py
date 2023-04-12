import subprocess
import random

def get_random_online_node(node_list, timeout=2):
    online_nodes = []
    offline_nodes = []

    for node in node_list:
        try:
            response = subprocess.run(['ping', '-c', '1', '-W', str(timeout), node], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if response.returncode == 0:
                online_nodes.append(node)
                print(f"Node {node} is up.")
            else:
                offline_nodes.append(node)
                print(f"Node {node} is down.")
        except Exception as e:
            offline_nodes.append(node)
            print(f"Error pinging node {node}: {e}")

    if online_nodes:
        random_online_node = random.choice(online_nodes)
        return random_online_node
    else:
        print("No online nodes found.")
        return None

# List of node IP addresses
node_list = [
    '172.30.0.140',
    '172.30.1.201',
    '172.31.15.87'
]

# Get a random online node
random_online_node = get_random_online_node(node_list)
if random_online_node is not None:
    print("Random online node:", random_online_node)
