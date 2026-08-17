#!/usr/bin/env python3
"""
Face Recognition App Launcher
=============================
This script launches the HTTP server and opens the face recognition app in your browser.

Usage: python launcher.py [port]
Default port: 8000
"""

import http.server
import socketserver
import webbrowser
import threading
import time
import sys
import os
import ssl
from pathlib import Path

# Configuration
DEFAULT_PORT = 8000
SERVER_DELAY = 2  # seconds to wait before opening browser

class CustomHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler with better error handling and CORS support"""
    
    def end_headers(self):
        # Add CORS headers to allow local file access
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging to make output cleaner"""
        print(f"[{time.strftime('%H:%M:%S')}] {format % args}")

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'index.html',
        'face-api.min.js',
        'models/tiny_face_detector',
        'models/face_recognition', 
        'models/face_landmark_68',
        'Faces'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files/directories:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print("✅ All required files found")
    return True

def find_available_port(start_port=DEFAULT_PORT):
    """Find an available port starting from the given port"""
    import socket
    
    for port in range(start_port, start_port + 10):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    
    raise Exception(f"No available ports found starting from {start_port}")

def open_browser(port):
    """Open the app in the default browser after a delay"""
    time.sleep(SERVER_DELAY)
    url = f"https://localhost:{port}"
    print(f"🌐 Opening {url} in your browser...")
    webbrowser.open(url)

def start_server(port):
    """Start the HTTPS server"""
    try:
        # Change to the script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)

        # Check requirements
        if not check_requirements():
            print("\n❌ Please ensure all required files are present before running the app.")
            return False

        # Create server
        handler = CustomHTTPRequestHandler
        with socketserver.TCPServer(("", port), handler) as httpd:
            # Wrap the socket with SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile="localhost.pem", keyfile="localhost.key", password=None)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

            print(f"\n🚀 Face Recognition App Launcher")
            print(f"📁 Serving from: {script_dir}")
            print(f"🔒 HTTPS server running at: https://localhost:{port}")
            print(f"📹 Access your face recognition app in the browser!")
            print(f"\n💡 Features available:")
            print(f"   - Real-time face detection and recognition")
            print(f"   - Recognition logging with timestamps")
            print(f"   - Download recognition records as JSON")
            print(f"\n⚠️  Make sure to allow webcam access when prompted!")
            print(f"\n🔄 Press Ctrl+C to stop the server\n")

            # Start browser in a separate thread
            browser_thread = threading.Thread(target=open_browser, args=(port,))
            browser_thread.daemon = True
            browser_thread.start()

            # Start server
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print(f"\n\n🛑 Server stopped by user")
                return True

    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {port} is already in use. Trying to find another port...")
            try:
                new_port = find_available_port(port + 1)
                print(f"✅ Using port {new_port} instead")
                return start_server(new_port)
            except Exception:
                print(f"❌ Could not find an available port")
                return False
        else:
            print(f"❌ Server error: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main launcher function"""
    print("🎯 Face Recognition App Launcher Starting...")
    
    # Parse command line arguments
    port = DEFAULT_PORT
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if not (1024 <= port <= 65535):
                raise ValueError("Port must be between 1024 and 65535")
        except ValueError as e:
            print(f"❌ Invalid port: {e}")
            print(f"Usage: python launcher.py [port]")
            sys.exit(1)
    
    # Check if enhanced server exists and use it
    enhanced_server_path = Path("enhanced_server.py")
    if enhanced_server_path.exists():
        print("🚀 Found enhanced server with record saving support!")
        print("🔄 Starting enhanced server...")
        try:
            # Import and use the enhanced server directly
            import enhanced_server
            success = enhanced_server.start_enhanced_server(port)
            if success:
                print("👋 Thanks for using Face Recognition App!")
            else:
                print("❌ Enhanced server failed, falling back to basic server")
                success = start_server(port)
                if not success:
                    print("❌ Failed to start the application")
                    sys.exit(1)
        except ImportError as e:
            print(f"⚠️ Could not import enhanced server: {e}")
            print("📝 Falling back to basic server")
            success = start_server(port)
            if not success:
                print("❌ Failed to start the application")
                sys.exit(1)
    else:
        # Fallback to basic server
        print("📝 Using basic server (no record saving)")
        success = start_server(port)
        
        if success:
            print("👋 Thanks for using Face Recognition App!")
        else:
            print("❌ Failed to start the application")
            sys.exit(1)

if __name__ == "__main__":
    main()
