from bs4 import BeautifulSoup
from obiekty import *

def stworz_dzialke(dzialka, soup):
    idDzialki = dzialka.find('egb:idDzialki').text
    geometria = dzialka.find('egb:geometria').text
    numerKW = dzialka.find('egb:numerKW').text if dzialka.find('egb:numerKW') is not None else ''
    poleEwidencyjne = dzialka.find('egb:poleEwidencyjne').text
    obreb_link = dzialka.find('egb:lokalizacjaDzialki').get('xlink:href')
    obreb_id = soup.find('egb:EGB_ObrebEwidencyjny', {'gml:id': obreb_link}).find('egb:idObrebu').text
    dokumentWlasnosci = dzialka.find('egb:dokumentWlasnosci').text if dzialka.find('egb:dokumentWlasnosci') is not None else ''
    adresNieruchomosci_link = dzialka.find('egb:adresNieruchomosci').get('xlink:href') if dzialka.find('egb:adresNieruchomosci') is not None else ''
    adresNieruchomosci = soup.find('egb:EGB_AdresNieruchomosci', {'gml:id': adresNieruchomosci_link}) if adresNieruchomosci_link else None
    adresNieruchomosci = stworz_adres_nieruchomosci(adresNieruchomosci) if adresNieruchomosci else None

    return DzialkaEwidencyjna(idDzialki, geometria, numerKW, poleEwidencyjne, obreb_id, dokumentWlasnosci, adresNieruchomosci)

def stworz_klasouzytek(klasouzytek):
    OFU = klasouzytek.find('egb:OFU').text 
    
    ozu_element = klasouzytek.find('egb:OZU')
    OZU = ozu_element.text if ozu_element is not None else ''

    ozk_element = klasouzytek.find('egb:OZK')
    OZK = ozk_element.text if ozk_element is not None else ''
    
    powierzchnia = klasouzytek.find('egb:powierzchnia').text

    return Klasouzytek(OFU, OZU, OZK, powierzchnia)

def stworz_budynek(budynek, dzialka, soup):
    idBudynku = budynek.find('egb:idBudynku').text
    geometria = budynek.find('egb:geometria').text
    rodzajWgKST = budynek.find('egb:rodzajWgKST').text
    liczbaKondygnacjiNadziemnych = budynek.find('egb:liczbaKondygnacjiNadziemnych').text
    liczbaKondygnacjiPodziemnych = budynek.find('egb:liczbaKondygnacjiPodziemnych').text
    powZabudowy = budynek.find('egb:powZabudowy').text
    dokumentWlasnosci = budynek.find('egb:dokumentWlasnosci').text if budynek.find('egb:dokumentWlasnosci') is not None else ''
    numerKW = budynek.find('egb:numerKW').text if budynek.find('egb:numerKW') is not None else ''
    dodatkoweInformacje = budynek.find('egb:dodatkoweInformacje').text if budynek.find('egb:dodatkoweInformacje') is not None else ''
    adresNieruchomosci_link = budynek.find('egb:adresNieruchomosci').get('xlink:href') if budynek.find('egb:adresNieruchomosci') is not None else ''
    adresNieruchomosci = soup.find('egb:EGB_AdresNieruchomosci', {'gml:id': adresNieruchomosci_link}) if adresNieruchomosci_link else None
    adresNieruchomosci = stworz_adres_nieruchomosci(adresNieruchomosci) if adresNieruchomosci else None

    return Budynek(idBudynku, geometria, rodzajWgKST, liczbaKondygnacjiNadziemnych, liczbaKondygnacjiPodziemnych, powZabudowy, dzialka, dokumentWlasnosci, numerKW, dodatkoweInformacje, adresNieruchomosci)

def stworz_kontur_klasyfikacyjny(kontur, soup):
    idKonturu = kontur.find('egb:idKonturu').text
    geometria = kontur.find('egb:geometria').text
    OZU = kontur.find('egb:OZU').text
    OZK = kontur.find('egb:OZK').text if kontur.find('egb:OZK') is not None else ''
    obreb_link = kontur.find('egb:lokalizacjaKonturu').get('xlink:href')
    obreb_id = soup.find('egb:EGB_ObrebEwidencyjny', {'gml:id': obreb_link}).find('egb:idObrebu').text

    return KonturKlasyfikacyjny(idKonturu, geometria, OZU, OZK, obreb_id)

