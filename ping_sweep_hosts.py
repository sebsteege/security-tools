import datetime
import ipaddress
from ping3 import ping

print('Enter the text file of hosts you would like to ping:')
host_file = input()
print('Enter the name of the output file:')
output_file = input()

def ping_sweep(host_file):

    with open(host_file) as file:
        for ip in file:
            ip = ip.strip()
            address = ipaddress.ip_address(ip)
            for value in ip.split():
                try:
                    response_time = ping(ip, timeout=1)
                    if response_time is not None:
                        message = f"{ip} reachable"
                    else:
                        message = f"{ip} unreachable"
                except Exception:
                    message = f"Error pinging {ip}"
                print(message)

ping_sweep(host_file)