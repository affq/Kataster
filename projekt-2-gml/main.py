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

def stworz_adres(adres):
    miejscowosc = adres.find('egb:miejscowosc').text
    kodPocztowy = adres.find('egb:kodPocztowy').text if adres.find('egb:kodPocztowy') is not None else None
    ulica = adres.find('egb:ulica').text if adres.find('egb:ulica') is not None else None
    numerPorzadkowy = adres.find('egb:numerPorzadkowy').text

    return Adres(miejscowosc, kodPocztowy, ulica, numerPorzadkowy)

def stworz_osobe(osobaFizyczna, adres):
    pierwszeImie = osobaFizyczna.find('egb:pierwszeImie').text
    pierwszyCzlonNazwiska = osobaFizyczna.find('egb:pierwszyCzlonNazwiska').text
    drugieImie = osobaFizyczna.find('egb:drugieImie').text if osobaFizyczna.find('egb:drugieImie') is not None else None
    imieOjca = osobaFizyczna.find('egb:imieOjca').text
    imieMatki = osobaFizyczna.find('egb:imieMatki').text
    pesel = osobaFizyczna.find('egb:pesel').text
    plec = osobaFizyczna.find('egb:plec').text
    status = osobaFizyczna.find('egb:status').text

    adresOsobyFizycznej = stworz_adres(adres)

    return OsobaFizyczna(pierwszeImie, pierwszyCzlonNazwiska, drugieImie, imieOjca, imieMatki, pesel, plec, status, adresOsobyFizycznej)

def stworz_instytucje(instytucja, adres):
    nazwaPelna = instytucja.find('egb:nazwaPelna').text
    nazwaSkrocona = instytucja.find('egb:nazwaSkrocona').text
    regon = instytucja.find('egb:regon').text
    status = instytucja.find('egb:status').text
    adresInstytucji = stworz_adres(adres)

    return Instytucja(nazwaPelna, nazwaSkrocona, regon, status, adresInstytucji)

def stworz_podmiot(podmiot, soup=soup):
    name = podmiot.name
    link = podmiot.get('xlink:href')
    if name == 'osobaFizyczna':
        podmiot = soup.find('egb:EGB_OsobaFizyczna', {'gml:id': link})
        adres_link = podmiot.find('egb:adresOsobyFizycznej').get('xlink:href')
        adres = soup.find('egb:EGB_AdresZameldowania', {'gml:id': adres_link})

        return stworz_osobe(podmiot, adres)
    elif name == 'instytucja1':
        podmiot = soup.find('egb:EGB_Instytucja', {'gml:id': link})
        adres_link = podmiot.find('egb:adresInstytucji').get('xlink:href')
        adres = soup.find('egb:EGB_AdresZameldowania', {'gml:id': adres_link})

        return stworz_instytucje(podmiot, adres)
    elif name == 'malzenstwo':
        podmiot = soup.find('egb:EGB_Malzenstwo', {'gml:id': link})
        osobaFizyczna2_link = podmiot.find('egb:osobaFizyczna2').get('xlink:href')
        osobaFizyczna3_link = podmiot.find('egb:osobaFizyczna3').get('xlink:href')
        osobaFizyczna2 = soup.find('egb:EGB_OsobaFizyczna', {'gml:id': osobaFizyczna2_link})
        osobaFizyczna2_adres = osobaFizyczna2.find('egb:adresOsobyFizycznej').get('xlink:href')
        osobaFizyczna2_adres = soup.find('egb:EGB_AdresZameldowania', {'gml:id': osobaFizyczna2_adres})
        osobaFizyczna3 = soup.find('egb:EGB_OsobaFizyczna', {'gml:id': osobaFizyczna3_link})
        osobaFizyczna3_adres = osobaFizyczna3.find('egb:adresOsobyFizycznej').get('xlink:href')
        osobaFizyczna3_adres = soup.find('egb:EGB_AdresZameldowania', {'gml:id': osobaFizyczna3_adres})

        osobaFizyczna2 = stworz_osobe(osobaFizyczna2, osobaFizyczna2_adres)
        osobaFizyczna3 = stworz_osobe(osobaFizyczna3, osobaFizyczna3_adres)

        return Malzenstwo(osobaFizyczna2, osobaFizyczna3)

class Instytucja:
    def __init__(self, nazwaPelna, nazwaSkrocona, regon, status, adresInstytucji):
        self.nazwaPelna = nazwaPelna
        self.nazwaSkrocona = nazwaSkrocona
        self.regon = regon
        self.status = status
        self.adresInstytucji = adresInstytucji

    def __str__(self):
        return f'{self.nazwaPelna}'

class Malzenstwo:
    def __init__(self, osobaFizyczna1, osobaFizyczna2):
        self.osobaFizyczna1 = osobaFizyczna1
        self.osobaFizyczna2 = osobaFizyczna2

    def __str__(self):
        return f'{self.osobaFizyczna1.pierwszeImie} {self.osobaFizyczna1.pierwszyCzlonNazwiska}, {self.osobaFizyczna1.pesel} oraz {self.osobaFizyczna2.pierwszeImie} {self.osobaFizyczna2.pierwszyCzlonNazwiska}, {self.osobaFizyczna2.pesel}'

class Adres:
    def __init__(self, miejscowosc, kodPocztowy, ulica, numerPorzadkowy):
        self.miejscowosc = miejscowosc
        self.kodPocztowy = kodPocztowy
        self.ulica = ulica
        self.numerPorzadkowy = numerPorzadkowy
        

class OsobaFizyczna:
    def __init__(self, pierwszeImie, pierwszyCzlonNazwiska, drugieImie, imieOjca, imieMatki, pesel, plec, status, adresOsobyFizycznej):
        self.pierwszeImie = pierwszeImie
        self.pierwszyCzlonNazwiska = pierwszyCzlonNazwiska
        self.drugieImie = drugieImie
        self.imieOjca = imieOjca
        self.imieMatki = imieMatki
        self.pesel = pesel
        self.plec = plec
        self.status = status
        self.adresOsobyFizycznej = adresOsobyFizycznej

    def __str__(self):
        return f'{self.pierwszeImie} {self.pierwszyCzlonNazwiska}, {self.pesel}'

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

podmioty = []
for udzial in soup.find_all('egb:EGB_UdzialWeWlasnosci'):
    obiekt_udzial = stworz_udzial(udzial)
    for podmiotUdzialuWlasnosci in udzial.find_all('egb:EGB_Podmiot'):
        for child in podmiotUdzialuWlasnosci.children:
            if child.name:
                podmiot = stworz_podmiot(child)
                print(podmiot)
