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
            address = ipaddress.ip_address(ip.strip()) # strip newline \n from address
            for value in ip.split():
                    print(value)

ping_sweep(host_file)