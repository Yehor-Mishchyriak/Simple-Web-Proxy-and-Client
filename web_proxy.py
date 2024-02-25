#!/usr/bin/python3
# YEHOR MISHCHYRIAK
# Wesleyan University
# COMP 332
# Homework 3: Simple multi-threaded web proxy

# Usage:
# python3 web_proxy.py <proxy_host> <proxy_port>

# utility functions
import util
# Python modules
import sys
import threading

'''
- WebProxy class:
    1) Initializes with default proxy host and port values.
    2) Provides a method start to begin the proxy server.
    3) Accepts client connections and handles them in separate threads using the serve_content method.
    4) The serve_content method receives URLs from clients, parses them, makes HTTP requests to remote servers, and forwards the responses back to clients.
- main function:
    1) Sets up the proxy host and port based on command-line arguments or defaults.
    2) Creates an instance of the WebProxy class and starts the proxy server.
'''

class WebProxy():

    def __init__(self, proxy_host, proxy_port):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.proxy_backlog = 1

        self.web_cache = {}

    def start(self):

        # initialize server socket on which to listen for connections
        self.proxy_sock = util.listening_socket(self.proxy_host, self.proxy_port, self.proxy_backlog)
        if not self.proxy_sock:
            print("Failed to run the proxy")
            exit(1)
        print("The proxy is up and running")

        # wait for client connection
        print("Ready to accept clients")
        try:
            while True:
                client_conn, client_addr = self.proxy_sock.accept()
                print('Client with address has connected', client_addr)
                thread = threading.Thread(target = self.serve_content, args = (client_conn, client_addr))
                thread.start()
        # stop the proxy server
        except KeyboardInterrupt:
            print("\nThe proxy has been stopped")
            client_conn.close()
            self.proxy_sock.close()
            exit(0)
        except Exception as e:
            print("\nThe proxy has stopped unexpectedly", e)
            client_conn.close()
            self.proxy_sock.close()
            exit(1)
        
    def serve_content(self, client_conn, client_addr):
        # receive the url from the client; if no url is received, terminate
        requested_url = util.receive_all(client_conn, decode=True, wait_time=1)
        if not requested_url:
            util.send_all('', client_conn)
            print("Couldn't serve the client\n")
            print("Waiting for another client to connect")
            return
        print(f"The client has requested {requested_url}")

        # parse the url to extract the hostname and pages; if the url is invalid, terminate
        host_pages = util.parse_url(requested_url)
        if not host_pages:
            util.send_all('', client_conn)
            print("Couldn't serve the client\n")
            print("Waiting for another client to connect")
            return
        
        # format an http request
        host, pages = host_pages
        formatted_request = util.format_httprequest(host, pages)

        # try to connect to the requested host; if unsuccessful, terminate
        server_sock = util.connection_socket(host, 80)
        if not server_sock:
            util.send_all('', client_conn)
            print("Couldn't serve the client\n")
            print("Waiting for another client to connect")
            return
        print(f"Successfully connected to {host}")

        # send the http request to server; if no response is received, terminate
        util.send_all(formatted_request, server_sock)
        print(f"Requested the webpage")
        response = util.receive_all(server_sock, wait_time=2)
        if not response:
            server_sock.close()
            util.send_all('', client_conn)
            print("Couldn't serve the client\n")
            print("Waiting for another client to connect")
            return

        # send the received server response to the client
        util.send_all(response, client_conn)
        print(f"The webpage has been received and transferred to the {client_addr}")

        server_sock.close()
        print("Successfully served the client\n")
        print("Waiting for another client to connect")
        return


def main():

    proxy_host = 'localhost'
    proxy_port = 50015

    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])

    web_proxy = WebProxy(proxy_host, proxy_port)
    web_proxy.start()

if __name__ == "__main__":
    main()
