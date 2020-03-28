import asyncore
import asynchat
import socket
import multiprocessing
import logging
import mimetypes
import os
import urllib
import argparse
from time import strftime
from datetime import datetime

responses = {
    200: ('OK', 'Request fulfilled, document follows'),
    400: ('Bad Request',
        'Bad request syntax or unsupported method'),
    403: ('Forbidden',
        'Request forbidden -- authorization will not help'),
    404: ('Not Found', 'Nothing matches the given URI'),
    405: ('Method Not Allowed',
        'Specified method is invalid for this resource.'),
}

class FileProducer(object):
# производитель файлов

    def __init__(self, file, chunk_size=4096):
        self.file = file
        # chunk size - размер куска
        self.chunk_size = chunk_size

    def more(self):
        if self.file:
            data = self.file.read(self.chunk_size)
            if data:
                return data
            self.file.close()
            self.file = None
        return ""


class AsyncServer(asyncore.dispatcher):

    def __init__(self, host="127.0.0.1", port=9090):
        super().__init__()
        self.create_socket()
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(5)


    def handle_accepted(self, sock, addr):
        # ручка принята
        print(f"Incoming connection from {addr}")
        handler = AsyncHTTPRequestHandler(sock)
        handler()

    def serve_forever(self):
        # служить вечно
        pass


class AsyncHTTPRequestHandler(asynchat.async_chat):

    def __init__(self, sock):
        super().__init__(sock)
        self.data = ""
        self.request = None
        self.set_terminator(b"\r\n\r\n")
        self.shutdown = 0


    def collect_incoming_data(self, data):
        # сбор входящих данных
        print(f"Incoming data: {data}")

        self._collect_incoming_data(data)

    def found_terminator(self):
        # найти терминатор
        self.parse_request()

    def parse_request(self):
        # разбор запроса
        if not self.request:
            self.data_list = self.data.split('\r\n')

            first_line_list = self.data_list[0].split()
            self.method = first_line_list[0]
            uri = first_line_list[1]
            protocol = first_line_list[2]
            self.request = dict(
                method=self.method,
                uri=uri,
                protocol=protocol
            )
            self.response_is_good = True
            self.parse_headers()

            if not self.response_is_good:
                self.send_error(400, responses[400])
                self.shutdown = 1

            self.handle_request()
        else:
            self.handle_request()

    def parse_headers(self):
        # разбор заголовков
        self.info = self.data_list[1:]
        body_index = None

        for item in self.info:
            if item == '\r\n':
                body_index = self.data_list.index(item)
                break
            item_data = item.split(": ")
            if len(item_data) == 2:
                self.request[item_data[0]] = item_data[1]
            else:
                self.response_is_good == False
                break

        if body_index:
            self.body = '\n'.join(self.data_list[body_index + 1:])

    def handle_request(self):
        # обработать запрос
        method_name = 'do_' + self.method
        if not hasattr(self, method_name):
            self.send_error(405)
            self.handle_close()
            return
        handler = getattr(self, method_name)
        handler()

    def send_header(self, keyword, value):
        # отправить заголовок
        self.push(f"{keyword}: {value}")

    def send_error(self, code, message=None):
        # отправить ошибку
        try:
            short_msg, long_msg = responses[code]
        except KeyError:
            short_msg, long_msg = '???', '???'
        if message is None:
            message = short_msg

        self.send_response(code, message)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Connection", "close")
        self.end_headers()

    def send_response(self, code, message):
        # отправить ответ
        self.push("HTTP/1.1 {} {}\r\n".format(code, message))

    def end_headers(self):
        # конечные заголовки
        self.push("\r\n")

    @staticmethod
    def date_time_string():
        # дата и время в строке
        now = datetime.now()
        return now.strftime("%c")

    def send_head(self):
        # отправить голову

        self.send_header("Date", self.date_time_string())
        self.send_header("Server", "MyServer")
        self.send_header("Content-Type", "text/plain")

    def do_GET(self):
        # выполнить GET
        self.send_response(code=200, message=responses[200][1])
        self.send_head()
        self.push("\r\n")
        self.push("You got some data from GET-request")

    def do_HEAD(self):
        # выполнить HEAD
        self.send_response(code=200, message=responses[200][1])
        self.send_head()

    def do_POST(self):
        self.send_response(code=200, message=responses[200][0])
        self.send_header("Content-Type", "text/plain")
        self.push('\r\n')
        self.push("info about POST {}".format(self.body))

if __name__ == "__main__":
    server = AsyncServer()
    asyncore.loop()