def stworz_kontur_uzytku(kontur, soup):
    idUzytku = kontur.find('egb:idUzytku').text
    geometria = kontur.find('egb:geometria').text
    OFU = kontur.find('egb:OFU').text
    obreb_link = kontur.find('egb:lokalizacjaUzytku').get('xlink:href')
    obreb_id = soup.find('egb:EGB_ObrebEwidencyjny', {'gml:id': obreb_link}).find('egb:idObrebu').text

    return KonturUzytkuGruntowego(idUzytku, geometria, OFU, obreb_id)

def stworz_udzial(udzial, podmiot, przedmiot):
    rodzajPrawa = udzial.find('egb:rodzajPrawa').text
    licznikUlamkaOkreslajacegoWartoscUdzialu = udzial.find('egb:licznikUlamkaOkreslajacegoWartoscUdzialu').text
    mianownikUlamkaOkreslajacegoWartoscUdzialu = udzial.find('egb:mianownikUlamkaOkreslajacegoWartoscUdzialu').text
    podmiotUdzialuWlasnosci = podmiot
    przedmiotUdzialuWlasnosci = przedmiot

    return UdzialWeWlasnosci(rodzajPrawa, licznikUlamkaOkreslajacegoWartoscUdzialu, mianownikUlamkaOkreslajacegoWartoscUdzialu, podmiotUdzialuWlasnosci, przedmiotUdzialuWlasnosci)

def stworz_adres(adres):
    miejscowosc = adres.find('egb:miejscowosc').text
    kodPocztowy = adres.find('egb:kodPocztowy').text if adres.find('egb:kodPocztowy') is not None else None
    ulica = adres.find('egb:ulica').text if adres.find('egb:ulica') is not None else None
    numerPorzadkowy = adres.find('egb:numerPorzadkowy').text

    return Adres(miejscowosc, kodPocztowy, ulica, numerPorzadkowy)

def stworz_osobe(osobaFizyczna, adres):
    pierwszeImie = osobaFizyczna.find('egb:pierwszeImie').text
    pierwszyCzlonNazwiska = osobaFizyczna.find('egb:pierwszyCzlonNazwiska').text
    drugiCzlonNazwiska = osobaFizyczna.find('egb:drugiCzlonNazwiska').text if osobaFizyczna.find('egb:drugiCzlonNazwiska') is not None else ''
    drugieImie = osobaFizyczna.find('egb:drugieImie').text if osobaFizyczna.find('egb:drugieImie') is not None else ''
    imieOjca = osobaFizyczna.find('egb:imieOjca').text
    imieMatki = osobaFizyczna.find('egb:imieMatki').text
    pesel = osobaFizyczna.find('egb:pesel').text if osobaFizyczna.find('egb:pesel') is not None else ''
    plec = osobaFizyczna.find('egb:plec').text
    status = osobaFizyczna.find('egb:status').text
    informacjaOSmierci = osobaFizyczna.find('egb:informacjaOSmierci').text if osobaFizyczna.find('egb:informacjaOSmierci') is not None else ''

    adresOsobyFizycznej = stworz_adres(adres)

    return OsobaFizyczna(pierwszeImie, pierwszyCzlonNazwiska, drugieImie, imieOjca, imieMatki, pesel, plec, status, adresOsobyFizycznej, drugiCzlonNazwiska, informacjaOSmierci)

def stworz_instytucje(instytucja, adres):
    nazwaPelna = instytucja.find('egb:nazwaPelna').text
    nazwaSkrocona = instytucja.find('egb:nazwaSkrocona').text
    regon = instytucja.find('egb:regon').text
    status = instytucja.find('egb:status').text
    adresInstytucji = stworz_adres(adres)

    return Instytucja(nazwaPelna, nazwaSkrocona, regon, status, adresInstytucji)

def stworz_podmiot(podmiot, soup):
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

def stworz_jednostke_ewid(jednostka):
    idJednostkiEwid = jednostka.find('egb:idJednostkiEwid').text
    geometria = jednostka.find('egb:geometria').text
    nazwaWlasna = jednostka.find('egb:nazwaWlasna').text

    return JednostkaEwidencyjna(idJednostkiEwid, geometria, nazwaWlasna)

