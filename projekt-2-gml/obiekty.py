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
        self.udzialy = []
    
    def add_udzial(self, udzial):
        self.udzialy.append(udzial)

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
    def __init__(self, rodzajPrawa, licznikUlamkaOkreslajacegoWartoscUdzialu, mianownikUlamkaOkreslajacegoWartoscUdzialu, podmiotUdzialuWlasnosci, przedmiotUdzialuWlasnosci):
        self.rodzajPrawa = rodzajPrawa
        self.licznikUlamkaOkreslajacegoWartoscUdzialu = licznikUlamkaOkreslajacegoWartoscUdzialu
        self.mianownikUlamkaOkreslajacegoWartoscUdzialu = mianownikUlamkaOkreslajacegoWartoscUdzialu
        self.przedmiotUdzialuWlasnosci = przedmiotUdzialuWlasnosci
        self.podmiotUdzialuWlasnosci = podmiotUdzialuWlasnosci

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
