import json
import os
import ipaddress
import socket
import sys


def load_ips(file_path):
    """Load IP address from artifacts/localHostIps.json file."""
    if not os.path.exists(file_path):
        print(f"\nError: Input file '{file_path}' not found.")
        print("Please run the reconHostIps module first, before executing the scan.\n")
        sys.exit(1)  # Exit the script if reconHostIps module has not been executed
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def scan_port(ip, port, is_ipv6=False):
    """Check if a port is open on a given IP address."""
    family = socket.AF_INET6 if is_ipv6 else socket.AF_INET
    try:
        with socket.socket(family, socket.SOCK_STREAM) as sock:
            sock.settimeout(1)  # Timeout for connection
            if sock.connect_ex((ip, port)) == 0:
                return True
    except socket.error:
        pass
    return False


def scan_cidr_block(ip, ports_to_scan=range(1, 1025), is_ipv6=False):
    """Scan the /24 CIDR block of an IP for open ports."""
    network = ipaddress.ip_network(f"{ip}/24", strict=False)
    print(f"\nScanning network: {network}\n")
    open_ports = {}

    for host in network.hosts(): # Repeat over all hosts in the network
        for port in ports_to_scan:
            if scan_port(str(host), port, is_ipv6):
                if str(host) not in open_ports:
                    open_ports[str(host)] = []
                open_ports[str(host)].append(port)
                print(f"Open port found: {host}:{port}")
    return open_ports


def save_results_to_file(results, file_path):
    """Save scan artifacts to a JSON file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # Confirming artifacts dir exists
    with open(file_path, "w") as file:
        json.dump(results, file, indent=4)
    print(f"\nScan artifacts saved to {file_path}")


def main():
    input_file = "artifacts/localHostIps.json"
    output_file = "artifacts/scanOfHostIps.json"
    ports_to_scan = range(1, 1025) # Common ports (1-1024)

    print(f"\nChecking for input file: {input_file}...\n")
    data = load_ips(input_file)

    scan_results = {}
    for interface, addresses in data.items():
        print(f"\nScanning interface: {interface}")
        for addr_info in addresses:
            ip_type = addr_info["type"]
            ip = addr_info["address"]

            if ip_type == "IPv4":
                print(f"Scanning IPv4: {ip}")
                results = scan_cidr_block(ip, ports_to_scan, is_ipv6=False)
                scan_results[ip] = results

            elif ip_type == "IPv6":
                print(f"Scanning IPv6: {ip}")
                results = scan_cidr_block(ip, ports_to_scan, is_ipv6=True)
                scan_results[ip] = results

    # Save the artifactsa to artifacts/scanOfHostIps.json file
    save_results_to_file(scan_results, output_file)


if __name__ == "__main__":
    main()