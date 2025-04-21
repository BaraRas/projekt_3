# **ENGETO 3. PROJEKT**
**Třetí projekt na Python Akademii od Engeta**

---

## **Popis projektu**
Tento projekt slouží k extrahování výsledků z **parlamentních voleb v roce 2017**. 
**Zdroj najdete** [zde](https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ)

---

## **Aktivace virtuálního prostředí**
Pro instalaci doporučuji využít nové virtuální prostředí. 
Pro vytvoření nového virtuálního prostředí použij následující příkaz v terminálu:

***Pro Windows*
python -m venv <NAZEV_ENV>      # vytvoření nového virtuálního prostředí
<NAZEV_ENV>\Scripts\Activate    # aktivace prostředí 

Například: 
python -m venv nove_venv
nove_venv\Scripts\Activate

---

## **Instalace knihoven**
Knihovny, které jsou použity v kódu, jsou uvedeny v souboru requirements.txt.
Pro jejich instalaci použij tento příkaz:

pip install -r requirements.txt

---

## **Spuštění projektu**
Spuštění souboru *main.py* v rámci příkazového řádku požaduje dva povinné argumenty. 
Pro argumenty byla využita knihovna *argparse*.

python main.py -u <odkaz_uzemniho_celku> -s <nazev_vysledného_csv_souboru>

Následně se stáhnou výsledky jako soubor s příponou *.csv*

---

## **Ukázka projektu**
Výsledky hlasování pro okres Břeclav:

1. argument: https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204
2. argument: Breclav.csv

Spuštění programu:
python main.py -u "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=11&xnumnuts=6204" -s "Breclav.csv"

Výstup:
- po úspěšném stáhnutí dat se objeví hláška *Soubor Brecla.csv uspěšně vytvořen*
- částečný výstup:
    [{'code': '584304', 'location': 'Bavory', 'registred': '334', 'envelopes': '236', 'valid': '236', 'Občanská demokratická strana': '42', 'Řád národa - Vlastenecká unie': '0', 'CESTA ODPOVĚDNÉ SPOLEČNOSTI': '0', 'Česká str.sociálně demokrat.': '10', 'Radostné Česko': '0', 'STAROSTOVÉ A NEZÁVISLÍ': '10', 'Komunistická str.Čech a Moravy': '22', 'Strana zelených': '6', 'ROZUMNÍ-stop migraci,diktát.EU': '6', 'Strana svobodných občanů': '4', 'Blok proti islam.-Obran.domova': '0', 'Občanská demokratická aliance': '0', 'Česká pirátská strana': '20', 'Referendum o Evropské unii': '0', 'TOP 09': '14', 'ANO 2011': '66', 'Dobrá volba 2016': '1', 'SPR-Republ.str.Čsl. M.Sládka': '0', 'Křesť.demokr.unie-Čs.str.lid.': '15', 'Česká strana národně sociální': '0', 'REALISTÉ': '0', 'SPORTOVCI': '0', 'Dělnic.str.sociální spravedl.': '1', 'Svob.a př.dem.-T.Okamura (SPD)': '18', 'Strana Práv Občanů': '0'...}]
- objeví se nový csv soubor *Breclav.csv*








