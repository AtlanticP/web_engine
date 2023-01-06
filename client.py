from socket import socket
from hinting import GenType
from log import logger
from urls import URLS


def parse_request(request: str) -> tuple[str, str] | None:
    parsed = request.split(' ')

    try:
        method = parsed[0]
        url = parsed[1]
    except IndexError:
        return None, None                     # !!!!!!!!!!!!!!! telnet localhost 5000

    return method, url

def generate_headers(method: str, url: str) -> tuple[int, str]:

    header = "HTTP/1.1 "

    if not method == 'GET':
        code = 405
        header += f' {code} Method not allowed'

    elif not url in URLS:
        # return response(404, 'Not found')
        code = 404
        header += f' {code} Not found'

    elif method is None:
        code = 400
        header += f' {code} Bad request'

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
    elif code == 200:
        content = get_content(f'<h1>{URLS[url]}</h1>')
    else:
        content = get_content(f'<h1>{400}</h1> Bad request')
            
    return content
        
def generate_response(request: str) -> bytes:
    method, url = parse_request(request)     # type: ignore
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

