from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    users = []
    def do_POST(self):
        got = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        data = got['data']
        match got['type']:
            case 'login':
                for user in self.users:
                    if (data['email'] == user['email']):
                        if (data['password'] == user['password']):
                            response = user['token']
                            break
                        else:
                            response = '密碼錯誤'
                            break
                else:
                    response = '未曾註冊'
            case 'signup':
                data['token'] = str(len(self.users))
                self.users.append(data)
                response = str(self.users)
        self.send_response(200)
        self.end_headers()
        self.wfile.write(response.encode())

HTTPServer(('', 8000), MyHTTPRequestHandler).serve_forever()