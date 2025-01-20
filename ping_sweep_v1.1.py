from datetime import datetime
import ipaddress
from ping3 import ping
from concurrent.futures import ThreadPoolExecutor

print()
print('Enter the text file of hosts you would like to ping:')
host_file = input()
print()
print('Enter the name of the output file:')
output_file = input()
print()

def ping_host(host):

    try:
        response_time = ping(host, timeout=1)
        if response_time is not None:
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
        results = executor.map(ping_host, tasks)
        for result in results:
            outfile.write(result)
            print(result)

now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_now)
print()
ping_sweep(host_file, output_file, max_threads=100)