import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import sqlite3
import json
from wsgiref.simple_server import make_server

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

def application(environ, start_response):
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    
    if method == 'POST' and path == '/login':
        try:
            content_length = int(environ.get('CONTENT_LENGTH', 0))
            request_body = environ['wsgi.input'].read(content_length).decode('utf-8')
            data = json.loads(request_body)
            
            success = DatabaseHandler.check_user(data.get('email'), data.get('password'))
            
            response = json.dumps({'success': success}).encode('utf-8')
            
            start_response('200 OK', [
                ('Content-Type', 'application/json'),
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Length', str(len(response)))
            ])
            return [response]
            
        except Exception as e:
            response = json.dumps({'success': False, 'error': str(e)}).encode('utf-8')
            start_response('500 Internal Server Error', [
                ('Content-Type', 'application/json'),
                ('Access-Control-Allow-Origin', '*'),
                ('Content-Length', str(len(response)))
            ])
            return [response]
    
    elif method == 'OPTIONS':
        start_response('200 OK', [
            ('Access-Control-Allow-Origin', '*'),
            ('Access-Control-Allow-Methods', 'POST, OPTIONS'),
            ('Access-Control-Allow-Headers', 'Content-Type'),
            ('Content-Length', '0')
        ])
        return []
    
    else:
        response = b'Not Found'
        start_response('404 Not Found', [
            ('Content-Type', 'text/plain'),
            ('Content-Length', str(len(response)))
        ])
        return [response]

app = application

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    with make_server('', port, app) as httpd:
        print(f'Serving on port {port}...')
        httpd.serve_forever()