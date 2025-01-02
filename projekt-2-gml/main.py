from bs4 import BeautifulSoup

with open('gml.xml', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f, 'xml')

class Klasouzytek:
    def __init__(self, OFU, OZU, OZK, powierzchnia):
        self.OFU = OFU
        self.OZU = OZU
        self.OZK = OZK
        self.powierzchnia = powierzchnia
    
    def __str__(self):
        return f'OFU: {self.OFU}, OZU: {self.OZU}, OZK: {self.OZK}, powierzchnia: {self.powierzchnia}'


class DzialkaEwidencyjna:
    def __init__(self, idDzialki, geometria, numerKW, poleEwidencyjne):
        self.idDzialki = idDzialki
        self.geometria = geometria
        self.numerKW = numerKW
        self.poleEwidencyjne = poleEwidencyjne
        self.Klasouzytki = []
    
    def add_klasouzytek(self, klasouzytek):
        self.Klasouzytki.append(klasouzytek)
    
    def __str__(self):
        return f'{self.idDzialki}'

class Budynek:
    def __init__(self, idBudynku, geometria, rodzajWgKST, liczbaKondygnacjiNadziemnych, liczbaKondygnacjiPodziemnych, powZabudowy):
        self.idBudynku = idBudynku
        self.geometria = geometria
        self.rodzajWgKST = rodzajWgKST
        self.liczbaKondygnacjiNadziemnych = liczbaKondygnacjiNadziemnych
        self.liczbaKondygnacjiPodziemnych = liczbaKondygnacjiPodziemnych
        self.powZabudowy = powZabudowy
    
    def __str__(self):
        return f'{self.idBudynku=}, {self.powZabudowy=} '

class Kontur:
    def __init__(self, idUzytku, geometria, OFU):
        self.idUzytku = idUzytku
        self.geometria = geometria
        self.OFU = OFU
    
    def __str__(self):
        return f'{self.idUzytku=}, {self.OFU=}'

class UdzialWeWlasnosci:
    def __init__(self, rodzajPrawa, licznikUlamkaOkreslajacegoWartoscUdzialu, mianownikUlamkaOkreslajacegoWartoscUdzialu):
        self.rodzajPrawa = rodzajPrawa
        self.licznikUlamkaOkreslajacegoWartoscUdzialu = licznikUlamkaOkreslajacegoWartoscUdzialu
        self.mianownikUlamkaOkreslajacegoWartoscUdzialu = mianownikUlamkaOkreslajacegoWartoscUdzialu
        self.przedmiotUdzialuWlasnosci = None
        self.podmiotUdzialuWlasnosci = []
    
    def add_podmiotUdzialuWlasnosci(self, podmiotUdzialuWlasnosci):
        self.podmiotUdzialuWlasnosci.append(podmiotUdzialuWlasnosci)

def stworz_dzialke(dzialka):
    idDzialki = dzialka.find('egb:idDzialki').text
    geometria = dzialka.find('egb:geometria').text
    numerKW_element = dzialka.find('egb:numerKW')
    numerKW = numerKW_element.text if numerKW_element is not None else None

    poleEwidencyjne = dzialka.find('egb:poleEwidencyjne').text

    return DzialkaEwidencyjna(idDzialki, geometria, numerKW, poleEwidencyjne)

def stworz_klasouzytek(klasouzytek):
    OFU = klasouzytek.find('egb:OFU').text 
    
    ozu_element = klasouzytek.find('egb:OZU')
    OZU = ozu_element.text if ozu_element is not None else None

    ozk_element = klasouzytek.find('egb:OZK')
    OZK = ozk_element.text if ozk_element is not None else None
    
    powierzchnia = klasouzytek.find('egb:powierzchnia').text

    return Klasouzytek(OFU, OZU, OZK, powierzchnia)

def stworz_budynek(budynek):
    idBudynku = budynek.find('egb:idBudynku').text
    geometria = budynek.find('egb:geometria').text
    rodzajWgKST = budynek.find('egb:rodzajWgKST').text
    liczbaKondygnacjiNadziemnych = budynek.find('egb:liczbaKondygnacjiNadziemnych').text
    liczbaKondygnacjiPodziemnych = budynek.find('egb:liczbaKondygnacjiPodziemnych').text
    powZabudowy = budynek.find('egb:powZabudowy').text

    return Budynek(idBudynku, geometria, rodzajWgKST, liczbaKondygnacjiNadziemnych, liczbaKondygnacjiPodziemnych, powZabudowy)

def stworz_kontur(kontur):
    idUzytku = kontur.find('egb:idUzytku').text
    geometria = kontur.find('egb:geometria').text
    OFU = kontur.find('egb:OFU').text

    return Kontur(idUzytku, geometria, OFU)

def stworz_udzial(udzial):
    rodzajPrawa = udzial.find('egb:rodzajPrawa').text
    licznikUlamkaOkreslajacegoWartoscUdzialu = udzial.find('egb:licznikUlamkaOkreslajacegoWartoscUdzialu').text
    mianownikUlamkaOkreslajacegoWartoscUdzialu = udzial.find('egb:mianownikUlamkaOkreslajacegoWartoscUdzialu').text
    przedmiotUdzialuWlasnosci = udzial.find('egb:przedmiotUdzialuWlasnosci').text

    return UdzialWeWlasnosci(rodzajPrawa, licznikUlamkaOkreslajacegoWartoscUdzialu, mianownikUlamkaOkreslajacegoWartoscUdzialu)

dzialki = []
for dzialka in soup.find_all('egb:EGB_DzialkaEwidencyjna'):
    obiekt_dzialka = stworz_dzialke(dzialka)
    for klasouzytek in dzialka.find_all('egb:klasouzytek'):
        obiekt_klasouzytek = stworz_klasouzytek(klasouzytek)
        obiekt_dzialka.add_klasouzytek(obiekt_klasouzytek)
    dzialki.append(obiekt_dzialka)

budynki = []
for budynek in soup.find_all('egb:EGB_Budynek'):
    obiekt_budynek = stworz_budynek(budynek)
    budynki.append(obiekt_budynek)

kontury = []
for kontur in soup.find_all('egb:EGB_KonturUzytkuGruntowego'):
    obiekt_kontur = stworz_kontur(kontur)
    kontury.append(obiekt_kontur)            

udzialy = []
for udzial in soup.find_all('egb:EGB_UdzialWeWlasnosci'):
    obiekt_udzial = stworz_udzial(udzial)
    for podmiotUdzialuWlasnosci in udzial.find_all('egb:EGB_Podmiot'):
        for child in podmiotUdzialuWlasnosci.children:
            if child.name:
                obiekt_podmiotUdzialuWlasnosci = PodmiotUdzialuWlasnosci(child)