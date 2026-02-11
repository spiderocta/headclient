# Quick Start Guide - ServerStore VPN Client

## For End Users (Non-Technical)

### Step 1: Install Tailscale
Before using this VPN client, you need to install Tailscale:

**Windows:**
1. Download Tailscale from: https://tailscale.com/download/windows
2. Run the installer
3. Restart your computer

**Linux (Ubuntu/Debian):**
```bash
curl -fsSL https://tailscale.com/install.sh | sh
```

**macOS:**
1. Download Tailscale from: https://tailscale.com/download/mac
2. Install the application
3. Restart your computer

### Step 2: Get Your Connection Details

Contact your VPN administrator to get:
1. **Server IP Address** (example: `192.168.1.100` or `vpn.yourcompany.com`)
2. **Port Number** (usually `8080`)
3. **Authentication Key** (a long string of characters)

### Step 3: Run the VPN Client

**If you have the executable (.exe or standalone file):**
- Windows: Double-click `ServerStoreVPN.exe`
- Linux: Make it executable first with `chmod +x ServerStoreVPN`, then run `./ServerStoreVPN`
- macOS: Double-click `ServerStoreVPN.app`

**If you're running the Python script:**
```bash
python headscale_gui.py
```

### Step 4: Connect to VPN

1. Enter the **Server IP** provided by your administrator
2. Enter the **Port** (default is 8080)
3. Paste your **Authentication Key**
4. Check "Accept routes from other nodes" if you need to access other computers
5. Click **Connect**
6. On Linux/Mac: Enter your password when prompted

### Step 5: Verify Connection

Once connected:
- The status will show "Connected" in green
- You can now access your company's internal resources
- The Connect button will be disabled (can't connect twice)

### Step 6: Disconnect When Done

1. Click the **Disconnect** button
2. Confirm you want to disconnect
3. Your network will return to normal

## For VPN Administrators

### Generating Authentication Keys for Users

On your Headscale server, run:

```bash
# Create a user (if not exists)
headscale users create USERNAME

# Generate a pre-auth key
headscale preauthkeys create --user USERNAME --expiration 24h --reusable
```

**Options:**
- `--expiration 24h` - Key expires in 24 hours (adjust as needed)
- `--reusable` - Key can be used multiple times
- Remove `--reusable` for one-time use keys (more secure)

### Recommended Key Distribution

For maximum security:
1. Generate one-time use keys (`--reusable` flag removed)
2. Use short expiration times (1-24 hours)
3. Send keys via secure channels (encrypted email, password manager)
4. Generate new keys for each user/device

### Server Configuration

Make sure your Headscale server is configured correctly:

```yaml
# config.yaml
server_url: http://YOUR_SERVER_IP:8080
listen_addr: 0.0.0.0:8080
```

### Firewall Settings

Ensure these ports are open:
- **Port 8080** (or your configured port) - for Headscale control plane
- **Port 3478/UDP** - for DERP relay (Tailscale's NAT traversal)

### Troubleshooting for Administrators

**Users can't connect:**
1. Check Headscale server logs: `journalctl -u headscale -f`
2. Verify server is accessible: `curl http://YOUR_SERVER_IP:8080/health`
3. Check auth key hasn't expired: `headscale preauthkeys list --user USERNAME`
4. Verify firewall rules allow connections on port 8080

**Connection drops frequently:**
1. Check server resource usage (CPU, memory)
2. Review Headscale logs for errors
3. Ensure stable internet connection on server
4. Consider using HTTPS instead of HTTP (more stable)

## Security Best Practices

### For Users:
- ✅ Never share your authentication key
- ✅ Disconnect when not using the VPN
- ✅ Keep Tailscale updated
- ✅ Report lost devices to your administrator

### For Administrators:
- ✅ Use one-time authentication keys when possible
- ✅ Set short expiration times on keys
- ✅ Regularly audit connected devices: `headscale nodes list`
- ✅ Remove unused devices: `headscale nodes delete --identifier NODE_ID`
- ✅ Use HTTPS with valid certificates in production
- ✅ Enable access control lists (ACLs) to restrict access
- ✅ Keep Headscale server updated

## Common Issues and Solutions

### "Tailscale Not Found"
**Solution:** Install Tailscale (see Step 1 above)

### "Permission Denied" (Linux/macOS)
**Solution:** The app needs administrator rights. You'll be prompted for your password.

### "Connection Failed"
**Possible causes:**
- Wrong server IP or port
- Expired authentication key
- Firewall blocking connection
- Headscale server is down

**Solutions:**
1. Verify server IP and port with administrator
2. Request a new authentication key
3. Check with administrator about server status

### "Already Connected"
**Solution:** Disconnect first, then reconnect with new credentials

## Advanced Usage

### Using HTTPS (Recommended for Production)

If your administrator has configured HTTPS, use:
- Server URL: `https://vpn.yourcompany.com`
- Port: `443` (or configured HTTPS port)

### Custom Routes

If you need to access specific subnets, ask your administrator to configure:
```bash
headscale routes enable --identifier NODE_ID --route 10.0.0.0/24
```

Then make sure "Accept routes from other nodes" is checked in the GUI.

## Support Contacts

- **Technical Issues with GUI:** [Your support contact]
- **VPN Access Issues:** [Your VPN administrator]
- **Headscale Issues:** https://github.com/juanfont/headscale
- **Tailscale Issues:** https://tailscale.com/contact/support
