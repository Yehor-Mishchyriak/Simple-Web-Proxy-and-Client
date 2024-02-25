# Simple Web Proxy and Client

This repository contains Python scripts for a simple web proxy server and client, designed to facilitate web page requests through the proxy.

## Repository files:
1. web_client.py
Implements a simple web client to interact with the proxy server.
Connects to the specified proxy server, sends a URL request, and displays the received webpage content.
2. web_proxy.py
Implements a basic web proxy server using threading for concurrency.
Accepts client connections and handles them in separate threads.
Parses client requests, forwards them to remote servers, and returns the responses to clients.
3. util.py
Contains utility functions shared between the proxy server and client scripts.
Includes functions for parsing URLs, formatting HTTP requests, creating sockets, sending and receiving data over sockets, etc.

## Usage
#### Starting the proxy server
```
python3 web_proxy.py [proxy_host] [proxy_port]
```
* Note: 
_proxy_host_ defaults to `local_host` and _proxy_port_ defaults to `50015`
#### Running the web client
```
python3 web_client.py [proxy_host] [proxy_port] [requested_url]
```
* Note:
_proxy_host_ should match the IP address of the proxy server,
_proxy_port_ should match the port on which the proxy is running,
therefore, their defualt values are `local_host` and `50015` as those specified for `web_proxy.py`
`requested_url` defaults to http://example.com/

## IMPORTANT
* The project does not require installation of any external libraries
* The current project design only allows the proxy to access files via the `http` protocol,
thus, if the you try to connect to a website that utilizes the `https` protocol, you are going to receive the following message at the client side:
```
HTTP/1.1 301 Moved Permanently
```
As an example try to access the following webpage:
```
https://cooking.nytimes.com/68861692-nyt-cooking/1324291-ramadan-main-dishes
```
* Another drawback of the current design is that it can only parse the webpages that utilize utf-8 encoding. Hence, you won't be able to parse a page that uses a different encoding type.

## Examples of webpages that can be easily accessed:
    http://example.com/
    http://eu.httpbin.org
    http://info.cern.ch/
    http://www-db.deis.unibo.it/
    http://info.cern.ch/hypertext/WWW/TheProject.html

# To install the package
```
git clone https://github.com/Yehor-Mishchyriak/Simple-Web-Proxy-and-Client.git
```
