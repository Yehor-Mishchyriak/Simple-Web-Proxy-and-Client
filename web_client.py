#!/usr/bin/python3
# YEHOR MISHCHYRIAK
# Wesleyan University
# COMP 332
# Homework 3: Simple web client to interact with proxy

# Usage:
# python3 web_client.py <proxy_host> <proxy_port> <requested_url>

# utility functions
import util
# Python modules
import sys

'''
- WebClient class:
    1) Initializes with the proxy host, proxy port, and the URL to request.
    2) Provides a method start to initiate the interaction with the proxy server.
    3) Connects to the proxy server using the provided host and port.
    4) Sends the requested URL to the proxy server and waits to receive the webpage content.
    5) Prints the received webpage content to the console.
- main function:
    1) Sets up default values for the proxy host, proxy port, and URL.
    2) Parses command-line arguments to override default values if provided.
    3) Creates an instance of the WebClient class with the specified parameters and starts the interaction with the proxy server.
'''

class WebClient:

    def __init__(self, proxy_host, proxy_port, url):
        self.proxy_host = proxy_host
        self.proxy_port = proxy_port
        self.url = url

    def start(self):

        # Connect to the proxy
        proxy_sock = util.connection_socket(self.proxy_host, self.proxy_port)

        # request the url, and then receive it (provided the proxy was able to get the page)
        util.send_all(self.url, proxy_sock)
        web_page = util.receive_all(proxy_sock, decode=True, wait_time=5)

        print("====================")
        print("The received webpage:")
        print(f"====================\n{web_page}")

        proxy_sock.close()


def main():

    '''
    URLs:
    - 'http://example.com/'
    - 'http://eu.httpbin.org'
    - 'http://info.cern.ch/'
    - 'http://www-db.deis.unibo.it/'
    - 'http://info.cern.ch/hypertext/WWW/TheProject.html'
    '''

    proxy_host = 'localhost'
    proxy_port = 50015
    url = 'http://example.com/'
    if len(sys.argv) > 1:
        proxy_host = sys.argv[1]
        proxy_port = int(sys.argv[2])
        url = sys.argv[3]

    web_client = WebClient(proxy_host, proxy_port, url)
    web_client.start()

if __name__ == "__main__":
    main()
