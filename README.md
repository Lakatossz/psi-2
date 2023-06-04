# 2. úloha semestarání práce

## Název: Topologie sítě

## Zadání: Implementujte aplikaci, která automaticky zjistí topologii sítě

## Popis
- Implementujte aplikaci v programovacím jazyce Python, která automaticky zjistí
topologii sítě, v které se nachází. Aplikace ke zjištění topologie využívá protokol
SNMP, pomocí kterého získá ze směrovačů obsah směrovacích tabulek.
Nejprve pomocí DHCP získá adresu výchozího směrovače, adresy dalších směrovačů
pak rekuzivním způsobem z obsahu směrovacích tabulek jednotlivých směrovačů. Je
nutné si uvědomit, že směrovač má zpravidla více rozhraní a je tedy identifikován
více IP adresami.

### Popis funkčnosti:

- Program nejpre zjístí default gateway zařízení, na kterém je spuštěn. Následně na tuto adresu pošle SNMP command.
Ten vrátí obash routovací tabulky routeru s danou IP. Následně se pro každou nalezenou IP zavolá stejný command.
Výsledkem je dvojice adres - IP routeru a IP sítě. Nakonec se z toho zjistí podsítě všech routerů a ty se vypíší.

### Příklad výstupu

    Found IPs: 
    -> 10.0.1.0
    -> 10.0.1.254
    -> 10.0.2.0
    -> 10.0.2.254
    -> 192.168.1.0
    -> 192.168.1.1
    Done scanning!
    For router on ip: 10.0.1.254 is subnet 10.0.1.0/24
    For router on ip: 10.0.2.254 is subnet 10.0.2.0/24
    For router on ip: 192.168.1.1 is subnet 192.168.1.0/30


### Implementace:

- Program je implementován v jazyce Python za použití knihoven scapy, pro zjištění default gateway, a pysnmp, pro
použití SNMP commandů pro Python.

### Spuštění

- python3 main.py