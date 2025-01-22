import json
import os
import ipaddress
import socket
import sys

def load_ips(file_path):
    """Load IPv4 addresses from JSON file."""
    if not os.path.exists(file_path):
        print(f"\nError: Input file '{file_path}' not found.")
        print("Please run the reconHostIps first, before executing this scan.\n")
        sys.exit(1) # Exit the script with an error code
    with open(file_path, "r") as file:
        data = json.load(file)
    return data


def scan_port(ip, port):
    """Check if a port is open on the IPv4 addresses."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1) # Timeout for connection
            if sock.connect_ex((ip, port)) == 0:
                return True
    except socket.error:
        pass
    return False


def scan_cidr_block(ip, ports_to_scan=range(1, 1025)):
    """Scan the /24 CIDR block of the IP for open ports."""
    network = ipaddress.ip_network(f"{ip}/24", strict=False)
    print(f"\nScanning network: {network}")
    open_ports = {}

    for host in network.hosts(): # Repeat over all hosts in the network
        # Skip localhost (127.0.0.0/8 network)
        if ipaddress.ip_address(host).is_loopback:
            print(f"\nSkipping localhost IP: {host}")
            continue

        for port in ports_to_scan:
            if scan_port(str(host), port):
                if str(host) not in open_ports:
                    open_ports[str(host)] = []
                open_ports[str(host)].append(port)
                print(f"Open port found: {host}:{port}")
    return open_ports


def save_results_to_file(results, file_path):
    """Save scan artifacts to a JSON file"""
    os.makedirs(os.path.dirname(file_path), exist_ok=True) # Ensure dir exists
    with open(file_path, "w") as file:
        json.dump(results, file, indent=4)
    print(f"\nScan artifacts saved to {file_path}")


def main():
    input_file = "artifacts/localHostIps.json"
    output_file = "artifacts/scanOfHostIps.json"
    ports_to_scan = range(1, 1025) # Common ports (1-1024)

    print(f"Loading IPs from {input_file}...")
    data = load_ips(input_file)

    scan_results = {}
    for interface, addresses in data.items():
        print(f"\nScanning interface: {interface}")
        for addr_info in addresses:
            if addr_info["type"] == "IPv4":
                ip = addr_info["address"]
                print(f"Scanning IP: {ip}")
                results = scan_cidr_block(ip, ports_to_scan)
                scan_results[ip] = results

    # Save the artifacts to a file
    save_results_to_file(scan_results, output_file)


if __name__ == "__main__":
    main()