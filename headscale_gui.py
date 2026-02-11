#!/usr/bin/env python3
"""
Headscale VPN Client GUI
A cross-platform GUI for connecting to Headscale servers
"""

import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
import platform
import os
import json
import sys
from pathlib import Path

class HeadscaleGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ServerStore VPN - Headscale Client")
        self.root.geometry("500x400")
        self.root.resizable(False, False)
        
        # Determine OS
        self.os_type = platform.system()
        
        # Config file path
        self.config_file = Path.home() / ".headscale_gui_config.json"
        
        # Connection status
        self.connected = False
        
        # Setup UI
        self.setup_ui()
        
        # Load saved configuration
        self.load_config()
        
        # Check initial connection status
        self.check_connection_status()
        
    def setup_ui(self):
        """Setup the user interface"""
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Logo/Title
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Create logo using text (you can replace with image later)
        logo_label = tk.Label(
            title_frame,
            text="🔒 ServerStore VPN",
            font=("Helvetica", 24, "bold"),
            fg="#2563eb"
        )
        logo_label.pack()
        
        subtitle_label = tk.Label(
            title_frame,
            text="Headscale Client Manager",
            font=("Helvetica", 10),
            fg="#64748b"
        )
        subtitle_label.pack()
        
        # Server IP input
        ttk.Label(main_frame, text="Headscale Server IP:", font=("Helvetica", 10)).grid(
            row=1, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.server_ip_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 10))
        self.server_ip_entry.grid(row=2, column=0, columnspan=2, pady=(0, 15), ipady=5)
        
        # Port input
        ttk.Label(main_frame, text="Port (default: 8080):", font=("Helvetica", 10)).grid(
            row=3, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.port_entry = ttk.Entry(main_frame, width=40, font=("Helvetica", 10))
        self.port_entry.insert(0, "8080")
        self.port_entry.grid(row=4, column=0, columnspan=2, pady=(0, 15), ipady=5)
        
        # Auth Key input
        ttk.Label(main_frame, text="Authentication Key:", font=("Helvetica", 10)).grid(
            row=5, column=0, sticky=tk.W, pady=(0, 5)
        )
        
        self.auth_key_entry = ttk.Entry(main_frame, width=40, show="*", font=("Helvetica", 10))
        self.auth_key_entry.grid(row=6, column=0, columnspan=2, pady=(0, 5), ipady=5)
        
        # Show/Hide auth key checkbox
        self.show_key_var = tk.BooleanVar()
        show_key_check = ttk.Checkbutton(
            main_frame,
            text="Show authentication key",
            variable=self.show_key_var,
            command=self.toggle_key_visibility
        )
        show_key_check.grid(row=7, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # Accept routes checkbox
        self.accept_routes_var = tk.BooleanVar(value=True)
        accept_routes_check = ttk.Checkbutton(
            main_frame,
            text="Accept routes from other nodes",
            variable=self.accept_routes_var
        )
        accept_routes_check.grid(row=8, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # Connection buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=2, pady=(0, 15))
        
        self.connect_button = tk.Button(
            button_frame,
            text="Connect",
            command=self.connect,
            bg="#10b981",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=12,
            height=2,
            cursor="hand2"
        )
        self.connect_button.pack(side=tk.LEFT, padx=5)
        
        self.disconnect_button = tk.Button(
            button_frame,
            text="Disconnect",
            command=self.disconnect,
            bg="#ef4444",
            fg="white",
            font=("Helvetica", 12, "bold"),
            width=12,
            height=2,
            cursor="hand2",
            state=tk.DISABLED
        )
        self.disconnect_button.pack(side=tk.LEFT, padx=5)
        
        # Status label
        self.status_label = tk.Label(
            main_frame,
            text="Status: Disconnected",
            font=("Helvetica", 10),
            fg="#64748b"
        )
        self.status_label.grid(row=10, column=0, columnspan=2, pady=(0, 10))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        
    def toggle_key_visibility(self):
        """Toggle authentication key visibility"""
        if self.show_key_var.get():
            self.auth_key_entry.config(show="")
        else:
            self.auth_key_entry.config(show="*")
    
    def load_config(self):
        """Load saved configuration"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    self.server_ip_entry.insert(0, config.get('server_ip', ''))
                    self.port_entry.delete(0, tk.END)
                    self.port_entry.insert(0, config.get('port', '8080'))
                    # Don't load auth key for security reasons
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def save_config(self):
        """Save configuration (without auth key)"""
        try:
            config = {
                'server_ip': self.server_ip_entry.get(),
                'port': self.port_entry.get()
            }
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
    
    def check_connection_status(self):
        """Check if Tailscale is currently connected"""
        try:
            if self.os_type == "Windows":
                result = subprocess.run(
                    ["tailscale", "status"],
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                result = subprocess.run(
                    ["tailscale", "status"],
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0 and result.stdout.strip():
                self.connected = True
                self.update_ui_state(connected=True)
                self.status_label.config(text="Status: Connected", fg="#10b981")
            else:
                self.connected = False
                self.update_ui_state(connected=False)
                self.status_label.config(text="Status: Disconnected", fg="#64748b")
        except FileNotFoundError:
            messagebox.showerror(
                "Tailscale Not Found",
                "Tailscale is not installed or not in PATH.\n\n"
                "Please install Tailscale first:\n"
                "- Windows: https://tailscale.com/download/windows\n"
                "- Linux: https://tailscale.com/download/linux"
            )
        except Exception as e:
            print(f"Error checking status: {e}")
    
    def update_ui_state(self, connected):
        """Update UI based on connection state"""
        if connected:
            self.connect_button.config(state=tk.DISABLED)
            self.disconnect_button.config(state=tk.NORMAL)
            self.server_ip_entry.config(state=tk.DISABLED)
            self.port_entry.config(state=tk.DISABLED)
            self.auth_key_entry.config(state=tk.DISABLED)
        else:
            self.connect_button.config(state=tk.NORMAL)
            self.disconnect_button.config(state=tk.DISABLED)
            self.server_ip_entry.config(state=tk.NORMAL)
            self.port_entry.config(state=tk.NORMAL)
            self.auth_key_entry.config(state=tk.NORMAL)
    
    def connect(self):
        """Connect to Headscale server"""
        server_ip = self.server_ip_entry.get().strip()
        port = self.port_entry.get().strip()
        auth_key = self.auth_key_entry.get().strip()
        
        # Validate inputs
        if not server_ip:
            messagebox.showerror("Error", "Please enter the Headscale server IP address")
            return
        
        if not port:
            messagebox.showerror("Error", "Please enter the port number")
            return
            
        if not auth_key:
            messagebox.showerror("Error", "Please enter the authentication key")
            return
        
        # Build login server URL
        login_server = f"http://{server_ip}:{port}"
        
        # Build command
        cmd = ["tailscale", "up", f"--login-server={login_server}", f"--authkey={auth_key}"]
        
        if self.accept_routes_var.get():
            cmd.append("--accept-routes")
        
        # Update status
        self.status_label.config(text="Status: Connecting...", fg="#f59e0b")
        self.root.update()
        
        try:
            # Execute command based on OS
            if self.os_type == "Windows":
                # On Windows, try to run with elevated privileges
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                # On Linux/Mac, use sudo if not root
                if os.geteuid() != 0:
                    cmd.insert(0, "sudo")
                    # Use pkexec for GUI sudo if available
                    if subprocess.run(["which", "pkexec"], capture_output=True).returncode == 0:
                        cmd[0] = "pkexec"
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                self.connected = True
                self.update_ui_state(connected=True)
                self.status_label.config(text="Status: Connected", fg="#10b981")
                self.save_config()
                messagebox.showinfo("Success", "Successfully connected to Headscale server!")
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                self.status_label.config(text="Status: Connection Failed", fg="#ef4444")
                messagebox.showerror(
                    "Connection Failed",
                    f"Failed to connect to Headscale server.\n\nError: {error_msg}"
                )
        except FileNotFoundError:
            self.status_label.config(text="Status: Tailscale Not Found", fg="#ef4444")
            messagebox.showerror(
                "Tailscale Not Found",
                "Tailscale is not installed or not in PATH.\n\n"
                "Please install Tailscale first."
            )
        except Exception as e:
            self.status_label.config(text="Status: Error", fg="#ef4444")
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    
    def disconnect(self):
        """Disconnect from Headscale"""
        # Confirm disconnection
        if not messagebox.askyesno(
            "Confirm Disconnect",
            "Are you sure you want to disconnect from the VPN?"
        ):
            return
        
        self.status_label.config(text="Status: Disconnecting...", fg="#f59e0b")
        self.root.update()
        
        try:
            cmd = ["tailscale", "down"]
            
            if self.os_type == "Windows":
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:
                if os.geteuid() != 0:
                    cmd.insert(0, "sudo")
                    if subprocess.run(["which", "pkexec"], capture_output=True).returncode == 0:
                        cmd[0] = "pkexec"
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True
                )
            
            if result.returncode == 0:
                self.connected = False
                self.update_ui_state(connected=False)
                self.status_label.config(text="Status: Disconnected", fg="#64748b")
                messagebox.showinfo("Disconnected", "Successfully disconnected from VPN")
            else:
                error_msg = result.stderr if result.stderr else result.stdout
                messagebox.showerror(
                    "Disconnection Failed",
                    f"Failed to disconnect.\n\nError: {error_msg}"
                )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")


def main():
    root = tk.Tk()
    app = HeadscaleGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
