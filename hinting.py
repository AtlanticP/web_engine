from typing import Generator, Optional
from socket import socket


GenType = Generator[tuple[str, socket], Optional[socket], None]    
