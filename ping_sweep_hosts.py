import datetime
import ipaddress
from ping3 import ping

print('Enter the text file of hosts you would like to ping:')
host_file = input()
print('Enter the name of the output file:')
output_file = input()

def ping_sweep(host_file):

    with open(host_file) as file:
        for line in file:
            ip_or_cidr = line.strip()
            try:
                address = ipaddress.ip_address(ip_or_cidr)
                response_time = ping(str(address), timeout=1)
                if response_time is not None:
                    message = f"{address} reachable"
                else:
                    message = f"{address} unreachable"
                print(message)
            except ValueError:
                try:
                    network = ipaddress.ip_network(ip_or_cidr, strict=False)
                    for host in network.hosts():
                        response_time = ping(str(host), timeout=1)
                        if response_time is not None:
                            message = f"{host} reachable"
                        else:
                            message = f"{host} unreachable"
                        print(message)
                except ValueError:
                    message = f"Error pinging {host}"
                print(message)
                
ping_sweep(host_file)