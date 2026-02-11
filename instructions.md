# ServerStore VPN - Headscale Client GUI

A cross-platform GUI application for connecting to your self-hosted Headscale server without needing to use command-line tools.

## Features

- 🖥️ **Cross-Platform**: Works on Windows, Linux, and macOS
- 🔒 **Secure**: Authentication keys are never saved to disk
- 💾 **Remembers Settings**: Saves server IP and port for convenience
- 🎨 **User-Friendly**: Clean, modern interface with clear status indicators
- 🔌 **Easy Connection**: Just enter your server details and click Connect
- 📡 **Route Management**: Option to accept routes from other nodes

## Prerequisites

**Tailscale must be installed on your system:**

- **Windows**: Download from [https://tailscale.com/download/windows](https://tailscale.com/download/windows)
- **Linux**: 
  ```bash
  curl -fsSL https://tailscale.com/install.sh | sh
  ```
- **macOS**: Download from [https://tailscale.com/download/mac](https://tailscale.com/download/mac)

## Installation

### Option 1: Run Python Script Directly

1. Install Python 3.7 or higher
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python headscale_gui.py
   ```

### Option 2: Build Portable Executable

#### Windows
```bash
pip install pyinstaller
python build_executable.py
```
The executable will be in `dist/ServerStoreVPN.exe`

#### Linux
```bash
pip install pyinstaller
python build_executable.py
```
The executable will be in `dist/ServerStoreVPN`

## Usage

1. **Launch the application**
   - Run the Python script or the executable

2. **Enter your Headscale server details**:
   - **Server IP**: Your Headscale server IP address (e.g., `192.168.1.100` or `vpn.example.com`)
   - **Port**: The port your Headscale server is running on (default: 8080)
   - **Authentication Key**: The auth key generated from your Headscale server

3. **Connect**:
   - Check "Accept routes from other nodes" if you want to access other nodes on the network
   - Click the **Connect** button
   - On Linux/macOS, you may be prompted for your password (sudo access required)

4. **Disconnect**:
   - Click the **Disconnect** button to return to normal network operation

## Generating Authentication Keys

On your Headscale server, generate a pre-authentication key:

```bash
headscale preauthkeys create --user YOUR_USERNAME --expiration 24h
```

Copy the generated key and paste it into the GUI application.

## Permissions

### Linux/macOS
- The application requires sudo/root access to connect/disconnect Tailscale
- You will be prompted for your password when connecting or disconnecting
- The app uses `pkexec` if available for a GUI password prompt, otherwise falls back to terminal `sudo`

### Windows
- The application may require administrator privileges
- Right-click the executable and select "Run as administrator" if you encounter permission issues

## Security Notes

- ✅ Authentication keys are **never saved** to disk
- ✅ Server IP and port are saved for convenience (but not sensitive)
- ✅ Configuration is stored in: `~/.headscale_gui_config.json`
- ✅ You can show/hide the authentication key using the checkbox

## Troubleshooting

### "Tailscale Not Found" Error
- Make sure Tailscale is installed and in your system PATH
- On Windows, restart your terminal/computer after installing Tailscale
- On Linux, ensure Tailscale service is running: `sudo systemctl status tailscaled`

### Connection Failed
- Verify your Headscale server is accessible from your network
- Check that the IP address and port are correct
- Ensure your authentication key hasn't expired
- Check your Headscale server logs for more details

### Permission Denied (Linux/macOS)
- The application needs sudo access to control Tailscale
- Make sure your user is in the sudoers file
- Try running with: `sudo python headscale_gui.py`

## Building from Source

### Requirements
```bash
pip install pyinstaller
```

### Build Commands

**Windows:**
```bash
pyinstaller --onefile --windowed --name ServerStoreVPN --icon=icon.ico headscale_gui.py
```

**Linux:**
```bash
pyinstaller --onefile --windowed --name ServerStoreVPN headscale_gui.py
```

**macOS:**
```bash
pyinstaller --onefile --windowed --name ServerStoreVPN --icon=icon.icns headscale_gui.py
```

## License

MIT License - Feel free to use and modify as needed.

## Support

For issues related to:
- **This GUI**: Create an issue in this repository
- **Headscale**: Visit [Headscale GitHub](https://github.com/juanfont/headscale)
- **Tailscale**: Visit [Tailscale Support](https://tailscale.com/contact/support)
