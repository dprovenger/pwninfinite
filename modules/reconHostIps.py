import psutil
import json
import socket

def get_ip_addresses():
    """Retrieve IPv4 and IPv6 IPs with associated interfaces"""
    ip_info = {}
    for interface, addrs in psutil.net_if_addrs().items():
        ip_info[interface] = []
        for addr in addrs:
            if addr.family == socket.AF_INET: # IPv4
                ip_info[interface].append({"type": "IPv4", "address": addr.address})
            elif addr.family == socket.AF_INET6: # IPv6
                ip_info[interface].append({"type": "IPv6", "address": addr.address})
    return ip_info

def save_to_json(data, file_path="artifacts/localHostIps.json"):
    """Save IP information to a JSON file"""
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)
    print(f"\nIP information saved to {file_path}\n")

def main():
    ip_info = get_ip_addresses()
    for interface, addresses in ip_info.items():
        print(f"Interface: {interface}")
        for addr in addresses:
            print(f"  {addr['type']}: {addr['address']}")

    save_to_json(ip_info)

if __name__ == "__main__":
    main()