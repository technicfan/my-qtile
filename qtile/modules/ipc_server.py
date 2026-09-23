import os
import socket
import struct
import threading

from .functions import get_distro


class IPCServer:
    def __init__(self, qtile):
        self.path = os.path.expanduser("~/.config/qtile/waybar/socket")
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
            conn, _ = self.socket.accept()
            if self.running:
                thread = threading.Thread(target=self._handle, args=[conn])
                self.threads[conn] = thread
                self.conns[conn] = 1
                thread.start()

    def start(self):
        if not self.running:
            self.main_thread = threading.Thread(target=self._run)
            self.running = True
            self.main_thread.start()

    def close(self):
        if self.main_thread:
            self.running = False
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
                s.connect(self.path)
                s.close()
            self.main_thread.join()
            for conn in self.conns:
                conn.setblocking(False)
                conn.close()
                thread = self.threads.get(conn)
                if thread:
                    thread.join()

    def notify_all(self, signal: int):
        for conn, t in self.conns.items():
            if t == signal:
                try:
                    conn.send(struct.pack("i", signal))
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
                    case 0:  # update request
                        conn.send(struct.pack("i", arg))
                        self.conns[conn] = 0
                    case 1:  # group request
                        msg = self._groups(arg).encode()
                        conn.send(struct.pack("i", 0))
                        conn.send(struct.pack("i", len(msg)))
                        conn.send(msg)
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
            except ConnectionResetError, BrokenPipeError:
                break
        self.threads.pop(conn)
        self.conns.pop(conn)
        conn.close()

    def _groups(self, show_all: int):
        screen = self.qtile.current_group.info()["screen"]
        output = ""
        for group in self.qtile.get_groups().values():
            if group["screen"] is not None:
                if group["screen"] == screen:
                    output += f"<p>{group['label']}</p>;"
                else:
                    output += f"<s>{group['label']}</s>;"
            elif group["label"] != "" and (show_all == 1 or len(group["windows"]) > 0):
                output += f"{group['label']};"
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
