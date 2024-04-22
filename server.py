from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import uuid

class MyHTTPRequestHandler(BaseHTTPRequestHandler):
    __users = []
    with open('default_news.json') as file:
        __news_list = json.load(file)

    def __make_json(self, type, data):
        return json.dumps({'type': type, 'data': data})

    def __respond(self, text):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(text.encode())

    def do_GET(self):
        match self.path[1:]:
            case 'news':
                text = json.dumps(self.__news_list)
            case 'introduction':
                with open('introduction.json') as file:
                    text = file.read()
            case 'history':
                with open('history.json') as file:
                    text = file.read()
            case 'TEST':
                self.__users.clear()
                with open('default_news.json') as file:
                    self.__news_list = json.load(file)
                text = ''
        self.__respond(text)

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        posted = json.loads(self.rfile.read(length))
        data = posted['data']
        match posted['type']:
            case 'login':
                emails = [i['email'] for i in self.__users]
                try:
                    index = emails.index(data['email'])
                except ValueError:
                    text = self.__make_json('failure', '未曾註冊')
                else:
                    user = self.__users[index]
                    if data['password'] != user['password']:
                        text = self.__make_json('failure', '密碼錯誤')
                    else:
                        text = self.__make_json('success', user['token'])
            case 'signup':
                data['token'] = str(uuid.uuid4())
                self.__users.append(data)
                text = json.dumps(self.__users)
            case 'modification':
                tokens = [i['token'] for i in self.__users]
                index = tokens.index(data['token'])
                self.__users[index] = data
                text = json.dumps(self.__users)
            case 'creating_news':
                data['token'] = str(uuid.uuid4())
                self.__news_list.insert(0, data)
                text = text = self.__make_json('success', data['token'])
            case 'deleting_news':
                tokens = [i['token'] for i in self.__news_list]
                index = tokens.index(data)
                self.__news_list.pop(index)
                text = text = self.__make_json('success', None)
        self.send_response(200)
        self.end_headers()
        self.__respond(text)

HTTPServer(('', 4444), MyHTTPRequestHandler).serve_forever()
