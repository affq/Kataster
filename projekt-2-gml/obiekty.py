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
    def __init__(self, idDzialki, geometria, numerKW, poleEwidencyjne, obreb_id, dokumentWlasnosci, adresNieruchomosci):
        self.nrDzialki = idDzialki.split('.')[-1]       
        super().__init__('blue', self.nrDzialki, geometria)
        self.idDzialki = idDzialki
        self.numerKW = numerKW
        self.poleEwidencyjne = poleEwidencyjne
        self.klasouzytki = []
        self.udzialy = []
        self.budynki = []
        self.obreb_id = obreb_id
        self.dokumentWlasnosci = dokumentWlasnosci
        self.adresNieruchomosci = adresNieruchomosci

    def add_udzial(self, udzial):
        self.udzialy.append(udzial)

    def add_klasouzytek(self, klasouzytek):
        self.klasouzytki.append(klasouzytek)
    
    def add_budynek(self, budynek):
        self.budynki.append(budynek)
    
    def __str__(self):
        return f'{self.idDzialki}'

class Budynek(Obiekt):
    def __init__(self, idBudynku, geometria, rodzajWgKST, liczbaKondygnacjiNadziemnych, liczbaKondygnacjiPodziemnych, powZabudowy, dzialka, dokumentWlasnosci, numerKW, dodatkoweInformacje, adresNieruchomosci):
        self.nrBudynku = idBudynku.split('.')[-1].split('_')[0]
        self.rodzajWgKST = rodzajWgKST
        super().__init__('black', self.rodzajWgKST, geometria)
        self.idBudynku = idBudynku
        self.liczbaKondygnacjiNadziemnych = liczbaKondygnacjiNadziemnych
        self.liczbaKondygnacjiPodziemnych = liczbaKondygnacjiPodziemnych
        self.powZabudowy = powZabudowy
        self.dzialka = dzialka
        self.dokumentWlasnosci = dokumentWlasnosci
        self.numerKW = numerKW
        self.dodatkoweInformacje = dodatkoweInformacje
        self.adresNieruchomosci = adresNieruchomosci
    
    def __str__(self):
        return f'{self.idBudynku=}, {self.powZabudowy=} '

class KonturKlasyfikacyjny(Obiekt):
    def __init__(self, idKonturu, geometria, OZU, OZK, obreb_id):
        self.nrKonturu = idKonturu.split('.')[-1]
        super().__init__('green', self.nrKonturu, geometria)
        self.idKonturu = idKonturu
        self.OZU = OZU
        self.OZK = OZK
        self.obreb_id = obreb_id

    def __str__(self):
        return f'{self.idUzytku=}, {self.geometria=}'

class KonturUzytkuGruntowego(Obiekt):
    def __init__(self, idKonturu, geometria, OFU, obreb_id):
        self.idKonturu = idKonturu
        self.nrKonturu = idKonturu.split('.')[-1]
        super().__init__('green', self.nrKonturu, geometria)
        self.OFU = OFU
        self.geometria = geometria
        self.obreb_id = obreb_id

    def __str__(self):
        return f'{self.idKonturu=}, {self.geometria=}'


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
        return f'{self.osobaFizyczna1.pierwszeImie} {self.osobaFizyczna1.pierwszyCzlonNazwiska} ({self.osobaFizyczna1.pesel}) oraz {self.osobaFizyczna2.pierwszeImie} {self.osobaFizyczna2.pierwszyCzlonNazwiska} ({self.osobaFizyczna2.pesel})'

class Adres:
    def __init__(self, miejscowosc, kodPocztowy, ulica, numerPorzadkowy):
        self.miejscowosc = miejscowosc
        self.kodPocztowy = kodPocztowy
        self.ulica = ulica
        self.numerPorzadkowy = numerPorzadkowy
        
class OsobaFizyczna:
    def __init__(self, pierwszeImie, pierwszyCzlonNazwiska, drugieImie, imieOjca, imieMatki, pesel, plec, status, adresOsobyFizycznej, drugiCzlonNazwiska, informacjaOSmierci):
        self.pierwszeImie = pierwszeImie
        self.pierwszyCzlonNazwiska = pierwszyCzlonNazwiska
        self.drugieImie = drugieImie
        self.imieOjca = imieOjca
        self.imieMatki = imieMatki
        self.pesel = pesel
        self.plec = plec
        self.status = status
        self.adresOsobyFizycznej = adresOsobyFizycznej
        self.drugiCzlonNazwiska = drugiCzlonNazwiska
        self.informacjaOSmierci = informacjaOSmierci

    def __str__(self):
        return f'{self.pierwszeImie} {self.pierwszyCzlonNazwiska}({self.pesel})'

class JednostkaEwidencyjna:
    def __init__(self, idJednostkiEwid, geometria, nazwaWlasna):
        self.idJednostkiEwid = idJednostkiEwid
        self.geometria = geometria
        self.nazwaWlasna = nazwaWlasna

class ObrebEwidencyjny:
    def __init__(self, idObrebu, geometria, nazwaWlasna, jednostkaEwid_id):
        self.idObrebu = idObrebu
        self.geometria = geometria
        self.nazwaWlasna = nazwaWlasna
        self.jednostkaEwid_id = jednostkaEwid_id

class ObiektTrwaleZwiazany:
    def __init__(self, geometria, rodzaj, idBudynku):
        self.geometria = geometria
        self.rodzaj = rodzaj
        self.idBudynku = idBudynku
    
class BlokBudynku:
    def __init__(self, geometria, rodzaj, oznaczenie, numerNajnizszejKondygnacji, numerNajwyzszejKondygnacji, idBudynku):
        self.geometria = geometria
        self.rodzaj = rodzaj
        self.oznaczenie = oznaczenie
        self.numerNajnizszejKondygnacji = numerNajnizszejKondygnacji
        self.numerNajwyzszejKondygnacji = numerNajwyzszejKondygnacji
        self.idBudynku = idBudynku

class PunktGraniczny:
    def __init__(self, geometria, idPunktu, sposobPozyskania, spelnienieWarunkowDokl, rodzajStabilizacji, oznWMaterialeZrodlowym, numerOperatuTechnicznego, dodatkoweInformacje):
        self.geometria = geometria
        self.idPunktu = idPunktu
        self.sposobPozyskania = sposobPozyskania
        self.spelnienieWarunkowDokl = spelnienieWarunkowDokl
        self.rodzajStabilizacji = rodzajStabilizacji
        self.oznWMaterialeZrodlowym = oznWMaterialeZrodlowym
        self.numerOperatuTechnicznego = numerOperatuTechnicznego
        self.dodatkoweInformacje = dodatkoweInformacje

class AdresNieruchomosci:
    def __init__(self, nazwaMiejscowosci, idMiejscowosci, nazwaUlicy, idNazwyUlicy, numerPorzadkowy, numerLokalu, geometria):
        self.nazwaMiejscowosci = nazwaMiejscowosci
        self.idMiejscowosci = idMiejscowosci
        self.nazwaUlicy = nazwaUlicy
        self.idNazwyUlicy = idNazwyUlicy
        self.numerPorzadkowy = numerPorzadkowy
        self.numerLokalu = numerLokalu
        self.geometria = geometria
    