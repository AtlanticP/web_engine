from socket import AF_INET     # Address Family IPv4
from socket import SOCK_STREAM    # TCP protocol
from socket import socket, SOL_SOCKET, SO_REUSEADDR 
from select import select
from loguru import logger

from hinting import GenType
from client import client
from log import logger


tasks: list[GenType] = [] 
to_read: dict[socket, GenType] = {}
to_write: dict[socket, GenType] = {}

def server() -> GenType:
    server_socket: socket = socket(AF_INET, SOCK_STREAM)
    server_socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server_socket.bind(("localhost", 5000))
    server_socket.listen()

    logger.info("Server is running...")

    while True:
        yield ("read", server_socket)
        client_socket, _ = server_socket.accept()       # (socket, addres)
        
        tasks.append(client(client_socket))


def event_loop():
    
    while any([tasks, to_read, to_write]):
        
        while not tasks:

            ready_to_read, ready_to_write, _ = select(
                    to_read, to_write, [])

            for sock in ready_to_read:
                task = to_read.pop(sock)
                tasks.append(task)

            for sock in ready_to_write:
                task = to_write.pop(sock)
                tasks.append(task)

        try:
            task = tasks.pop(0)

            sign, sock = next(task)

            if sign == "read":
                to_read[sock] =  task

            if sign == "write":
                logger.info('write ')
                to_write[sock] = task

        except StopIteration:
            pass


if __name__ == "__main__":

    tasks.append(server())
    event_loop()
