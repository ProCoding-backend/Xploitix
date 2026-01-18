from playwright.sync_api import sync_playwright
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
import time
import json

console = Console()

def web_proxy_inspector():
    console.print(Panel(Align.center("Web Proxy Inspector Running", vertical="middle"), style="bold yellow"))
    url = console.input("[#abeb34]Enter Website URL: [/#abeb34]")

    requests_log = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        def handle_request(req):
            if req.resource_type in ["xhr", "fetch"]:
                requests_log.append({
                    "url": req.url,
                    "method": req.method,
                    "headers": req.headers,
                    "post_data": req.post_data
                })

        def handle_response(res):
            for r in requests_log:
                if r["url"] == res.url:
                    try:
                        r["status"] = res.status
                        r["response"] = res.text()
                    except:
                        r["response"] = "Binary / Empty"

        page.on("request", handle_request)
        page.on("response", handle_response)

        page.goto(url)
        time.sleep(10)
        browser.close()

    table = Table(title="Captured XHR / Fetch Requests")
    table.add_column("No", justify="center")
    table.add_column("Method")
    table.add_column("URL", overflow="fold")

    for i, r in enumerate(requests_log, 1):
        table.add_row(str(i), r["method"], r["url"])

    console.print(table)

    choice = int(console.input("\n[#ffcc00]Select Request Number: [/#ffcc00]")) - 1
    option = console.input("[#ff6666]1.Response  2.Payload → [/#ff6666]")

    selected = requests_log[choice]

    if option == "1":
        content = selected.get("response", "No Response")
        console.print(Panel(content[:5000], title="Response", style="cyan"))
    else:
        payload = selected.get("post_data") or "No Payload"
        console.print(Panel(payload, title="Payload", style="green"))


