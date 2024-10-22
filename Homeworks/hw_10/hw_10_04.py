"""
Задача 4: створення веб-сервера, що обслуговує кілька клієнтів одночасно.

Напишіть простий веб-сервер, який може обслуговувати кілька клієнтів одночасно,
використовуючи потоки або процеси.
Ваша програма повинна відповідати на HTTP-запити клієнтів і відправляти їм текстові повідомлення.

Підказка: можна використовувати вбудовану бібліотеку http.server.
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
from concurrent.futures import ThreadPoolExecutor
import threading

# ---- Global Variables ----
max_workers = 5
semaphore = threading.BoundedSemaphore(value=max_workers)


# ---- Request Handler Class ----
class SimpleHandler(BaseHTTPRequestHandler):
    """
    Handle HTTP GET and POST requests.

    The SimpleHandler processes GET and POST requests, limiting the number of simultaneous requests
    using a semaphore.
    """

    def do_GET(self):
        """
        Handle GET requests and send a basic text response.

        The GET response is limited by a semaphore to control concurrent access.
        """
        with semaphore:
            message = "Hello, this is a response to a GET request!"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(message.encode())

    def do_POST(self):
        """
        Handle POST requests and echo back the posted data.

        The POST response is limited by a semaphore to control concurrent access.
        """
        with semaphore:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            message = f"Hello, you POSTed: {post_data.decode()}"
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(message.encode())


# ---- Threaded HTTP Server Class ----
class ThreadedHTTPServer(HTTPServer):
    """
    HTTP server with thread-pool handling for concurrent requests.

    The ThreadedHTTPServer uses a ThreadPoolExecutor to handle requests asynchronously,
    allowing for multi-threaded request processing.
    """

    def __init__(self, server_address, RequestHandlerClass):
        """
        Initialize the server with the given address and request handler.

        :param server_address: Tuple with the server address and port.
        :type server_address: tuple
        :param RequestHandlerClass: Request handler class to handle requests.
        :type RequestHandlerClass: class
        """
        super().__init__(server_address, RequestHandlerClass)
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def process_request(self, request, client_address):
        """
        Submit the request to be handled by the thread pool.

        :param request: Client request object.
        :type request: socket
        :param client_address: Client address tuple.
        :type client_address: tuple
        """
        self.executor.submit(self.__new_request, request, client_address)

    def __new_request(self, request, client_address):
        """
        Handle a new request using the provided client address.

        This method ensures that the request is processed and properly shutdown after completion.
        """
        try:
            self.finish_request(request, client_address)
            self.shutdown_request(request)
        except Exception:
            self.handle_error(request, client_address)
            self.shutdown_request(request)


# ---- Main Execution Block ----
if __name__ == "__main__":
    server_address = ('', 8080)
    httpd = ThreadedHTTPServer(server_address, SimpleHandler)
    print("Starting server on port 8080, use <Ctrl-C> to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
