from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
from mitmproxy import http
from mitmproxy.tools.dump import DumpMaster
from mitmproxy.options import Options
import threading
import time

console = Console()
requests_log = []

class WebProxyAddon:
    def request(self, flow: http.HTTPFlow):
        if flow.request.headers.get("content-type", "").startswith(("application/json", "application/x-www-form-urlencoded")):
            requests_log.append({
                "method": flow.request.method,
                "url": flow.request.url,
                "headers": dict(flow.request.headers),
                "post_data": flow.request.get_text(),
                "status": None,
                "response": None
            })

    def response(self, flow: http.HTTPFlow):
        for r in requests_log:
            if r["url"] == flow.request.url:
                r["status"] = flow.response.status_code
                try:
                    r["response"] = flow.response.get_text()
                except:
                    r["response"] = "Binary / Empty"


def start_proxy():
    opts = Options(listen_host="0.0.0.0", listen_port=8080)
    m = DumpMaster(opts, with_termlog=False, with_dumper=False)
    m.addons.add(WebProxyAddon())
    m.run()


def web_proxy_inspector():
    console.print(
        Panel(
            Align.center("Web Proxy Inspector Running\nProxy: 127.0.0.1:8080", vertical="middle"),
            style="bold yellow"
        )
    )

    t = threading.Thread(target=start_proxy, daemon=True)
    t.start()

    console.print("[green]▶ Set your browser proxy to 127.0.0.1 : 8080")
    console.print("[green]▶ Open the website manually and browse")
    console.print("[yellow]▶ Capturing for 20 seconds...\n")

    time.sleep(20)

    table = Table(title="Captured Requests")
    table.add_column("No", justify="center")
    table.add_column("Method")
    table.add_column("URL", overflow="fold")

    for i, r in enumerate(requests_log, 1):
        table.add_row(str(i), r["method"], r["url"])

    console.print(table)

    if not requests_log:
        console.print("[red]No requests captured.")
        return

    choice = int(console.input("\n[#ffcc00]Select Request Number: [/#ffcc00]")) - 1
    option = console.input("[#ff6666]1.Response  2.Payload → [/#ff6666]")

    selected = requests_log[choice]

    if option == "1":
        console.print(Panel(selected.get("response", "No Response"), title="Response", style="cyan"))
    else:
        console.print(Panel(selected.get("post_data") or "No Payload", title="Payload", style="green"))
