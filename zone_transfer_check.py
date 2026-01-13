#!/usr/bin/env python3

import subprocess
import sys
import os
import shutil
import argparse
from urllib.parse import urlparse

# Colors
RED    = "\033[91m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
WHITE  = "\033[97m"
RESET  = "\033[0m"

USE_COLOR = True

# Cloud / managed DNS patterns that will NEVER allow AXFR
SKIP_NS_PATTERNS = [
    "awsdns-",
    "cloudflare.com",
    "cloudfront.net",
    "azure-dns",
    "google",
    "googledomains",
    "akamai",
    "akamaitech",
    "edgekey.net",
    "fastly",
]

def c(text, color):
    if not USE_COLOR:
        return text
    return color + text + RESET

def banner():
    os.system("clear")
    print(c("""
╔══════════════════════════════════════╗
║         AXFR ZONE SCANNER            ║
║   Smart Filter + Zone Discovery      ║
╚══════════════════════════════════════╝
""", CYAN))

def check_dependencies():
    if not shutil.which("dig"):
        print(c("[!] 'dig' not found. Install: apt install dnsutils", RED))
        sys.exit(1)

def normalize_domain(target):
    target = target.strip()

    if target.startswith("http://") or target.startswith("https://"):
        parsed = urlparse(target)
        return parsed.netloc

    if "/" in target:
        return target.split("/")[0]

    return target

def load_domains(args):
    targets = []

    if args.u:
        targets.append(normalize_domain(args.u))

    if args.f:
        if not os.path.isfile(args.f):
            print(c("[!] File not found", RED))
            sys.exit(1)
        with open(args.f, "r", errors="ignore") as f:
            for line in f:
                d = line.strip()
                if d and not d.startswith("#"):
                    targets.append(normalize_domain(d))

    return list(set(targets))

def get_parent_domains(domain):
    parts = domain.split(".")
    parents = []
    for i in range(len(parts) - 1):
        parents.append(".".join(parts[i:]))
    return parents

def get_nameservers(domain, timeout, silent):
    if not silent:
        print(c(f"[*] Fetching NS for {domain}", CYAN))

    try:
        result = subprocess.check_output(
            ["dig", "NS", domain, "+short"],
            stderr=subprocess.STDOUT,
            timeout=timeout
        )

        ns_list = []

        for line in result.decode(errors="ignore").splitlines():
            line = line.strip().rstrip(".")

            if not line:
                continue

            bad = [";", "timed out", "error", "connection", "communications"]
            if any(x in line.lower() for x in bad):
                continue

            if " " in line:
                continue

            ns_list.append(line.lower())

        return ns_list

    except:
        return []

def is_managed_dns(ns):
    ns = ns.lower()
    for pat in SKIP_NS_PATTERNS:
        if pat in ns:
            return True
    return False

def try_zone_transfer(domain, ns, timeout, outdir, silent):
    if is_managed_dns(ns):
        if not silent:
            print(c(f"[*] Skipping managed DNS: {ns}", CYAN))
        return False

    if not silent:
        print(c(f"[*] Trying AXFR: {domain} @ {ns}", YELLOW))

    try:
        result = subprocess.check_output(
            ["dig", "AXFR", "@"+ns, domain],
            stderr=subprocess.STDOUT,
            timeout=timeout
        )

        output = result.decode(errors="ignore")

        if "Transfer failed" in output or "XFR size" not in output or "connection timed out" in output.lower():
            if not silent:
                print(c("[-] AXFR failed", RED))
            return False

        print(c(f"[VULN] AXFR SUCCESS: {domain} @ {ns}", RED))

        if outdir:
            os.makedirs(outdir, exist_ok=True)
            fname = f"{domain}_{ns}.txt".replace("/", "_")
            path = os.path.join(outdir, fname)
            with open(path, "w") as f:
                f.write(output)
            print(c(f"[+] Saved: {path}", GREEN))

        return True

    except:
        if not silent:
            print(c("[-] AXFR error / refused / timeout", RED))
        return False

def main():
    global USE_COLOR

    parser = argparse.ArgumentParser(description="AXFR Zone Transfer Scanner (Smart + Filtered)")
    parser.add_argument("-u", help="Single domain or URL")
    parser.add_argument("-f", help="File with domains or URLs")
    parser.add_argument("-o", help="Output directory")
    parser.add_argument("-t", type=int, default=15, help="Timeout (default: 15)")
    parser.add_argument("-v", action="store_true", help="Show only vulnerable results")
    parser.add_argument("--no-color", action="store_true", help="Disable colors")

    args = parser.parse_args()

    if not args.u and not args.f:
        parser.print_help()
        sys.exit(1)

    if args.no_color:
        USE_COLOR = False

    silent = args.v

    if not silent:
        banner()

    check_dependencies()

    targets = load_domains(args)

    if not silent:
        print(c(f"[+] Loaded {len(targets)} targets", CYAN))

    vulnerable = set()
    tested_zones = set()

    for target in targets:
        if not target:
            continue

        parent_list = get_parent_domains(target)

        if not silent:
            print(c(f"\n===== Scanning target: {target} =====", WHITE))

        for domain in parent_list:
            if domain in tested_zones:
                continue

            tested_zones.add(domain)

            if not silent:
                print(c(f"\n--- Testing zone candidate: {domain} ---", CYAN))

            nss = get_nameservers(domain, args.t, silent)
            if not nss:
                continue

            for ns in nss:
                if try_zone_transfer(domain, ns, args.t, args.o, silent):
                    vulnerable.add(domain)

    if not silent:
        print(c("\n========== SUMMARY ==========", WHITE))

    if vulnerable:
        for d in sorted(vulnerable):
            print(c(f"[VULN] {d}", RED))
    else:
        if not silent:
            print(c("[✓] No vulnerable domains found", GREEN))

    if not silent:
        print(c("\n[*] Scan complete", CYAN))

if __name__ == "__main__":
    main()

