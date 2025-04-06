# 🧠 Keylogger Demonstration Project

> **Disclaimer:** This project is strictly for **educational** and **authorized cybersecurity research** purposes. It demonstrates how keyloggers work and how to defend against them.  
> **Do not deploy this tool on systems you do not own or have written permission to test. Unauthorized use is illegal.**

---

## 📌 Project Overview

This project simulates a real-world keylogger for **educational** and **defensive research** purposes. It helps users understand:

- Keylogger operation mechanics
- Data exfiltration via network sockets
- How to detect, analyze, and defend against keylogging behavior
- The ethical implications of surveillance tools

### Included Features:

- 🛠️ **Builder GUI** – Easily create custom keylogger executables
- 👂 **Listener Server** – Monitor and log captured keystrokes
- 🔐 **Secure Socket Communication** – For reliable data transfer

---

## ✅ Ethical Use Cases

This tool can be ethically used in:

- ✅ **Penetration testing** with written consent
- ✅ **Corporate red teaming**
- ✅ **Cybersecurity education and lab exercises**
- ✅ **Parental controls** (with full transparency)

---

## ⚙️ Technical Components

### `gui.py` – Keylogger Builder
- Input IP and port for the keylogger connection
- Displays received keystrokes in real time
- Supports building a `.exe` payload via PyInstaller
- Handles input validation and error catching

### `keylogger.py` – Payload
- Uses `pynput` to capture keyboard input
- Transmits data using TCP sockets
- Supports retry logic for reconnection
- Gracefully exits on `ESC` key
- Detects and formats special keys

---

## 🧰 Requirements

Install all dependencies with:

```bash
pip install -r requirements.txt
```

### `requirements.txt`

```
pynput
tkinter
pyinstaller
```

---

## 🚀 Usage Instructions

### 1. Run the Builder GUI

```bash
python gui.py
```

### 2. Build the Executable (.exe)

> Windows Only (Run in CMD or PowerShell):

```bash
pyinstaller --onefile --noconsole keylogger.py
```

- Output will be in the `/dist` directory.
- Move the `.exe` to a test environment **you are authorized to analyze**.

### 3. Deploy & Monitor

- Run the `.exe` payload on an authorized machine.
- Start the listener in the GUI to receive keystrokes.
- Captured keystrokes will appear in the GUI panel in real time.

---

## 🛡️ Detection & Prevention

This tool aids defenders in understanding and testing detection techniques:

- Monitor for hidden Python-based or renamed `.exe` processes
- Analyze outbound connections to suspicious IPs or unusual ports
- Use behavior-based detection in EDR and sandboxes
- Alert on keylogging libraries like `pynput` being imported

---

## ⚖️ Legal Notice

This project is licensed for:

- ✅ Ethical hacking courses
- ✅ Controlled lab environments
- ✅ Client-approved penetration testing
- ❌ Not for spying, stalking, or unauthorized surveillance

By using this project, you confirm that you understand and will adhere to **all applicable laws and ethical guidelines**.

---

## 🤝 Contributing

Contributions are welcome!

You can submit:
- 🔐 New security features
- 🧠 Improved logging or monitoring methods
- 📖 Updated ethical usage and documentation

To contribute, fork the repo and submit a pull request.

---

## 👻 Ghost – Because even ghosts leave traces
