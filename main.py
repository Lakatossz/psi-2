import math

from pysnmp.hlapi import *
from scapy.all import *

SNMP_PORT = 161  ## port pro SNMP
ipRouteDest = "1.3.6.1.2.1.4.21.1.1.2"  ## oid pro ipRouteDest
ipAdEntNetMask = "1.3.6.1.2.1.4.20.1.3.1.0"  ## oid pro ipRouteDest
ip = conf.route.route('0.0.0.0')[2]  ## default gateway zarizeni
community = 'PSIPUB'  ## Community rezetec site.


ips = []  ## Pole pro nacteni IP adres site.
found_ips = [] ## Nalezene IP adresy v

# Vypocita pocet bitu
def bit_count(self):
    return bin(self).count("1")


## Funkce pro vytvoreni pysnmp commandu.
def run_cmd(host, oid):
    return bulkCmd(SnmpEngine(),
                   CommunityData(community, mpModel=1),
                   UdpTransportTarget((host, SNMP_PORT), timeout=0.0, retries=0),
                   ContextData(),
                   0, 25,
                   ObjectType(ObjectIdentity(oid)))

# Vypocita pocet bytu subnetu
def count_subnet(ip, net_mask):
    last_ip = ip.split('.', 3)
    last_net_mask = net_mask.split('.', 3)
    bits = 0
    for j in range(4):
        bits += bit_count(int(last_net_mask[j]) - int(last_ip[j]))
    return bits


try:
    print('Starting scanning...')
    g = run_cmd(ip, ipRouteDest)  ## Vytvoreni SNMP prikazu.
    errorIndication, errorStatus, errorIndex, varBinds = next(g)  ## Spusteni prvni SNMP prikazu.
    temp = varBinds[0][-1].prettyPrint()  ## Ziskani prvni IP adresy.
    # print('nalezene IP v prvnim nodu:')
    while len(temp) > 1:  ## Pokud SNMP vraci IP adresy.
        ips.append(temp)  ## Pridam adresu do pole.
        # print('-> ' + str(temp))
        errorIndication, errorStatus, errorIndex, varBinds = next(g)  ## Dalsi spusteni
        ## Odchyceni chyb a jejich vypis.
        if errorIndication:
            print('errorIndication: ' + str(errorIndication) + ' (' + str(temp) + ')')
            continue
        elif errorStatus:
            print('errorStatus: ' + str(errorStatus) + ' (' + str(temp) + ')')
            continue
        elif errorIndex:
            print('errorIndex: ' + str(errorIndex) + ' (' + str(temp) + ')')
            continue
        else:
            temp = varBinds[0][-1].prettyPrint()
    ## Nyni se projdou vsechny nalezene zarizeni podle IP adres.
    for i in range(len(ips)):
        # print('nalezene IP v na IP: ' + ips[i])
        g = run_cmd(ips[i], ipRouteDest)
        for j in range(4):
            errorIndication, errorStatus, errorIndex, varBinds = next(g)
            if errorIndication:
                print('errorIndication: ' + str(errorIndication) + ' (' + str(ips[i]) + ')')
                break
            elif errorStatus:
                print('errorStatus: ' + str(errorStatus) + ' (' + str(ips[i]) + ')')
                break
            elif errorIndex:
                print('errorIndex: ' + str(errorIndex) + ' (' + str(ips[i]) + ')')
                break
            else:
                temp = varBinds[0][-1].prettyPrint()
                ## Vypisou se vsechny nalezene adresy.
                while len(temp) > 1:
                    if temp not in ips:
                        ips.append(temp)
                    # print('--> ' + temp)
                    errorIndication, errorStatus, errorIndex, varBinds = next(g)
                    temp = varBinds[0][-1].prettyPrint()
    print('Found IPs: ') ## Vypis nalezenych IP adres
    for i in range(len(ips)):
        print('-> ' + ips[i])
    print('Done scanning!')
    for i in range(int(len(ips) / 2)): ## Vypis ve formatu IP_router + IP_subnet
        print('For router on ip: ' + ips[i * 2 + 1] + ' is subnet ' + ips[i * 2] + '/'
              + str(31 - count_subnet(ips[i * 2], ips[i * 2 + 1])))
except StopIteration:
    print('Ending with error') ## Vypis chyby
