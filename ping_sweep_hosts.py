import datetime
import ipaddress
from ping3 import ping

print('Enter the hosts you would like to ping:')
host_file = input()
print('Enter the name of the output file:')
output_file = input()

def ping_sweep(subnet):
    network = ipaddress.ip_network(subnet, strict=False)

    with open(host_file) as file:
         for line in file:
             for value in line.split():
                 print(value)

test