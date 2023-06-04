from pysnmp.hlapi import *
from scapy.all import *

SNMP_PORT = 161  ## port pro SNMP
ipAdEntAddr = "1.3.6.1.2.1.4.21.1.1.2"  ## oid pro ipRouteDest
ip = conf.route.route('0.0.0.0')[2]  ## default gateway zarizeni
community = 'PSIPUB' ## Community rezetec site.


## Funkce pro vytvoreni pysnmp commandu.
def walk_remote(host, oid):
    return bulkCmd(SnmpEngine(),
                   CommunityData(community, mpModel=1),
                   UdpTransportTarget((host, SNMP_PORT), timeout=0.0, retries=0),
                   ContextData(),
                   0, 25,
                   ObjectType(ObjectIdentity(oid)))


ips = [] ## Pole pro nacteni IP adres site.

try:
    print('Starting scanning...')
    g = walk_remote(ip, ipAdEntAddr) ## Vytvoreni SNMP prikazu.
    errorIndication, errorStatus, errorIndex, varBinds = next(g) ## Spusteni prvni SNMP prikazu.
    temp = varBinds[0][-1].prettyPrint() ## Ziskani prvni IP adresy.
    print('nalezene IP v prvnim nodu:')
    while len(temp) > 1: ## Pokud SNMP vraci IP adresy.
        ips.append(temp) ## Pridam adresu do pole.
        print('-> ' + str(temp))
        errorIndication, errorStatus, errorIndex, varBinds = next(g) ## Dalsi spusteni
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
    print('-------------------------------')
    ## Nyni se projdou vsechny nalezene zarizeni podle IP adres.
    for i in range(len(ips)):
        print('nalezene IP v na IP: ' + ips[i])
        g = walk_remote(ips[i], ipAdEntAddr)
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
                    ips.append(temp)
                    print('--> ' + temp)
                    errorIndication, errorStatus, errorIndex, varBinds = next(g)
                    temp = varBinds[0][-1].prettyPrint()
    print('Done scanning!')
except StopIteration:
    print('koncim')
