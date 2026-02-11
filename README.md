# headclient

I'll create a cross-platform Python GUI application for your Headscale client connection manager. Let me build this with a professional interface and the ServerStore VPN logo.Now let me create a README with instructions and a script to build portable executables:Now let me create a simple SVG logo file that can be used with the application:Now let me create a quick start guide:Perfect! Now let me move all the files to the outputs directory:Perfect! I've created a complete cross-platform Headscale VPN client GUI for you. Here's what you get:

## 📦 Package Contents

1. **headscale_gui.py** - Main GUI application with:
   - Clean, modern interface with ServerStore VPN branding
   - Server IP, port, and auth key inputs
   - Show/hide password for auth key
   - Accept routes checkbox
   - Connect/Disconnect buttons with status indicators
   - Configuration saving (IP and port only, not auth key for security)
   - Cross-platform support (Windows, Linux, macOS)

2. **build_executable.py** - Script to build portable executables for distribution

3. **README.md** - Complete documentation with installation, usage, and troubleshooting

4. **QUICKSTART.md** - User-friendly guide for both end users and administrators

5. **requirements.txt** - Python dependencies

6. **logo.svg** - ServerStore VPN logo (shield with lock design)

## 🚀 Quick Start

**For testing right now:**
```bash
python headscale_gui.py
```

**To build portable executables:**
```bash
pip install pyinstaller
python build_executable.py
```

## ✨ Key Features

- ✅ No command-line needed for users
- ✅ Remembers server settings between sessions
- ✅ Secure (auth keys never saved)
- ✅ Works on Windows, Linux, and macOS
- ✅ Clean status indicators (green=connected, red=error)
- ✅ Automatic sudo/admin privilege handling
- ✅ Simple connect/disconnect workflow

The GUI handles all the complexity of running `tailscale up` with the right parameters, so your users just enter their details and click Connect!
