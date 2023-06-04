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

- 

### Implementace:

- 

### Spuštění

- ./build/client/client <cislo_port> <obsah_zpravy>