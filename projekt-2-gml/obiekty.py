class Klasouzytek:
    def __init__(self, OFU, OZU, OZK, powierzchnia):
        self.OFU = OFU
        self.OZU = OZU
        self.OZK = OZK
        self.powierzchnia = powierzchnia
    
    def __str__(self):
        return f'OFU: {self.OFU}, OZU: {self.OZU}, OZK: {self.OZK}, powierzchnia: {self.powierzchnia}'

class Obiekt:
    def __init__(self, color, podpis, geometria):
        self.color = color
        self.podpis = podpis
        self.geometria = geometria
        self.narysowany = False
        self.polygon = None

class DzialkaEwidencyjna(Obiekt):
    def __init__(self, idDzialki, geometria, numerKW, poleEwidencyjne):
        super().__init__('blue', idDzialki, geometria)
        self.idDzialki = idDzialki
        self.numerKW = numerKW
        self.poleEwidencyjne = poleEwidencyjne
        self.klasouzytki = []
        self.udzialy = []
        self.budynki = []

    def add_udzial(self, udzial):
        self.udzialy.append(udzial)

    def add_klasouzytek(self, klasouzytek):
        self.klasouzytki.append(klasouzytek)
    
    def add_budynek(self, budynek):
        self.budynki.append(budynek)
    
    def __str__(self):
        return f'{self.idDzialki}'

class Budynek(Obiekt):
    def __init__(self, idBudynku, geometria, rodzajWgKST, liczbaKondygnacjiNadziemnych, liczbaKondygnacjiPodziemnych, powZabudowy, dzialka):
        super().__init__('red', idBudynku, geometria)
        self.idBudynku = idBudynku
        self.rodzajWgKST = rodzajWgKST
        self.liczbaKondygnacjiNadziemnych = liczbaKondygnacjiNadziemnych
        self.liczbaKondygnacjiPodziemnych = liczbaKondygnacjiPodziemnych
        self.powZabudowy = powZabudowy
        self.dzialka = dzialka
    
    def __str__(self):
        return f'{self.idBudynku=}, {self.powZabudowy=} '

class Kontur(Obiekt):
    def __init__(self, idUzytku, geometria, OFU):
        super().__init__('green', idUzytku, geometria)
        self.idUzytku = idUzytku
        self.OFU = OFU

    def __str__(self):
        return f'{self.idUzytku=}, {self.geometria=}'

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