#!/usr/bin/env python3
"""
Build script for creating portable executables of the Headscale GUI
"""

import subprocess
import platform
import sys
import os

def build_executable():
    """Build platform-specific executable"""
    
    os_type = platform.system()
    print(f"Building executable for {os_type}...")
    
    # Base PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name", "ServerStoreVPN",
    ]
    
    # Platform-specific options
    if os_type == "Windows":
        print("Building Windows executable...")
        # You can add --icon=icon.ico if you have an icon file
        cmd.append("--clean")
    elif os_type == "Darwin":  # macOS
        print("Building macOS application...")
        # You can add --icon=icon.icns if you have an icon file
        cmd.append("--clean")
    else:  # Linux
        print("Building Linux executable...")
        cmd.append("--clean")
    
    # Add the main script
    cmd.append("headscale_gui.py")
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True)
        
        if result.returncode == 0:
            print("\n" + "="*60)
            print("BUILD SUCCESSFUL!")
            print("="*60)
            
            if os_type == "Windows":
                print(f"\nExecutable location: dist\\ServerStoreVPN.exe")
                print("\nYou can distribute this .exe file to users.")
                print("Users can double-click it to run (no Python needed).")
            elif os_type == "Darwin":
                print(f"\nApplication location: dist/ServerStoreVPN.app")
                print("\nYou can distribute this .app bundle to macOS users.")
            else:
                print(f"\nExecutable location: dist/ServerStoreVPN")
                print("\nYou can distribute this executable to Linux users.")
                print("Make it executable with: chmod +x dist/ServerStoreVPN")
            
            print("\n" + "="*60)
            
    except subprocess.CalledProcessError as e:
        print(f"\nBuild failed with error: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("\nError: PyInstaller not found!")
        print("Please install it with: pip install pyinstaller")
        sys.exit(1)

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller is not installed")
        print("\nPlease install it with:")
        print("  pip install pyinstaller")
        return False

if __name__ == "__main__":
    print("ServerStore VPN - Executable Builder")
    print("="*60)
    
    if not check_dependencies():
        sys.exit(1)
    
    if not os.path.exists("headscale_gui.py"):
        print("\nError: headscale_gui.py not found in current directory!")
        sys.exit(1)
    
    print("\nStarting build process...\n")
    build_executable()
