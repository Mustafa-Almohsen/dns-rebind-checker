#!/usr/bin/env python3
import dns.resolver
import ipaddress
import sys
import time
import argparse
from rich.console import Console
console = Console()
from rich.table import Table
from pyfiglet import Figlet


BANNER = r"""
 ______   _        _______    _______  _______  ______  _________
(  __  \ ( (    /|(  ____ \  (  ____ )(  ____ \(  ___ \ \__   __/
| (  \  )|  \  ( || (    \/  | (    )|| (    \/| (   ) )   ) (
| |   ) ||   \ | || (_____   | (____)|| (__    | (__/ /    | |
| |   | || (\ \) |(_____  )  |     __)|  __)   |  __ (     | |
| |   ) || | \   |      ) |  | (\ (   | (      | (  \ \    | |
| (__/  )| )  \  |/\____) |  | ) \ \__| (____/\| )___) )___) (___
(______/ |/    )_)\_______)  |/   \__/(_______/|/ \___/ \_______/

( (    /|(  __  \   (  ____ \|\     /|(  ____ \(  ____ \| \    /\
|  \  ( || (  \  )  | (    \/| )   ( || (    \/| (    \/|  \  / /
|   \ | || |   ) |  | |      | (___) || (__    | |      |  (_/ /
| (\ \) || |   | |  | |      |  ___  ||  __)   | |      |   _ (
| | \   || |   ) |  | |      | (   ) || (      | |      |  ( \ \
| )  \  || (__/  )  | (____/\| )   ( || (____/\| (____/\|  /  \ \
|/    )_)(______/   (_______/|/     \|(_______/(_______/|_/    \/

                      DNS Rebdind Check
                  Mustafa-Almohsen
"""


def is_private_ip(ip):
    try:
        return ipaddress.ip_address(ip).is_private or \
               ipaddress.ip_address(ip).is_loopback or \
               ipaddress.ip_address(ip).is_link_local
    except:
        return False

def check_dns(domain, attempts=5, delay=3):
    console.print(f"\n[bold cyan]🔍 Checking domain:[/bold cyan] {domain}\n{'-'*40}")
    resolver = dns.resolver.Resolver()
    resolver.lifetime = 3

    seen_ips = set()
    private_seen = False
    suspicious_ttl = False

    for i in range(attempts):
        try:
            answers = resolver.resolve(domain, "A")
            ips = [str(rdata) for rdata in answers]
            ttl = answers.rrset.ttl

            console.print(f"[Attempt {i+1}] TTL={ttl} IPs={ips}", style="dim")

            for ip in ips:
                if is_private_ip(ip):
                    private_seen = True
                seen_ips.add(ip)

            if ttl <= 10:
                suspicious_ttl = True

        except Exception as e:
            console.print(f"[Attempt {i+1}] ❌ Error: {e}", style="red")

        time.sleep(delay)

    console.print("\n[bold]✅ Summary:[/bold]")
    if private_seen:
        console.print("🔴 [bold red]Potential DNS rebinding detected! (Private IPs returned)[/bold red]")
    elif suspicious_ttl:
        console.print("🟡 [yellow]Suspiciously low TTLs detected (could enable rebinding).[/yellow]")
    else:
        console.print("🟢 [green]No rebinding indicators. Likely normal CDN/load balancing.[/green]")

    console.print(f"Unique IPs seen: {seen_ips}\n{'='*40}")

def main():
    parser = argparse.ArgumentParser(description="DNS rebinding detector")
    parser.add_argument("-d", "--domain", help="Single domain to test")
    parser.add_argument("-l", "--list", help="File with list of domains (one per line)")
    parser.add_argument("-n", "--attempts", type=int, default=5, help="Number of attempts per domain")
    parser.add_argument("-t", "--delay", type=int, default=3, help="Delay between attempts (seconds)")
    args = parser.parse_args()



    console.print(BANNER, style="bold cyan")


    domains = []
    if args.domain:
        domains.append(args.domain)
    if args.list:
        with open(args.list) as f:
            domains.extend([line.strip() for line in f if line.strip()])

    if not domains:
        console.print("❌ [red]You must provide a domain (-d) or list (-l).[/red]")
        sys.exit(1)

    for d in domains:
        check_dns(d, attempts=args.attempts, delay=args.delay)

if __name__ == "__main__":
    main()
