import json
import os
import time
import psycopg2
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Type
 
DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_PORT = int(os.environ.get('DB_PORT', 5432))
DB_NAME = os.environ.get('DB_NAME', 'mydatabase')
DB_USER = os.environ.get('DB_USER', 'myuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mypassword')
 
 
def connect_to_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                port=DB_PORT,
                dbname=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            print("Połączono z bazą danych")
            return conn
        except psycopg2.OperationalError:
            print("Błąd połączenia z bazą danych, ponawianie za 5 sekund...")
            time.sleep(5)
 
conn = connect_to_db()
cursor = conn.cursor()
 
class SimpleRequestHandler(BaseHTTPRequestHandler):
 
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
 
        cursor.execute("SELECT * FROM users;")
        users = cursor.fetchall()
       
        response = [{
            'id': user[0],
            'first_name': user[1],
            'last_name': user[2],
            'role': user[3]
        } for user in users]
 
        self.wfile.write(json.dumps(response).encode())
 
    def do_POST(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())
 
        cursor.execute("INSERT INTO users (first_name, last_name, role) VALUES (%s, %s, %s) RETURNING id;",
                       (received_data['first_name'], received_data['last_name'], received_data['role']))
        user_id = cursor.fetchone()[0]
        conn.commit()
 
        response = {
            "id": user_id,
            "first_name": received_data['first_name'],
            "last_name": received_data['last_name'],
            "role": received_data['role']
        }
 
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
 
        self.wfile.write(json.dumps(response).encode())
 
    def do_DELETE(self) -> None:
        content_length: int = int(self.headers['Content-Length'])
        post_data: bytes = self.rfile.read(content_length)
        received_data: dict = json.loads(post_data.decode())
 
        user_id = received_data.get('id')
        cursor.execute("DELETE FROM users WHERE id = %s RETURNING id;", (user_id,))
        deleted_user = cursor.fetchone()
 
        if deleted_user:
            conn.commit()
            response = {"message": f"User with id {user_id} has been deleted."}
            self.send_response(200)
        else:
            response = {"error": "User not found"}
            self.send_response(404)
 
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
 
        self.wfile.write(json.dumps(response).encode())
 
 
def run(server_class: Type[HTTPServer] = HTTPServer, handler_class: Type[BaseHTTPRequestHandler] = SimpleRequestHandler, port: int = 8000) -> None:
    server_address: tuple = ('', port)
    httpd: HTTPServer = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    httpd.serve_forever()
 
 
if __name__ == '__main__':
    run()