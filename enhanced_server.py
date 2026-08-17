#!/usr/bin/env python3
"""
Enhanced Face Recognition Server with Record Saving Support
===========================================================
This server supports both serving static files and saving recognition records via POST requests.
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from pathlib import Path
import time
import webbrowser
import threading
import glob
import ssl

def cleanup_old_backups(backup_pattern, max_files=2):
    """Keep only the most recent backup files, delete older ones"""
    backup_files = glob.glob(backup_pattern)
    if len(backup_files) > max_files:
        # Sort by modification time (newest first)
        backup_files.sort(key=os.path.getmtime, reverse=True)
        # Keep only the newest files, delete the rest
        files_to_delete = backup_files[max_files:]
        for file_path in files_to_delete:
            try:
                os.remove(file_path)
                print(f"🗑️ Deleted old backup: {os.path.basename(file_path)}")
            except OSError as e:
                print(f"⚠️ Could not delete {file_path}: {e}")

class FaceRecognitionHandler(http.server.SimpleHTTPRequestHandler):
    """Custom HTTP handler that supports POST requests for saving records"""
    
    def do_POST(self):
        """Handle POST requests for saving recognition records and punch-in data"""
        if self.path == '/save-records':
            try:
                # Get the content length
                content_length = int(self.headers['Content-Length'])
                
                # Read the POST data
                post_data = self.rfile.read(content_length)
                records = json.loads(post_data.decode('utf-8'))
                
                # Ensure Record directory exists
                os.makedirs('Record', exist_ok=True)
                os.makedirs('Record/BackUP', exist_ok=True)
                
                # Save to Local.json
                with open('Record/Local.json', 'w') as f:
                    json.dump(records, f, indent=2)
                
                # Also save a timestamped backup in BackUP folder
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                backup_file = f'Record/BackUP/backup_{timestamp}.json'
                with open(backup_file, 'w') as f:
                    json.dump(records, f, indent=2)
                
                # Clean up old backups (keep only 2 most recent)
                cleanup_old_backups('Record/BackUP/backup_*.json', max_files=2)
                
                print(f"📝 Saved {len(records)} records to Local.json and {backup_file}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': f'Saved {len(records)} records',
                    'timestamp': timestamp
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error saving records: {e}")
                
                # Send error response
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
                
        elif self.path == '/save-punch-in':
            try:
                # Get the content length
                content_length = int(self.headers['Content-Length'])
                
                # Read the POST data
                post_data = self.rfile.read(content_length)
                punch_records = json.loads(post_data.decode('utf-8'))
                
                # Ensure Record directory exists
                os.makedirs('Record', exist_ok=True)
                os.makedirs('Record/BackUP', exist_ok=True)
                
                # Save to Punch_in.json
                with open('Record/Punch_in.json', 'w') as f:
                    json.dump(punch_records, f, indent=2)
                
                # Also save a timestamped backup in BackUP folder
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                backup_file = f'Record/BackUP/punch_in_backup_{timestamp}.json'
                with open(backup_file, 'w') as f:
                    json.dump(punch_records, f, indent=2)
                
                # Clean up old backups (keep only 2 most recent)
                cleanup_old_backups('Record/BackUP/punch_in_backup_*.json', max_files=2)
                
                print(f"🎯 Saved {len(punch_records)} punch-in records to Punch_in.json and {backup_file}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': f'Saved {len(punch_records)} punch-in records',
                    'timestamp': timestamp
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error saving punch-in records: {e}")
                
                # Send error response
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
                
        elif self.path == '/save-punch-out':
            try:
                # Handle punch-out records
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                punch_out_records = json.loads(post_data.decode('utf-8'))
                
                # Ensure Record directory exists
                os.makedirs('Record', exist_ok=True)
                os.makedirs('Record/BackUP', exist_ok=True)
                
                # Save to Punch_out.json
                with open('Record/Punch_out.json', 'w') as f:
                    json.dump(punch_out_records, f, indent=2)
                
                # Also save a timestamped backup in BackUP folder
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                backup_file = f'Record/BackUP/punch_out_backup_{timestamp}.json'
                with open(backup_file, 'w') as f:
                    json.dump(punch_out_records, f, indent=2)
                
                # Clean up old backups (keep only 2 most recent)
                cleanup_old_backups('Record/BackUP/punch_out_backup_*.json', max_files=2)
                
                print(f"🔴 Saved {len(punch_out_records)} punch-out records to Punch_out.json and {backup_file}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': f'Saved {len(punch_out_records)} punch-out records',
                    'timestamp': timestamp
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error saving punch-out records: {e}")
                
                # Send error response
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
                
        elif self.path == '/save-currently-online':
            try:
                # Handle currently online records
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                online_records = json.loads(post_data.decode('utf-8'))
                
                # Ensure Record directory exists
                os.makedirs('Record', exist_ok=True)
                os.makedirs('Record/BackUP', exist_ok=True)
                
                # Save to Currently_online.json
                with open('Record/Currently_online.json', 'w') as f:
                    json.dump(online_records, f, indent=2)
                
                # Also save a timestamped backup in BackUP folder
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                backup_file = f'Record/BackUP/currently_online_backup_{timestamp}.json'
                with open(backup_file, 'w') as f:
                    json.dump(online_records, f, indent=2)
                
                # Clean up old backups (keep only 2 most recent)
                cleanup_old_backups('Record/BackUP/currently_online_backup_*.json', max_files=2)
                
                print(f"👥 Saved {len(online_records)} currently online records to Currently_online.json and {backup_file}")
                
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'success',
                    'message': f'Saved {len(online_records)} currently online records',
                    'timestamp': timestamp
                }
                self.wfile.write(json.dumps(response).encode())
                
            except Exception as e:
                print(f"❌ Error saving currently online records: {e}")
                
                # Send error response
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response = {
                    'status': 'error',
                    'message': str(e)
                }
                self.wfile.write(json.dumps(response).encode())
        else:
            # Return 404 for other POST paths
            self.send_response(404)
            self.end_headers()
    
    def do_OPTIONS(self):
        """Handle OPTIONS requests for CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def end_headers(self):
        # Add CORS headers to all responses
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def log_message(self, format, *args):
        """Custom logging to make output cleaner"""
        timestamp = time.strftime('%H:%M:%S')
        message = format % args
        
        # Color code different request types
        if 'POST /save-records' in message:
            print(f"[{timestamp}] 💾 {message}")
        elif 'POST /save-punch-in' in message:
            print(f"[{timestamp}] 🎯 {message}")
        elif 'POST /save-punch-out' in message:
            print(f"[{timestamp}] 🔴 {message}")
        elif 'POST /save-currently-online' in message:
            print(f"[{timestamp}] 👥 {message}")
        elif 'GET' in message and any(ext in message for ext in ['.js', '.json', '.png', '.jpg']):
            print(f"[{timestamp}] 📁 {message}")
        else:
            print(f"[{timestamp}] 🌐 {message}")

