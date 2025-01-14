from datetime import datetime
import ipaddress
from ping3 import ping

print()
print('Enter the text file of hosts you would like to ping:')
host_file = input()
print()
print('Enter the name of the output file:')
output_file = input()
print()

def ping_sweep(host_file):

    with open(host_file) as file, open(output_file, "w") as outfile:
        for line in file:
            ip_or_cidr = line.strip()
            try:
                address = ipaddress.ip_address(ip_or_cidr)
                response_time = ping(str(address), timeout=1)
                if response_time is not None:
                    message = f"{address} reachable\n"
                else:
                    message = f"{address} unreachable\n"
                outfile.write(message)
                print(message)
            except ValueError:
                try:
                    network = ipaddress.ip_network(ip_or_cidr, strict=False)
                    for host in network.hosts():
                        response_time = ping(str(host), timeout=1)
                        if response_time is not None:
                            message = f"{host} reachable\n"
                        else:
                            message = f"{host} unreachable\n"
                        outfile.write(message)
                        print(message)
                except ValueError:
                    message = f"Error pinging {host}\n"
                    outfile.write(message)
                    print(message)

now = datetime.now()
formatted_now = now.strftime("%Y-%m-%d %H:%M:%S")
print(formatted_now)
print()
ping_sweep(host_file)