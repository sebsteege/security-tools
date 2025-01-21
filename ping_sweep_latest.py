from datetime import datetime
import platform
import ipaddress
import subprocess
from concurrent.futures import ThreadPoolExecutor

"""
This script is used to ping host.
Enter the full path to your hosts file if it exists in
another directory.
"""

print()
print('Enter the text file of hosts you would like to ping:')
host_file = input()
print()
print('Enter the name of the output file:')
output_file = input()
print()

def ping_host_windows(host):

    try:
        result = subprocess.run(['ping', '-n', '4', host], stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
        if "Destination host unreachable" in result.stdout:
            return f"{host} unreachable\n"
        elif "Request timed out" in result.stdout:
            return f"{host} unreachable\n"
        elif "transmit failed" in result.stdout:
            return f"{host} unreachable\n"
        elif "TTL expired in transit" in result.stdout:
            return f"{host} unreachable\n"
        else:
            return f"{host} reachable\n"
    except Exception:
        return f"Error pinging {host}\n"

def ping_host_linux(host):

    try:
        result = subprocess.run(['ping', '-c', '4', '-n', host], stdout=subprocess.DEVNULL, encoding='utf-8')
        if result is not None:
            return f"{host} reachable\n"
        else:
            return f"{host} unreachable\n"
    except Exception:
        return f"Error pinging {host}\n"

def ping_sweep(host_file, output_file, max_threads=10):

    tasks = []
    with open(host_file) as file:
        for line in file:
            ip_or_cidr = line.strip()
            try:
                address = ipaddress.ip_address(ip_or_cidr)
                tasks.append(str(address))
            except ValueError:
                try:
                    network = ipaddress.ip_network(ip_or_cidr, strict=False)
                    tasks.extend(str(host) for host in network.hosts())
                except ValueError:
                    print(f"Invalid input: {ip_or_cidr}")

    with ThreadPoolExecutor(max_threads) as executor, open(output_file, "w") as outfile:
        if platform.system().lower()=='linux':
            results = executor.map(ping_host_linux, tasks)
        elif platform.system().lower()=='windows':
            results = executor.map(ping_host_windows, tasks)
        for result in results:
            outfile.write(result)
            print(result)

now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_now)
print()
ping_sweep(host_file, output_file, max_threads=100)