from http.server import HTTPServer, SimpleHTTPRequestHandler
from jinja2 import Environment, FileSystemLoader, select_autoescape
import json
import urllib

file_loader = FileSystemLoader('templates')
environment = Environment(loader=file_loader)


class MyRequestHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed_path.query)
        path = parsed_path.path

        with open('templates/source/json/advantages.json', 'rb') as file:
            data = json.load(file)
            
        if path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            template = environment.get_template('about.html')
            output = template.render(advantages=data['advantages'])
            self.wfile.write(output.encode('utf-8'))

        elif path == '/production' or path == f'/production?{query}':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            products = data['production']
            filtered_data = []
            for product in products:
                if product.get('category') == query.get('product', [''])[0]:
                    filtered_data.append(product)
            template = environment.get_template('production.html')
            if filtered_data != []:
                output = template.render(production=filtered_data)
            else:
                output = template.render(production=data['production'])
            self.wfile.write(output.encode('utf-8'))

        elif path == '/delivery':   
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()     
            template = environment.get_template('delivery.html')
            output = template.render()
            self.wfile.write(output.encode('utf-8'))

        elif path == '/vacancies':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            template = environment.get_template('vacancies.html')
            output = template.render(vacancies=data['vacancies'])
            self.wfile.write(output.encode('utf-8'))

        elif path.endswith('.css'):
            self.send_response(200)
            self.send_header('Content-type', 'text/css')
            self.end_headers()
            with open(path.replace('/', '', 1), 'rb') as file:
                self.wfile.write(file.read())

        elif path.endswith('.png'):
            self.send_response(200)
            self.send_header('Content-type', 'image/png')
            self.end_headers()
            with open(path.replace('/', '', 1), 'rb') as file:
                self.wfile.write(file.read())

        else:
            self.send_response(404)

    def do_POST(self):
        content_length =int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        parsed_data = urllib.parse.parse_qs(post_data.decode('utf-8'))

        with open('form_data.txt', 'a') as file:
            for key, value in parsed_data.items():
                file.write(f'{key}: {value}\n')
            file.write('\n')
        
        self.send_response(200)
        self.end_headers()
        self.wfile.write(environment.get_template('server_answer.html').render().encode('utf-8'))

def run(server_class=HTTPServer, handler_class=MyRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == "__main__":
    run()