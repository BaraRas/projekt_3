"""
projekt_3.py: třetí projekt do Engeto Online Python Akademie, verze 2

author: Barbora Rašticová
email: rasticova.barbora@seznam.cz
"""

import requests
from bs4 import BeautifulSoup
import argparse
import sys
import csv
import os

def definuj_argumenty() -> tuple[str, str]:
    '''
    Zpracuje argumenty z příkazové řádky.

    Returns:
        Tuple[str, str]: URL adresa a název složky pro uložení CSV souboru
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", 
                        type = str, 
                        help = "url adresa vybraného uzemního celku", 
                        required = True)
    parser.add_argument("-s", "--slozka",
                        type = str, 
                        help = "Název csv složky, do které budou data uložena.",
                        required = True)
     
    args = parser.parse_args()
    return args.url, args.slozka

def ziskej_obec(soup) -> list[dict[str, str]]:
    '''
    Extrahuje kody a názvy obcí z hlavní stránky.

    Args:
        soup: HTML strom hlavní stránky 
    Returns:
        list[dict[str, str]]: Seznam slovníků s kodem a názvem obce
    '''
    vsechny_tabulky = soup.find_all("table")    # Najde všechny tabulky na zadané url adrese
    
    data_obce = []
    for tabulka in vsechny_tabulky: # Pro každou nalezenou tabulku najde všechny řádky 
        vsechny_tr = tabulka.find_all("tr")[2:] # Přeskočí první 2 řádky (záhlaví tabulky)
        
        for tr in vsechny_tr:   # Pro všechny řádky v dané tabulce (kromě prvních dvou řádků) najde všechny sloupce 
            td_na_radku = tr.find_all("td")
            data_obce.append({
                "code" : td_na_radku[0].get_text(),
                "location" : td_na_radku[1].get_text()
            }) #vybere 1. a 2. sloupec a uloží je do slovníku ke klíčům code a location

    return data_obce

def extrahuj_data_z_tabulky(soup) -> dict[str, str]:
    '''
    Získá volební data z detailní stránky obce.

    Args:
        soup: HTML strom hlavní stránky 
    Returns:
        Dict[str, str]: Slovník s informacemi o voličích a stranách
    '''

    #tabulka_1 = voliči, celkove hlasy a obálky
    tabulka_1 = soup.find_all("table")[0] # Najde všechny tabulky a vybere 1. tabulku s informacemi o celkovém počtu voličů, vydaných obálek a platných hlasů
    radky = tabulka_1.find_all("tr")[2] # V tabulce nejde všechny řádky kromě prvních 2 (záhlaví tabulky)

    try:
        sloupce = radky.find_all("td") # Pro tyto řádky najde všechny dostupné sloupce 
        data_tabulka_1 = { # Vybere 4, 5 a 7 sloupec a uloží je do slovníku s klíči registred, envelopec a valid
            "registred" : sloupce[3].get_text().replace("\xa0", "").strip(), # z každého sloupce odstraní '/xa0', což je znak pevné mezery
            "envelopes" : sloupce[4].get_text().replace("\xa0", "").strip(),
            "valid" : sloupce[7].get_text().replace("\xa0", "").strip()
        } 
    except IndexError: #ošetření, v případě, že by daný sloupec neexistoval
        data_tabulka_1 = {"registred": "N/A", "envelopes": "N/A", "valid": "N/A"}

    #tabulka_2 a tabulka_3 = strany a počet hlasů pro jednotlivé strany
    data_tabulka_2_3 = {}

    tabulka_2_3 = soup.find_all("table")[1:] # najde ostatní tabulky na stránce (od 2. tabulky..)

    for tabulka in tabulka_2_3:
        tr = tabulka.find_all("tr")[2:] # Pro každou tabulku najde všechny řádky kromě prvních 2 (záhlaví)

        for radek in tr:
            td = radek.find_all("td") # Po každý řádek najde sloupec
            data_tabulka_2_3[td[1].get_text()] = td[2].get_text().replace("\xa0", "").strip() # Hodnotu ze sloupce 2 přiřadí jako klíč a hodnotu ze sloupce 3 jako jeho hodnotu
            
    result = {**data_tabulka_1, **data_tabulka_2_3} # Sloučí dva slovníky - data z tabulky 1 a z tabulek 2 a 3
    return result


def hlavni_scraping(url, soup) -> list[dict[str, str]]:
    '''
    Provede scraping všech obcí a jejich detailních stránek.

    Args:
        url: URL hlavní stránky
        soup: HTLM strom hlavní stránky 
    Returns:
        list[dict[str, str]]: Seznam výslednů pro každou obec
    '''

    obce = ziskej_obec(soup)
    vsechny_vysledky = []

    #získání kodu kraje z URL hlavní stránky
    xkraj = url.split("xkraj=")[1].split("&")[0] # Z URL adresy získá hodnotu pro xkraj
    xnumnuts = url.split("xnumnuts=")[1] # A hodnotu pro xnumnuts

    for obec in obce: # ze slovníku obcí pak získá hodnoty pro code a location 
        code = obec["code"]
        location = obec["location"]

        #dynamické URL pro detailní stránku obce - dynamické dosazení daných hodnot xkraj, code a xnumnuts
        detail_url_obce = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={xkraj}&xobec={code}&xvyber={xnumnuts}" 

        #načtení detailní stránky obce
        odpoved_detail = requests.get(detail_url_obce)
        soup_detail = BeautifulSoup(odpoved_detail.text, "html.parser")

        #zisk detailních dat pro danou obec
        data = extrahuj_data_z_tabulky(soup_detail)

        #slovník pro výsledky této obce
        obec_vysledky = {
            "code" : code,
            "location" : location,
            **data #přidáme data z detailní stránky
            }

        #přidáme výsledky do celkového seznamu
        vsechny_vysledky.append(obec_vysledky)

    return vsechny_vysledky


def vytvor_csv_soubor(soubor: str, url: str, soup) -> str: 
    '''
    Vytvoří CSV soubor s výsledky voleb.

    Args:
        soubor: Cílová cesta pro výstupní soubor.
        url: URL adresa stránky
        soup: HTML strom hlavní stránky
    Returns:
        str: Zpráva o výsledku zápisu
    '''
    
    vysledny_soubor = hlavni_scraping(url, soup)

    slozka = os.path.dirname(soubor) # Získáme cestu k adresáři, ve kterém bude soubor uložen
    if slozka and not os.path.exists(slozka):
        os.makedirs(slozka) # Pokud adresář neexistuje, vytvoříme ho

    try:
        with open(soubor, mode = "x", encoding = "utf-8-sig", newline = "") as file:
            hlavicka = vysledny_soubor[0].keys() #hlavička tabulky bude tvořena z klíčů 

            zapisovac = csv.DictWriter(file, fieldnames = hlavicka, delimiter = ";")
            zapisovac.writeheader()
            zapisovac.writerows(vysledny_soubor)
    
        return f"Soubor {soubor} uspěšně vytvořen."
    
    except FileExistsError:
        return f"Soubor {soubor} již existuje" # Vrátí vyjímku pokud soubor už existuje 


def main() -> None:
    '''
    Hlavní vstupní  bod programu. 
    Získá argumenty, načte stránku a spustí scraping + zápis výsledků
    '''

    url, slozka = definuj_argumenty() #získání URL hlavní stránky a názvu složky 

    odpoved = requests.get(url) #Načtení stránky a vytvoření bs objektu

    if odpoved.status_code != 200: # Zkontroluje status kód odpovědi a případně ukončí program při chybě
        print(f"Chyba při stahování stránky, status code: {odpoved.status_code}")
        sys.exit(1)

    soup = BeautifulSoup(odpoved.text, "html.parser")

    vysledky = hlavni_scraping(url, soup) # Spuštění scrapingu s předaným HTML
    print(vysledky)
    
    zprava = vytvor_csv_soubor(slozka, url, soup)
    print(zprava) # Vypíše hlášku zda byl soubor úspěšně vytvořen, či daná složka už existuje

if __name__ == "__main":
    main()

    

























