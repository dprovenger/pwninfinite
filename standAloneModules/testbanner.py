import json
import socket
import os

def load_scan_results(file_path):
    """Load scan results from a JSON file."""
    with open(file_path, "r") as file:
        return json.load(file)

def grab_banner(ip, port):
    """Attempt to connect to a port and retrieve a banner."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)  # Set timeout for the connection
            sock.connect((ip, port))
            # Try to retrieve a banner
            sock.sendall(b"\r\n")
            banner = sock.recv(1024).decode("utf-8", errors="ignore").strip()
            return banner or "Unknown Service (no banner)"
    except (socket.timeout, ConnectionRefusedError, OSError):
        return "Unknown Service (no response)"

def identify_services(ip, ports):
    """Identify services running on the given ports for a specific IP."""
    services = {}
    for port in ports:
        print(f"    Connecting to {ip}:{port}...")
        service = grab_banner(ip, port)
        services[port] = service
    return services

def main():
    input_file = "artifacts/scanOfHostIps.json"
    output_file = "artifacts/service_identification.json"

    print(f"Loading scan results from {input_file}...")
    if not os.path.exists(input_file):
        print(f"Error: File {input_file} does not exist.")
        return

    scan_results = load_scan_results(input_file)
    identified_services = {}

    for source_ip, target_data in scan_results.items():
        print(f"\nProcessing source IP: {source_ip}")
        identified_services[source_ip] = {}
        for target_ip, ports in target_data.items():
            print(f"  Analyzing target IP: {target_ip}")
            if ports:
                services = identify_services(target_ip, ports)
                identified_services[source_ip][target_ip] = services
                print(f"    Found services: {services}")
            else:
                print(f"    No open ports found for {target_ip}")

    # Save the identified services to a file
    print(f"\nSaving identified services to {output_file}...")
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w") as file:
        json.dump(identified_services, file, indent=4)

if __name__ == "__main__":
    main()
