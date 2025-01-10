import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sqlite3
import json

class DatabaseHandler:
    @staticmethod
    def get_db_connection():
        conn = sqlite3.connect('telegram.db')
        conn.row_factory = sqlite3.Row
        return conn

    @staticmethod
    def check_user(email, password):
        conn = DatabaseHandler.get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user is not None

class CustomHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        SimpleHTTPRequestHandler.end_headers(self)

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        if self.path == '/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            success = DatabaseHandler.check_user(data.get('email'), data.get('password'))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = json.dumps({'success': success})
            self.wfile.write(response.encode('utf-8'))
            return

        return super().do_POST()

def run_server():
    port = int(os.environ.get('PORT', 8000))
    server_address = ('', port)
    httpd = HTTPServer(server_address, CustomHandler)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()