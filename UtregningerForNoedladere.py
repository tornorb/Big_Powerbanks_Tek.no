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
    return("\nRunde " + str(teller+1) + " målt: " + str(float("{0:.2f}".format(Wh))) + " Wh. Prosentandel: " + str(float("{0:.2f}".format(prosent))) + "%")


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
    total = 0.0
    for l in liste:
        total += float(l)
    return total/len(liste)


def les_data():
    ferdigFil = open(velg_filnavn(), "w")
    print("    >> Velg kildefil i filvelgervinduet\r\n")
    ferdigData = list()
    with open(velg_fil()) as fil:
        for linje in fil:
            t = linje.find("*", 0, )
            ferdigData.append("\n" + fjern_stjerner(linje))
            temp = linje.split(" * ")
            if len(temp) > 1:
                produkt = temp[0]
                gittWh = temp[1]
                volt = temp[2]
                tempTekst = "Hevdet Wh: " + str(gittWh) + " Wh"
                ferdigData.append(tempTekst)
                try:
                    temp1 = temp[3].split(" + ")
                    for i, tall in enumerate(temp1):
                        ferdigData.append(regn_ut(tall, volt, gittWh, i))
                except Exception as e:
                    print("        ERROR", e)
            if len(linje) > 10:
                wattimerGjennomsnitt = regn_gjennomsnitt(wattimer)
                prosentGjennomsnitt = regn_gjennomsnitt(prosenter)
                totaleWattimer.append(wattimerGjennomsnitt)
                totaleProsenter.append(prosentGjennomsnitt)
                ferdigData.append("\nSnitt: " + str("{0:.2f}".format(wattimerGjennomsnitt)) + " Wh + " + str("{0:.2f}".format(prosentGjennomsnitt)) + "%")
                wattimer.clear()
                prosenter.clear()
        ferdigData.append("\n\n\n * - - - - - - - - - - - - - - - - - - - - *\n\nSnitt for alle laderne totalt: " + str("{0:.2f}".format(regn_gjennomsnitt(totaleWattimer))) + " Wh + " + str("{0:.2f}".format(regn_gjennomsnitt(totaleProsenter))) + "%")
    for f in ferdigData:
        ferdigFil.write(f)
    print("\n\n    Jobber med dataene...")
    time.sleep(2)
    print("\n\n    Fil med prosessert data opprettet: '" + ferdigFil.name + "'\r\n    Tilgjengelig ved:", os.path.realpath(ferdigFil.name),"\r\n")


def velg_filnavn():
    return str(input("\r\n    Hva oensker du at den ferdig prosesserte filen skal hete? ") + ".txt")


def velg_fil():
    filbane = os.getcwd()  #Henter naavaerende filbane
    root = tkinter.Tk()  # Rot
    root.withdraw() # Gjemmer selve Tkinter-vinduet
    root.update()
    filnavn = askopenfilename(initialdir=filbane, # Lar bruker velge fil
                              filetypes =(("Tekst", "*.txt"), ("Alle filtyper","*.*")),
                              title = "Velg filen du vil hente data fra:")
    root.destroy()
    return filnavn

if __name__ == '__main__':
    les_data()
