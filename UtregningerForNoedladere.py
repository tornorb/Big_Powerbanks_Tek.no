#! /usr/bin/env python3

import time
import os
import tkinter
from tkinter.filedialog import askopenfilename

wattimer = list()
prosenter = list()
totaleWattimer = list()
totaleProsenter = list()
elementTeller = 0


def regn_ut(mAh, volt, gittWh, teller):
    Wh = (float(mAh) * float(volt))/1000
    prosent = (Wh * 100)/float(gittWh)
    wattimer.append(float(Wh))
    prosenter.append(float(prosent))
    return (
        f"\nRunde {teller + 1} målt: {Wh:#.2f} Wh. "
        f"Prosentandel: {prosent:#.2f}%"
    )


def fjern_stjerner(linje):
    nyLinje = ""
    stjerneTeller = 0
    fjern = False
    for tegn in linje:
        if stjerneTeller == 3:
            fjern = False
        if tegn == "*" and stjerneTeller == 0:
            fjern = True
            stjerneTeller += 1
        elif tegn == "*" and stjerneTeller > 0:
            stjerneTeller += 1
        if fjern is not True:
            nyLinje += tegn
    return nyLinje


def regn_gjennomsnitt(liste):
    total = sum(map(float, liste))
    return total / len(liste)


def les_data():
    ferdigFil = open(velg_filnavn(), "w")
    print("\t>> Velg kildefil i filvelgervinduet\r\n")
    ferdigData = list()
    with open(velg_fil()) as fil:
        for linje in fil:
            ferdigData.append("\n" + fjern_stjerner(linje))
            temp = linje.split(" * ")
            if len(temp) > 1:
                gittWh, volt = temp[1], temp[2]
                tempTekst = f"Hevdet Wh: {gittWh} Wh"
                ferdigData.append(tempTekst)
                try:
                    temp1 = temp[3].split(" + ")
                    for i, tall in enumerate(temp1):
                        ferdigData.append(regn_ut(tall, volt, gittWh, i))
                except Exception as e:
                    print("\t\tERROR", e)
            if len(linje) > 10:
                wattimerGjennomsnitt = regn_gjennomsnitt(wattimer)
                prosentGjennomsnitt = regn_gjennomsnitt(prosenter)
                totaleWattimer.append(wattimerGjennomsnitt)
                totaleProsenter.append(prosentGjennomsnitt)
                ferdigData.append(
                    f"\nSnitt: {wattimerGjennomsnitt:#.2f}"
                    f" Wh + {prosentGjennomsnitt:#.2f}%"
                )
                wattimer.clear()
                prosenter.clear()
        totale_watt_timer_snitt = regn_gjennomsnitt(totaleWattimer)
        totale_prosenter_snitt = regn_gjennomsnitt(totaleProsenter)
        ferdigData.append(
            "\n\n\n* - - - - - - - - - - - - - - - - - - - - *\n\n"
            f"Snitt for alle laderne totalt: {totale_watt_timer_snitt:#.2f}"
            f" Wh + {totale_prosenter_snitt:#.2f}%"
        )
    for f in ferdigData:
        ferdigFil.write(f)
    print("\n\n\tJobber med dataene...")
    time.sleep(2)
    print(
        f"\n\n\tFil med prosessert data opprettet: '{ferdigFil.name}'"
        f"\n\tTilgjengelig ved: {os.path.realpath(ferdigFil.name)}"
    )


def velg_filnavn():
    filnavn = input(
        "\n\tHva oensker du at den ferdig prosesserte filen skal hete? "
    )
    return f"{filnavn}.txt"


def velg_fil():
    filbane = os.getcwd()  # Henter naavaerende filbane
    root = tkinter.Tk()  # Rot
    root.withdraw()     # Gjemmer selve Tkinter-vinduet
    root.update()
    filnavn = askopenfilename(
        initialdir=filbane,     # Lar bruker velge fil
        filetypes=(("Tekst", "*.txt"), ("Alle filtyper", "*.*")),
        title="Velg filen du vil hente data fra:"
    )
    root.destroy()
    return filnavn


if __name__ == '__main__':
    les_data()
