import itertools
import socket
import json
import re


def get_components(filename):
    pattern = r"Mw Server now listening on port (\d+) for component (\w+)\."
    text = open(filename).read()
    match = re.findall(pattern, text)

    components = {device: int(port) for port, device in match}

    robot_id = lambda x: x.rpartition('_')[-1]
    data = sorted(components.keys(), key=robot_id)
    groups = itertools.groupby(data, key=robot_id)

    return [{key: components[key] for key in g} for k, g in groups]


class MorsesimError(Exception):
    pass


class Device(object):
    def __init__(self, name, port, host='localhost'):
        self.socket = None
        self.buffer = ''
        self.name = name
        self.port = port
        self.host = host

        self._connect()

    def _connect(self):
        info = socket.getaddrinfo(self.host, self.port,
                                  socket.AF_UNSPEC, socket.SOCK_STREAM)

        for res in info:
            af, socktype, proto, canonname, sa = res

            try:
                self.socket = socket.socket(af, socktype, proto)
            except socket.error:
                raise

            try:
                self.socket.connect(sa)
            except socket.error:
                self.socket.close()
                self.socket = None
                raise
            break

    def __del__(self):
        self.socket.close()


class Sensor(Device):
    def read(self):
        got_message = False

        while not got_message:
            data = self.socket.recv(1024)

            if not data:
                raise MorsesimError('socket connection broken')

            self.buffer += data.decode('utf-8')
            messages = self.buffer.split('\n')

            if len(messages) == 1:
                continue

            for message in messages[:-1]:
                got_message = True

            self.buffer = messages[-1]

        decoded_message = json.loads(message)
        return (decoded_message)


class Actuator(Device):
    def write(self, msg):
        data_out = (json.dumps((msg)) + '\n').encode()
        sent = self.socket.send(data_out)

        if not sent:
            raise MorsesimError('socket connection broken')
