import os
import socket
import struct
import threading

from libqtile import qtile

from .functions import get_distro


class Server:
    def __init__(self, path: str):
        self.path = path
        if os.path.exists(self.path):
            os.unlink(self.path)
        self.qtile = qtile
        self.socket = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.socket.bind(self.path)
        self.socket.listen(1)
        self.running = False
        self.conns = dict[socket.socket, int]()
        self.threads = dict[socket.socket, threading.Thread]()
        self.main_thread = None

    def _run(self):
        while self.running:
            try:
                conn, _ = self.socket.accept()
                if self.running:
                    thread = threading.Thread(target=self._handle, args=[conn])
                    self.threads[conn] = thread
                    self.conns[conn] = 1
                    thread.start()
            except OSError:
                break
        self.socket.close()

    def start(self):
        if not self.running and not self.main_thread:
            self.main_thread = threading.Thread(target=self._run)
            self.running = True
            self.main_thread.start()

    def close(self):
        if self.main_thread:
            self.running = False
            self.socket.shutdown(socket.SHUT_RDWR)
            self.main_thread.join()
            for conn in self.conns:
                thread = self.threads.get(conn)
                if thread:
                    conn.shutdown(socket.SHUT_RDWR)
                    thread.join()

    def notify_all(self, signal: int):
        for conn, t in self.conns.items():
            if t == signal:
                try:
                    conn.send(struct.pack("i", signal))
                    if signal == 0:
                        self._send_groups(conn)
                except ConnectionResetError, BrokenPipeError:
                    pass

    def _handle(self, conn: socket.socket):
        while self.running:
            try:
                command = conn.recv(4)
                arg = conn.recv(4)
                if not (command and arg):
                    raise BrokenPipeError
                command = int.from_bytes(command, "little")
                arg = int.from_bytes(arg, "little")
                match command:
                    case 0:  # group update request
                        conn.send(struct.pack("i", arg))
                        self._send_groups(conn)
                        self.conns[conn] = 0
                    case 2:  # switch request
                        name = conn.recv(arg).decode()
                        self._switch(name)
                    case 3:  # window request
                        port = conn.recv(arg).decode()
                        msg = self._window(port).encode()
                        conn.send(struct.pack("i", 0))
                        conn.send(struct.pack("i", len(msg)))
                        conn.send(msg)
                    case _:
                        pass
            except ConnectionResetError, BrokenPipeError, OSError:
                break
        if self.running:
            self.threads.pop(conn)
            self.conns.pop(conn)
        conn.close()

    def _send_groups(self, conn: socket.socket):
        msg = self._groups().encode()
        conn.send(struct.pack("i", 0))
        conn.send(struct.pack("i", len(msg)))
        conn.send(msg)

    def _groups(self):
        screen = self.qtile.current_group.info()["screen"]
        output = ""
        for group in self.qtile.get_groups().values():
            if group["screen"] is not None:
                if group["screen"] == screen:
                    output += f"<a>{group['label']};"
                else:
                    output += f"<v>{group['label']};"
            elif group["label"] != "":
                if len(group["windows"]) > 0:
                    output += f"{group['label']};"
                else:
                    output += f"<e>{group['label']};"
        return output

    def _get_screen(self, port: str):
        screen = 0
        try:
            while True:
                if self.qtile.screens[screen].info()["port"] == port:
                    break
                else:
                    screen += 1
        except IndexError, KeyError:
            pass
        return screen

    def _switch(self, label: str):
        try:
            for group in self.qtile.get_groups().values():
                if group["label"] == label:
                    self.qtile.groups_map[group["name"]].toscreen()
        except KeyError:
            pass
        return ""

    def _window(self, port: str):
        try:
            name = self.qtile.groups_map[
                self.qtile.get_screens()[self._get_screen(port)]["group"]
            ].info()["focus"]
            if name is not None:
                return name.lower()
            raise KeyError
        except IndexError, KeyError:
            return get_distro("Linux") + " - Qtile".lower()
