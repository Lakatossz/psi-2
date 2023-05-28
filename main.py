import socket
import struct
import subprocess

from pysnmp.hlapi import *

ipAdEntAddr = "1.3.6.1.2.1.4.24.1.4"

SNMP_PORT = 161


def mib_category(host):
    iterator = bulkCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=1),
        UdpTransportTarget((host, SNMP_PORT)),
        ContextData(),
        0, 50,
        ObjectType(ObjectIdentity(ipAdEntAddr)),
        lexicographicMode=False
    )

    varBinds = next(iterator)
    print(varBinds[0])


def get_mib_category(host, category):
    end = category[:-1] + str((int(category[-1]) + 1))
    print(end)

    my_cmd = f"snmpwalk -c PSIPUB -v1 -CE {end} {host} {category}"
    run_my_cmd = subprocess.run(my_cmd, shell=True, capture_output=True)

    return run_my_cmd.stdout.decode().splitlines()


def default_gateway():
    with open("/proc/net/route") as file_header:
        for line_values in file_header:
            values = line_values.strip().split()
            if values[1] != '00000000' or not int(values[3], 16) & 2:
                # If not default route or not RTF_GATEWAY, skip it
                continue

            return socket.inet_ntoa(struct.pack("<L", int(values[2], 16)))


def parse_value(value):
    split_values = str.split(value, sep=" ")

    return split_values[-1]


def apply_mask(network, mask):
    network_list = str(network).split(sep=".")
    mask_list = str(mask).split(sep=".")

    for i in range(0, len(network_list)):
        temp = int(mask_list[i]) & int(network_list[i])
        network_list[i] = str(temp)

    return f"{network_list[0]}.{network_list[1]}.{network_list[2]}.{network_list[3]}"


def get_mask(mask):
    number_of_mask = 0
    mask = str(mask).split(sep=".")

    for i in range(0, 4):
        mask_byte = int(mask[i])

        if mask_byte == 255:
            number_of_mask += 8
        else:
            while mask_byte & 128 > 0:
                number_of_mask += 1
                mask_byte = mask_byte << 1
            break
    return number_of_mask


def network_with_mask(addr, mask):
    current_mask = get_mask(mask)
    if current_mask == 0 or current_mask == 32:
        return ""

    return f"{apply_mask(addr, mask)}/{current_mask}"

print("Start scanning...")

visited = []
to_visit = [default_gateway()]

visited_networks = []

to_visit_new_level = []


print("Scanning done.")
