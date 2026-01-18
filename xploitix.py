import importlib.util
import subprocess
import sys
import os
import time
import random

required_libs = [
    "pyfiglet",
    "rich",
    "requests",
    "pyngrok",
    "psutil",
    "playwright",
]

for lib in required_libs:
    if importlib.util.find_spec(lib) is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", lib])

# Ensure Playwright browsers are installed when the package is available
try:
    if importlib.util.find_spec('playwright') is not None:
        print('Ensuring Playwright browsers are installed (this may take a while)...')
        subprocess.check_call([sys.executable, "-m", "playwright", "install"])
except Exception as _e:
    # Non-fatal: continue even if install fails here
    print('Warning: failed to run `playwright install` automatically.')

import pyfiglet


colors = [
    "\033[1;31m",
    "\033[1;32m",
    "\033[1;33m",
    "\033[1;34m",
    "\033[1;35m",
    "\033[1;36m"
]

fonts = ["starwars", "slant", "big"]

ascii_art = pyfiglet.figlet_format("Xploitix", font=random.choice(fonts))
chosen_color = random.choice(colors)

for ch in ascii_art:
    if ch not in (" ", "\n"):
        print(chosen_color + ch + "\033[0m", end="", flush=True)
        time.sleep(0.002)
    else:
        print(ch, end="")

print("\n")
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.text import Text
def frame(eyes="^ ^", bold=True):
    style = "bold yellow3" if bold else "yellow3"
    t = Text()
    t.append("   /|_/|\n", style)
    t.append("  / ", style)
    t.append(eyes, "bold red")
    t.append("(_o\n", style)
    t.append(" /    __.'\n", style)
    t.append(" /     \\\n", style)
    t.append("(_) (_) '._\n", style)
    t.append("  '.__     '. .-''-'.\n", style)
    t.append("     ( '.   ('.____.''\n", style)
    t.append("     _) )'_, )mrf\n", style)
    t.append("    (__/ (__/\n", style)
    t.append("\n", style)
    t.append("  Loading...\n", "bold red")
    return t

frames = [
    frame("^ ^", True),
    frame("- -", False),
    frame("^ ^", True),
    frame("o o", True)
]

with Live(frames[0], refresh_per_second=6) as live:
    for _ in range(2):
        for f in frames:
            live.update(f)
            time.sleep(0.55)

console = Console()

console.print(
    Panel(
        Align.center(
            "[bold cyan]Xploitix[/bold cyan]\n"
            '''[red]An Advanced Website Exploitation, Sniffer Framework
            Use ETHICALLY, I am not responsible for any illegal activities done with[/red]\n'''
            "[yellow]By: Pro-CodingBackend[/yellow]",
            vertical="middle"
        ),
        title="[bold magenta]Welcome to Xploitix[/bold magenta]",
        border_style="bright_blue"
    )
)

console.print(Align.left("[bold #00fc1d]Choose from Menu[/bold #00fc1d]"))
console.print(
    "[red][1] Web Proxy Inspector[/red]\n"
    "[yellow][2] Credential Stuffing Tool[/yellow]\n"
    "[blue][3] Location Tracking Tool[/blue]\n"
    "[green][4] Get Victim's IP Address[/green]\n"
    "[magenta][5] Exit Xploitix[/magenta]"
)

choice = console.input("[bold #00fc1d]Enter your choice: [/bold #00fc1d]")

if choice == "1":
    from Tools.web_proxy_inspector import web_proxy_inspector
    os.system("cls" if os.name == "nt" else "clear")
    web_proxy_inspector()

elif choice == "2":
    from Tools.credential_stuffing_tool import credential_stuffing_tool
    os.system("cls" if os.name == "nt" else "clear")
    credential_stuffing_tool()

elif choice == "3":
    from Tools.location_tracking_tool import location_tracking_tool
    os.system("cls" if os.name == "nt" else "clear")
    location_tracking_tool()

elif choice == "4":
    from Tools.get_victim_ip import get_victim_ip
    os.system("cls" if os.name == "nt" else "clear")
    get_victim_ip()

elif choice == "5":
    console.print("[bold red]Exiting Xploitix. Goodbye![/bold red]")
    sys.exit()

else:
    console.print("[bold red]Invalid choice[/bold red]")
    console.input("[bold #00fc1d]Press Enter to return...[/bold #00fc1d]")
