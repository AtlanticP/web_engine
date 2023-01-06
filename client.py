from socket import socket
from hinting import GenType
from log import logger
from urls import URLS


def parse_request(request: str) -> tuple[str, str]:
    parsed = request.split(' ')

    method = parsed[0]
    url = parsed[1]

    return method, url

def generate_headers(method: str, url: str) -> tuple[int, str]:

    header = "HTTP/1.1 "

    if not method == 'GET':
        code = 405
        header += f' {code} Method not allowed'

    elif not url in URLS:
        code = 404
        header += f' {code} Not found'

    else:
        code = 200
        header += f' {code} OK'

    return code, header

def generate_content(code: int, url: str) -> str:

    get_content = lambda descr: (f"""
                    Content-Type: text/html

                     <html><body>{descr}</body></html>
                    """)

    if code == 404:
        content = get_content(f'<h1>{code}</h1> Not found')
    elif code == 405:
        content = get_content(f'<h1>{code}</h1> Not allowed')
    else:
        content = get_content(URLS[url]())
            
    return content
        
def generate_response(request: str) -> bytes:
    method, url = parse_request(request)
    code, headers = generate_headers(method, url)
    body = generate_content(code, url)

    return (headers + body).encode()

def client(client_socket: socket) -> GenType:
            
    while True:

        yield ("read", client_socket)

        request = client_socket.recv(4096)
        logger.info("Server received the request")

        if not request:
            break
        else:

            yield ("write", client_socket)

            response = generate_response(request.decode('utf-8'))
            client_socket.sendall(response)

    client_socket.close()