def stworz_obreb_ewid(obreb, soup):
    idObrebu = obreb.find('egb:idObrebu').text
    geometria = obreb.find('egb:geometria').text
    nazwaWlasna = obreb.find('egb:nazwaWlasna').text
    jednostkaEwid_link = obreb.find('egb:lokalizacjaObrebu').get('xlink:href')
    jednostkaEwid = soup.find('egb:EGB_JednostkaEwidencyjna', {'gml:id': jednostkaEwid_link})
    jednostkaEwid_id = jednostkaEwid.find('egb:idJednostkiEwid').text

    return ObrebEwidencyjny(idObrebu, geometria, nazwaWlasna, jednostkaEwid_id)

def stworz_obiekt_trwale_zwiazany(obiekt, soup):
    geometria = obiekt.find('egb:geometria').text
    rodzaj = obiekt.find('egb:rodzajObiektuZwiazanegoZBudynkiem').text
    budynek_link = obiekt.find('egb:budynekZElementamiZwiazanymi').get('xlink:href')
    budynek = soup.find('egb:EGB_Budynek', {'gml:id': budynek_link})
    idBudynku = budynek.find('egb:idBudynku').text

    return ObiektTrwaleZwiazany(geometria, rodzaj, idBudynku)

def stworz_blok(blok, soup):
    geometria = blok.find('egb:geometria').text
    rodzaj = blok.find('egb:rodzajBloku').text
    oznaczenie = blok.find('egb:oznaczenieBloku').text
    numerNajnizszejKondygnacji = blok.find('egb:numerNajnizszejKondygnacji').text
    numerNajwyzszejKondygnacji = blok.find('egb:numerNajwyzszejKondygnacji').text
    budynek_link = blok.find('egb:budynekZBlokiemBud').get('xlink:href')
    budynek = soup.find('egb:EGB_Budynek', {'gml:id': budynek_link})
    idBudynku = budynek.find('egb:idBudynku').text

    return BlokBudynku(geometria, rodzaj, oznaczenie, numerNajnizszejKondygnacji, numerNajwyzszejKondygnacji, idBudynku)

def stworz_punkt_graniczny(punkt):
    idPunktu = punkt.find('egb:idPunktu').text
    geometria = punkt.find('egb:geometria').text
    sposobPozyskania = punkt.find('egb:sposobPozyskania').text if punkt.find('egb:sposobPozyskania') is not None else None
    spelnienieWarunkowDokl = punkt.find('egb:spelnienieWarunkowDokl').text
    rodzajStabilizacji = punkt.find('egb:rodzajStabilizacji').text
    oznWMaterialeZrodlowym = punkt.find('egb:oznWMaterialeZrodlowym').text if punkt.find('egb:oznWMaterialeZrodlowym') is not None else None
    numerOperatuTechnicznego = punkt.find('egb:numerOperatuTechnicznego').text if punkt.find('egb:numerOperatuTechnicznego') is not None else None
    dodatkoweInformacje = punkt.find('egb:dodatkoweInformacje').text if punkt.find('egb:dodatkoweInformacje') is not None else None

    return PunktGraniczny(geometria, idPunktu, sposobPozyskania, spelnienieWarunkowDokl, rodzajStabilizacji, oznWMaterialeZrodlowym, numerOperatuTechnicznego, dodatkoweInformacje)

def stworz_adres_nieruchomosci(adres):
    nazwaMiejscowosci = adres.find('egb:nazwaMiejscowosci').text
    idMiejscowosci = adres.find('egb:idMiejscowosci').text if adres.find('egb:idMiejscowosci') is not None else ''
    nazwaUlicy = adres.find('egb:nazwaUlicy').text if adres.find('egb:nazwaUlicy') is not None else ''
    idNazwyUlicy = adres.find('egb:idNazwyUlicy').text if adres.find('egb:idNazwyUlicy') is not None else ''
    numerPorzadkowy = adres.find('egb:numerPorzadkowy').text if adres.find('egb:numerPorzadkowy') is not None else ''
    numerLokalu = adres.find('egb:numerLokalu').text if adres.find('egb:numerLokalu') is not None else ''
    geometria = adres.find('egb:geometria').text

    return AdresNieruchomosci(nazwaMiejscowosci, idMiejscowosci, nazwaUlicy, idNazwyUlicy, numerPorzadkowy, numerLokalu, geometria)


