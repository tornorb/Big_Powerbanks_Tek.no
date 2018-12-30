#! /usr/bin/env python3

import os
from pathlib import Path
import re
import tkinter
from tkinter.filedialog import askopenfilename
from typing import List, Union

wattimer = list()
prosenter = list()
NUMBER = Union[int, float]


def regn_ut(
    mAh: NUMBER,
    volt: NUMBER,
    gittWh: NUMBER,
    teller: int,
) -> str:
    Wh = (float(mAh) * float(volt)) / 1000
    prosent = (Wh * 100) / float(gittWh)
    wattimer.append(float(Wh))
    prosenter.append(float(prosent))
    return (
        f"Runde {teller + 1} målt: {Wh:.2f} Wh. Prosentandel: {prosent:.2f}%"
    )


def fjern_stjerner(linje):
    plasseringer_av_stjerner = [
        m.start()
        for m in re.finditer(r'\*', linje)
    ]

    # Ta med alt frem til, men ikke med første '*'
    nyLinje = linje[:plasseringer_av_stjerner[0]]

    if len(plasseringer_av_stjerner) >= 3:
        # Ta med alt etter tredje '*' om den finnes
        nyLinje += linje[plasseringer_av_stjerner[2] + 1:]
    return nyLinje


def regn_gjennomsnitt(liste: List[Union[NUMBER]]) -> float:
    if len(liste) == 0:
        return float(0)
    total = sum(map(float, liste))
    return total / len(liste)


def les_data(input_fil: Path) -> List[str]:
    ferdigData = list()
    totaleWattimer, totaleProsenter = list(), list()
    for linje in input_fil.read_text().splitlines():
        if linje.strip() == '':
            # Hopp over tomme linjer...
            continue
        enhetsData = [f"\n{fjern_stjerner(linje)}"]
        verdier = linje.split(' * ')
        if len(verdier) > 1:
            gittWh, volt = verdier[1], verdier[2]
            enhetsData.append(f"Hevdet Wh: {gittWh} Wh")
            # Alltid tøm globale lister før man kaller regn_ut() på en ny linje
            wattimer.clear()
            prosenter.clear()
            try:
                for i, tall in enumerate(verdier[3].split(" + ")):
                    enhetsData.append(regn_ut(tall, volt, gittWh, i))
            except Exception as e:
                print('\t\tERROR', e)
        if len(linje) > 10:
            watt_snitt = regn_gjennomsnitt(wattimer)
            prosent_snitt = regn_gjennomsnitt(prosenter)
            totaleWattimer.append(watt_snitt)
            totaleProsenter.append(prosent_snitt)
            enhetsData.append(
                f"Snitt: {watt_snitt:.2f} Wh + {prosent_snitt:.2f}%"
            )
            # Alltid tøm globale lister før man kaller regn_ut() på en ny linje
            wattimer.clear()
            prosenter.clear()
        ferdigData.append('\n'.join(enhetsData))

    totale_w_snitt = regn_gjennomsnitt(totaleWattimer)
    totale_p_snitt = regn_gjennomsnitt(totaleProsenter)
    ferdigData.append(
        '\n\n* - - - - - - - - - - - - - - - - - - - - *\n\n'
        f"Snitt for alle laderne totalt: {totale_w_snitt:.2f} Wh + {totale_p_snitt:.2f}%"
        '\n'
    )
    return ferdigData


def velg_filnavn() -> str:
    filnavn = input(
        '\n\tHva oensker du at den ferdig prosesserte filen skal hete? '
    )
    filtype = os.path.splitext(filnavn)[1]
    if filtype == '':
        filnavn += '.txt'
    return filnavn


def velg_fil() -> Path:
    filbane = os.getcwd()  # Henter nåværende filbane
    root = tkinter.Tk()  # Rot
    root.withdraw()     # Gjemmer selve Tkinter-vinduet
    root.update()
    print("\t>> Velg kildefil i filvelgervinduet\n")
    filnavn = askopenfilename(
        initialdir=filbane,     # Lar bruker velge fil
        filetypes=(("Tekst", "*.txt"), ("Alle filtyper", "*.*")),
        title="Velg filen du vil hente data fra:"
    )
    root.destroy()
    return Path(filnavn)


if __name__ == '__main__':
    output_fil = Path(velg_filnavn()).resolve()
    while output_fil.is_file():
        print(f"\n\t'{output_fil.absolute()}' eksisterer.")
        svar = input('\tOverskrive filen? j[a]/y[es]/Nei]: ')
        if svar.lower().startswith('j') or svar.lower().startswith('y'):
            break
        output_fil = velg_filnavn()

    print('\n\n\tJobber med dataene...')
    innleste_data = "\n".join(
        les_data(
            input_fil=velg_fil()  # Filen med data å lese
        )
    )
    output_fil.write_text(innleste_data)

    print(
        f"\n\n\tFil med prosessert data opprettet: '{output_fil.name}'"
        f"\n\tTilgjengelig ved: {output_fil.absolute()}"
    )
