#!/usr/bin/env python3
"""
Extract Tor-related IPs from Suricata rules and format them for Kusto.

Author: Adair John Collins (X: @AdairJCollins)
Revision: 2025-08-24
"""

import re
import requests
import argparse
import logging
from collections import defaultdict
from pathlib import Path

# 📝 Logging setup
logging.basicConfig(
    filename="tor_ip_extractor.log",
    level=logging.ERROR,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

DEFAULT_URL = "https://rules.emergingthreats.net/open/suricata-7.0.3/rules/tor.rules"


def fetch_rules_from_url(url: str, verbose: bool = True) -> str:
    """Download rules from a remote URL with error handling."""
    try:
        if verbose:
            print(f'// 📡 Fetching rules from: {url}')
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        if not response.text.strip():
            raise ValueError("Downloaded file is empty.")

        return response.text

    except requests.Timeout:
        logging.error("Request timed out.")
        raise SystemExit("// ❌ Request timed out. Check your internet connection.")
    except requests.ConnectionError:
        logging.error("Connection error.")
        raise SystemExit("// ❌ Connection error. Unable to reach the server.")
    except requests.HTTPError as http_err:
        logging.error(f"HTTP error: {http_err}")
        raise SystemExit(f"// ❌ HTTP error: {http_err}")
    except Exception as exc:
        logging.error(f"Unexpected error: {exc}")
        raise SystemExit(f"// ❌ Failed to fetch rules: {exc}")


def read_rules_from_file(file_path: str, verbose: bool = True) -> str:
    """Read rules from a local file with error handling."""
    try:
        path = Path(file_path)
        if not path.is_file():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = path.read_text(encoding="utf-8")
        if not content.strip():
            raise ValueError(f"Local file is empty: {file_path}")

        if verbose:
            print(f'// 📁 Reading rules from local file: {file_path}')
        return content

    except Exception as exc:
        logging.error(f"File read error: {exc}")
        raise SystemExit(f"// ❌ Error reading file: {exc}")


def extract_ips_and_messages(rules_text: str) -> dict:
    """Extract IPs and associated msg descriptions from rules."""
    msg_pattern = re.compile(r'msg:"([^"]+)"')
    bracket_pattern = re.compile(r'\[([^\]]+)\]')
    paren_pattern = re.compile(r'\(([^)]+)\)')

    msg_ip_map = defaultdict(list)

    for line in rules_text.splitlines():
        msg_match = msg_pattern.search(line)
        ip_match = bracket_pattern.search(line) or paren_pattern.search(line)

        if msg_match and ip_match:
            msg = msg_match.group(1)
            raw_ips = ip_match.group(1).split(',')
            ips = [
                ip.strip()
                for ip in raw_ips
                if re.match(r'\d+\.\d+\.\d+\.\d+', ip.strip())
            ]
            msg_ip_map[msg].extend(ips)

    return msg_ip_map


def format_kusto_datatable(msg_ip_map: dict) -> str:
    """Format extracted IPs into a Kusto datatable block without blank lines."""
    output_lines = ["let TorIPs = datatable(IP: string)\n["]
    for msg, ips in msg_ip_map.items():
        if not ips:
            continue
        output_lines.append(f'    // msg: "{msg}"')
        for ip in ips:
            output_lines.append(f'    "{ip}",')
    output_lines.append("];")
    return "\n".join(output_lines)


def main():
    """Main execution function with CLI support."""
    parser = argparse.ArgumentParser(
        description="Extract Tor IPs from Suricata rules and format for Kusto.",
        epilog=(
            "Examples:\n"
            "  python tor_ip_extractor.py -f tor.rules -o tor_ips.kql\n"
            "  python tor_ip_extractor.py -u https://yourdomain.com/custom.rules\n"
            "  python tor_ip_extractor.py -d -o tor_ips.kql"
        ),
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-u", "--url", help="URL of the Suricata rules file")
    parser.add_argument("-f", "--file", help="Path to a local Suricata rules file")
    parser.add_argument("-d", "--download", action="store_true", help="Download Tor rules from the default Emerging Threats URL")
    parser.add_argument("-o", "--output", help="Path to save the processed Kusto-formatted IPs")

    args = parser.parse_args()

    if not args.file and not args.url and not args.download:
        parser.print_help()
        raise SystemExit("\n// ❌ No input source provided. Use -f, -u, or -d.\n")

    try:
        verbose = not args.output  # Only print status messages if not writing to file

        if args.file:
            rules_text = read_rules_from_file(args.file, verbose=verbose)
        elif args.url:
            rules_text = fetch_rules_from_url(args.url, verbose=verbose)
        elif args.download:
            rules_text = fetch_rules_from_url(DEFAULT_URL, verbose=verbose)
        else:
            raise SystemExit("// ❌ No valid input source found.")

        msg_ip_map = extract_ips_and_messages(rules_text)
        kusto_output = format_kusto_datatable(msg_ip_map)

        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(kusto_output + "\n")
                print(f"// ✅ Output written to: {args.output}")
            except Exception as exc:
                logging.error(f"Failed to write output file: {exc}")
                raise SystemExit("// ❌ Could not write to output file.")
        else:
            print(kusto_output)

    except Exception as exc:
        logging.error(f"Unhandled exception: {exc}")
        raise SystemExit("// ❌ Script failed. Check tor_ip_extractor.log for details.")


if __name__ == "__main__":
    main()