def read_gml(file):
    with open(file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'xml')

    dzialki = {}
    budynki = []
    kontury_klasyfikacyjne = []
    kontury_uzytku = []
    jednostki_ewidencyjne = {}
    obreby_ewidencyjne = {}
    obiekty_trwale_zwiazane = []
    bloki = []
    punkty = []
    
    for jednostka in soup.find_all('egb:EGB_JednostkaEwidencyjna'):
        obiekt_jednostka = stworz_jednostke_ewid(jednostka)
        jednostki_ewidencyjne[obiekt_jednostka.idJednostkiEwid] = obiekt_jednostka

    for obreb in soup.find_all('egb:EGB_ObrebEwidencyjny'):
        obiekt_obreb = stworz_obreb_ewid(obreb, soup)
        obreby_ewidencyjne[obiekt_obreb.idObrebu] = obiekt_obreb

    for dzialka in soup.find_all('egb:EGB_DzialkaEwidencyjna'):
        obiekt_dzialka = stworz_dzialke(dzialka, soup)
        for klasouzytek in dzialka.find_all('egb:klasouzytek'):
            obiekt_klasouzytek = stworz_klasouzytek(klasouzytek)
            obiekt_dzialka.add_klasouzytek(obiekt_klasouzytek)
        dzialki[obiekt_dzialka.idDzialki] = obiekt_dzialka
    
    for budynek in soup.find_all('egb:EGB_Budynek'):
        dzialka_link = budynek.find('egb:dzialkaZabudowana').get('xlink:href')
        dzialka = soup.find('egb:EGB_DzialkaEwidencyjna', {'gml:id': dzialka_link})
        id_dzialki = dzialka.find('egb:idDzialki').text
        dzialka = dzialki[id_dzialki] if id_dzialki in dzialki else None
        obiekt_budynek = stworz_budynek(budynek, dzialka, soup)
        budynki.append(obiekt_budynek)
        dzialki[id_dzialki].add_budynek(obiekt_budynek) if id_dzialki in dzialki else None
    
    for obiekt in soup.find_all('egb:EGB_ObiektTrwaleZwiazanyZBudynkiem'):
        obiekt_trwale_zwiazany = stworz_obiekt_trwale_zwiazany(obiekt, soup)
        obiekty_trwale_zwiazane.append(obiekt_trwale_zwiazany)

    for blok in soup.find_all('egb:EGB_BlokBudynku'):
        obiekt_blok = stworz_blok(blok, soup)
        bloki.append(obiekt_blok)
    
    for punkt in soup.find_all('egb:EGB_PunktGraniczny'):
        obiekt_punkt = stworz_punkt_graniczny(punkt)
        punkty.append(obiekt_punkt)

    for kontur in soup.find_all('egb:EGB_KonturKlasyfikacyjny'):
        obiekt_kontur = stworz_kontur_klasyfikacyjny(kontur, soup)
        kontury_klasyfikacyjne.append(obiekt_kontur)
    
    for kontur in soup.find_all('egb:EGB_KonturUzytkuGruntowego'):
        obiekt_kontur = stworz_kontur_uzytku(kontur, soup)
        kontury_uzytku.append(obiekt_kontur)

    for udzial in soup.find_all('egb:EGB_UdzialWeWlasnosci'):
        for podmiotUdzialuWlasnosci in udzial.find_all('egb:EGB_Podmiot'):
            for child in podmiotUdzialuWlasnosci.children:
                if child.name:
                    podmiot = stworz_podmiot(child, soup)
        
        JRG = udzial.find('egb:JRG').get('xlink:href') 
        przedmiot = soup.find('egb:JRG2', {'xlink:href': JRG}).parent
        id_przedmiotu = przedmiot.find('egb:idDzialki').text
        przedmiot = dzialki[id_przedmiotu] if id_przedmiotu in dzialki else None
        obiekt_udzial = stworz_udzial(udzial, podmiot, przedmiot)
        dzialki[id_przedmiotu].add_udzial(obiekt_udzial) if id_przedmiotu in dzialki else None
    
    return dzialki, budynki, kontury_klasyfikacyjne, kontury_uzytku, jednostki_ewidencyjne, obreby_ewidencyjne, obiekty_trwale_zwiazane, bloki, punkty