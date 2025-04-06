# Keylogger Demonstration Project

**Disclaimer**: This project is for educational and cybersecurity research purposes only. It demonstrates keylogger concepts for defensive cybersecurity awareness. Unauthorized use against systems you don't own or have permission to test is illegal.

## Project Overview

This project demonstrates:
- How keyloggers operate at a technical level
- Common data exfiltration techniques
- Defensive detection methods
- Ethical considerations around monitoring tools

The implementation includes:
- 🛠️ Builder GUI to create keylogger executables
- 👂 Listener server to monitor keystrokes (for authorized testing only)
- 🔐 Secure socket communication demonstration

## Ethical Use Cases

Appropriate uses include:
- Penetration testing with explicit written consent
- Corporate security audits
- Cybersecurity education
- Parental control systems (with full disclosure)

## Technical Components

### Builder GUI (`gui.py`)
- Creates customized keylogger executables
- Listens for incoming keylogger connections
- Displays captured keystrokes in real-time
- Validates input parameters

### Keylogger (`keylogger.py`)
- Captures and transmits keystrokes
- Uses Python's `pynput` library
- Implements socket communication
- Includes connection retry logic

## Setup Instructions

1. **Requirements**:
   ```bash
   pip install pynput pyinstaller tkinter