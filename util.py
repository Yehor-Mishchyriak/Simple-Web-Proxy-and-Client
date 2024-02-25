# YEHOR MISHCHYRIAK
from socket import socket, timeout, AF_INET, SOCK_STREAM

'''
The file contains utility functions for the following purposes:
    1) Parsing URLs to extract host and pages.
    2) Formatting HTTP requests based on a host and pages.
    3) Creating a listening socket bound to a specified host and port.
    4) Creating a connection socket to connect to a specified host and port.
    5) Sending data over a socket.
    6) Receiving data from a socket.
'''

# ========================================
# Helper functions for http requests
# ========================================

def parse_url(url: str) -> tuple:
    """
    Parse the URL string and extract the host and pages.
    
    Args:
        url (str): The URL to parse.
        
    Returns:
        tuple: A tuple containing the host and pages.
        or
        None in case of the inability to parse the url.
    """
    try:
        if url[-1] != '/':
            url += '/'
        start = url.index("//") + 2
        to_host = url.index('/', start)
        host = url[start:to_host]
        pages = url[to_host:]
    except ValueError as e:
        print("ERROR: Invalid URL format: ", e)
        return None
    except TypeError as e:
        print("ERROR: Invalid URL type: ", e)
        return None
    except Exception as e:
        print("An unexpected error has occurred: ", e)
        return None

    return host, pages

def format_httprequest(host: str, pages: str) -> str:
    """
    Format an HTTP request string.
    
    Args:
        host (str): The host to request from.
        pages (str): The pages to request.
        
    Returns:
        str: The formatted HTTP request string.
    """
    return f"GET {pages} HTTP/1.1\r\nHOST: {host}\r\n\r\n"

# ========================================
# Helper functions for socket operations
# ========================================

def listening_socket(socket_host, socket_port, socket_backlog) -> socket:
    """
    Create a listening socket.
    
    Args:
        socket_host (str): The host to bind the socket to.
        socket_port (int): The port to listen on.
        socket_backlog (int): The maximum number of queued connections.
        
    Returns:
        socket: The listening socket.
        or
        None in case the attempt to open the socket failed.
    """
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.bind((socket_host, socket_port))
        sock.listen(socket_backlog)
    except OSError as e:
        print("Couldn't open a listening socket: ", e)
        if sock:
            sock.close()
            return None
    except TypeError as e:
        print("Couldn't open a listening socket: ", e)
        if sock:
            sock.close()
            return None
    except Exception as e:
        print("An unexpected error has occurred: ", e)
        if sock:
            sock.close()
            return None

    return sock

def connection_socket(host, port) -> socket:
    """
    Create a connection socket.
    
    Args:
        host: The host to connect to.
        port: The port to connect to.
        
    Returns:
        socket: The connection socket.
        or
        None in case the connection attempt failed
    """
    try:
        sock = socket(AF_INET, SOCK_STREAM)
        sock.connect((host, port))
    except OSError as e:
        print(f"Couldn't connect to {host}: ", e)
        if sock:
            sock.close()
            return None
    except TypeError as e:
        print(f"Couldn't connect to {host}: ", e)
        if sock:
            sock.close()
            return None
    except Exception as e:
        print("An unexpected error has occurred: ", e)
        if sock:
            sock.close()
            return None

    return sock

def send_all(content: str, sock: socket) -> None:
    """
    Send all data over the socket.
    
    Args:
        content (str): The data to send.
        sock (socket): The socket to send data over.
    """
    try:
        bcontent = content.encode("utf-8")
    except AttributeError:
        # the data is already in binary and doesn't need to be encoded
        bcontent = content
    except TypeError as e:
        print(f"ERROR: {content} is not of UTF-8 format and cannot be converted into binary: ", e)
        bcontent = b''
    except Exception as e:
        print("An unexpected error has occurred: ", e)
        bcontent = b''

    sock.sendall(bcontent)

def receive_all(sock: socket, decode=False, wait_time=None):
    """
    Receive all data from a socket.
    
    Args:
        sock (socket): The socket to receive data from.
        decode (bool): Whether to decode the received data (default is False).
        wait_time (int): The timeout for receiving data (default is 1).
        
    Returns:
        str or bytes: The received data.
    """
    old_wait_time = sock.gettimeout()
    sock.settimeout(wait_time)

    bin_response = b""
    while True:
        try:
            parsed_chunk = sock.recv(1024)
            if parsed_chunk == b"":
                raise timeout
            bin_response += parsed_chunk
        except timeout:
            break
        except OSError as e:
            sock.settimeout(old_wait_time)
            print(f"ERROR: Unable to receive data from {sock}: ", e)
            return "" if decode else b""
        except Exception as e:
            sock.settimeout(old_wait_time)
            print("An unexpected error has occurred: ", e)
            return "" if decode else b""
    sock.settimeout(old_wait_time)

    if decode:
        try:
            response = bin_response.decode("utf-8")
            return response
        except UnicodeDecodeError as e:
            print("ERROR: Unable to decode the received data: ", e)
            return "" if decode else b""
        except Exception as e:
            print("An unexpected error has occurred: ", e)
            return "" if decode else b""
    else:
        return bin_response


if __name__ == "main":
    pass