def open_browser(port):
    """Open the app in the default browser after a delay"""
    time.sleep(2)
    url = f"https://localhost:{port}"
    print(f"🌐 Opening {url} in your browser...")
    webbrowser.open(url)

def start_enhanced_server(port=8000):
    """Start the enhanced server with POST support over HTTPS"""
    try:
        # Change to the script directory
        script_dir = Path(__file__).parent
        os.chdir(script_dir)

        # Create server
        with socketserver.TCPServer(("", port), FaceRecognitionHandler) as httpd:
            # Wrap the socket with SSL
            context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
            context.load_cert_chain(certfile="localhost.pem", keyfile="localhost.key", password=None)
            httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

            print(f"\n🚀 Enhanced Face Recognition Server")
            print(f"📁 Serving from: {script_dir}")
            print(f"🔒 HTTPS server running at: https://localhost:{port}")
            print(f"💾 Record saving: ENABLED")
            print(f"📝 Records will be saved to: Record/Local.json")
            print(f"🎯 Punch-in records will be saved to: Record/Punch_in.json")
            print(f"🔴 Punch-out records will be saved to: Record/Punch_out.json")
            print(f"👥 Currently online records will be saved to: Record/Currently_online.json")
            print(f"\n✨ Features:")
            print(f"   - Static file serving (HTML, JS, images, models)")
            print(f"   - POST /save-records endpoint for saving recognition data")
            print(f"   - POST /save-punch-in endpoint for saving punch-in data")
            print(f"   - POST /save-punch-out endpoint for saving punch-out data")
            print(f"   - POST /save-currently-online endpoint for online status")
            print(f"   - Automatic timestamped backups")
            print(f"   - CORS headers for local development")
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
            print(f"❌ Port {port} is already in use")
            return False
        else:
            print(f"❌ Server error: {e}")
            return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    port = 8000
    if len(sys.argv) > 1:
        try:
            port = int(sys.argv[1])
            if not (1024 <= port <= 65535):
                raise ValueError("Port must be between 1024 and 65535")
        except ValueError as e:
            print(f"❌ Invalid port: {e}")
            print(f"Usage: python enhanced_server.py [port]")
            sys.exit(1)
    
    print("🎯 Enhanced Face Recognition Server Starting...")
    
    success = start_enhanced_server(port)
    if success:
        print("👋 Thanks for using Face Recognition App!")
    else:
        print("❌ Failed to start the server")
        sys.exit(1)
