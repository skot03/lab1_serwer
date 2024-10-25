import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type



class SimpleRequestHandler(BaseHTTPRequestHandler):

    user_list = [{
        'first_name': 'Pawel',
        'last_name': 'Skotnicki',
        'role': 'Manager'
    }]

    
    def do_OPTIONS(self):
        
        self.send_response(200, "OK")

       
        self.send_header("Access-Control-Allow-Origin", "*")

        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

       
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

        self.end_headers()

   
    def do_GET(self) -> None:
        
        self.send_response(200)

       
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        
        self.end_headers()

        response: list
        response = self.user_list

       
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self) -> None:
        
        content_length: int = int(self.headers['Content-Length'])

        post_data: bytes = self.rfile.read(content_length)

        received_data: dict = json.loads(post_data.decode())

        response: dict = {
            "first_name": received_data['first_name'],
            "last_name": received_data['last_name'],
            "role": received_data['role']
        }

        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        
        self.wfile.write(json.dumps(response).encode())

        self.user_list.append(response)


    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])

        post_data: bytes = self.rfile.read(content_length)

        
        received_data: dict = json.loads(post_data.decode())

        response: dict = {
            "first_name": received_data['first_name'],
            "last_name": received_data['last_name'],
            "role": received_data['role']
        }

       
        self.send_response(200)
        self.send_header('Content-type', 'application/json')

        self.send_header('Access-Control-Allow-Origin', '*')

        self.end_headers()

        
        self.wfile.write(json.dumps(response).encode())

        
        self.user_list.remove(response)

def run(
        server_class: Type[HTTPServer] = HTTPServer,
        handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler,
        port: int = 8000
) -> None:
    
    server_address: tuple = ('', port)

   
    httpd: HTTPServer = server_class(server_address, handler_class)

    
    print(f"Starting HTTP server on port {port}...")

   
    httpd.serve_forever()



if __name__ == '__main__':
    run()

