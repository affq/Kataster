from stworz_obiekty import *
import folium
from pyproj import Transformer
from shapely.geometry import Polygon

transformer = Transformer.from_proj(2178, 4326)

import webbrowser

def geostring_to_coords(geostring):
    coords = list(map(float, geostring.split()))
    coords_2180 = [(coords[i], coords[i + 1]) for i in range(0, len(coords), 2)]
    coords_4326 = [transformer.transform(x, y) for x, y in coords_2180]
    return coords_4326

def format_udzialy(udzialy):
    if udzialy:
        udzialy = sorted(
            udzialy,
            key=lambda udzial: float(udzial.licznikUlamkaOkreslajacegoWartoscUdzialu) / float(udzial.mianownikUlamkaOkreslajacegoWartoscUdzialu),
            reverse=True
        )
        tabelka_html = """
        <table border="1">
            <thead>
                <tr>
                    <th>udział</th>
                    <th>rodzaj podmiotu</th>
                    <th>podmiot</th>
                </tr>
            </thead>
            <tbody>
        """
        for udzial in udzialy:
            if type(udzial.podmiotUdzialuWlasnosci) == Instytucja:
                rodzaj_podmiotu = "instytucja"
                podmiot = udzial.podmiotUdzialuWlasnosci.nazwaPelna
            elif type(udzial.podmiotUdzialuWlasnosci) == OsobaFizyczna:
                rodzaj_podmiotu = "osoba"
                podmiot = udzial.podmiotUdzialuWlasnosci
            elif type(udzial.podmiotUdzialuWlasnosci) == Malzenstwo:
                rodzaj_podmiotu = "małżeństwo"
                podmiot = udzial.podmiotUdzialuWlasnosci
            tabelka_html += f"""
                <tr>
                    <td>{udzial.licznikUlamkaOkreslajacegoWartoscUdzialu}/{udzial.mianownikUlamkaOkreslajacegoWartoscUdzialu}</td>
                    <td>{rodzaj_podmiotu}</td>
                    <td>{podmiot}</td>
                </tr>
            """
        tabelka_html += """
            </tbody>
        </table>
        """
        return tabelka_html
    return "brak informacji"

def format_budynki(budynki):
    if budynki:
        tabelka_html = """
        <table border="1">
            <thead>
                <tr>
                    <th>nr budynku</th>
                    <th>rodzaj wg KST</th>
                    <th>powierzchnia zabudowy</th>
                </tr>
            </thead>
            <tbody>
        """
        for budynek in budynki:
            tabelka_html += f"""
                <tr>
                    <td>{budynek.nrBudynku}</td>
                    <td>{budynek.rodzajWgKST}</td>
                    <td>{budynek.powZabudowy} m<sup>2</sup></td>
                </tr>
            """
        tabelka_html += """
            </tbody>
        </table>
        """
        return tabelka_html
    return "brak"

def format_klasouzytki(klasouzytki):
    tabelka_html = """
    <table border="1">
        <thead>
            <tr>
                <th>OFU</th>
                <th>OZU</th>
                <th>OZK</th>
                <th>powierzchnia</th>
            </tr>
        </thead>
        <tbody>
    """
    for klasouzytek in klasouzytki:
        tabelka_html += f"""
            <tr>
                <td>{klasouzytek.OFU}</td>
                <td>{klasouzytek.OZU}</td>
                <td>{klasouzytek.OZK}</td>
                <td>{klasouzytek.powierzchnia} ha</td>
            </tr>
        """
    tabelka_html += """
        </tbody>
    </table>
    """
    return tabelka_html

grunty_dict = {
    'R': 'grunt orny',
    'Ł': 'łąka trwała',
    'Ps': 'pastwisko trwałe',
    'S': 'sad',
    'Br': 'grunt rolny zabudowany',
    'Lzr': 'grunt zadrzewiony i zakrzewiony na użytku rolnych',
    'Wsr': 'grunt pod stawem',
    'W': 'grunt pod rowem',
    'N': 'nieużytek',
    'Ls': 'las',
    'Lz': 'grunt zadrzewiony i zakrzewiony',
    'B': 'teren mieszkaniowy',
    'Ba': 'teren przemysłowy',
    'Bi': 'inny teren zabudowany',
    'Bp': 'zurbanizowany teren niezabudowany lub w trakcie zabudowy',
    'Bz': 'teren rekreacyjno-wypoczynkowy',
    'K': 'użytek kopalny',
    'dr': 'droga',
    'Tk': 'teren kolejowy',
    'Ti': 'inny teren komunikacyjny',
    'Tp': 'grunt przeznaczony pod budowę drogi publicznej lub linii kolejowej',
    'Wm': 'grunt pod morskimi wodami wewnętrznymi',
    'Wp': 'grunt pod wodami powierzchniowymi płynącymi',
    'Ws': 'grunt pod wodami powierzchniowymi stojącymi',
    'Tr': 'teren różny'
}

wg_kst = {
    'm': 'mieszkalny',
    'g': 'produkcyjny/usługowy/gospodarczy',
    't': 'transportu/łączności',
    'k': 'oświaty/nauki/kultury/sportu',
    'z': 'szpitala/opieki zdrowotnej',
    'b': 'biurowy',
    'h': 'handlowo-usługowy',
    'p': 'przemysłowy',
    's': 'magazynowy/silos',
    'i': 'niemieszkalny'
}

rodzaj_obiektu_dict = {
    't': 'taras',
    'w': 'weranda/ganek',
    'i': 'wiatrołap',
    's': 'schody',
    'r': 'rampa',
    'o': 'podpora',
    'j': 'wjazd do podziemia',
    'd': 'podjazd dla osób niepełnosprawnych'
}

rodzaj_bloku_dict = {
    'n': 'kondygnacje nadziemne',
    'p': 'kondygnacje podziemne',
    'l': 'łącznik',
    'a': 'nawis',
    'z': 'przejazd przez budynek',
    'y': 'inny'
}

sposob_pozyskania_dict = {
    "1": "ustalony",
    "2": "nieustalony"
}

kod_stabilizacji_dict = {
    "1": "brak informacji",
    "2": "niestabilizowany",
    "3": "znak naziemny",
    "4": "znak naziemny i podziemny",
    "5": "znak podziemny",
    "6": "szczegół terenowy"
}

spelnienie_warunkow_dict = {
    "1": "spełnia",
    "2": "nie spełnia"
}

def popup_jednostka_ewidencyjna(jednostka):
    popup = f"""
    <h3><b>{jednostka.nazwaWlasna}</b></h3>
    <p><b>id jednostki</b>: {jednostka.idJednostkiEwid}</p>
"""
    return popup

DZIALKA_KOLOR = "#008000"
KONTUR_KLASYFIKACYJNY_KOLOR = "#adfc33"
UZYTEK_GRUNTOWY_KOLOR = "#90ee90"
BUDYNEK_KOLOR = "#000000"

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("gml_file", help="ścieżka do pliku GML")
args = parser.parse_args()

class GML():
    def __init__(self):
        self.dzialki = None
        self.budynki = None
        self.kontury_klasyfikacyjne = None
        self.kontury_uzytkow = None
        self.jednostki_ewidencyjne = None
        self.obreby_ewidencyjne = None
        self.obiekty_trwale_zwiazane = None
        self.bloki = None
        self.punkty_graniczne = None
        self.map = None
        self.out_map = "projekt-2-gml/web/map.html"

    def load_gml(self, file):
        # file_dialog = QFileDialog(self)
        # file, _ = file_dialog.getOpenFileName(
        #     self, "Wybierz plik GML", "", "Pliki GML (*.gml *.xml);;Wszystkie pliki (*.*)"
        # )
        if file:
            (
                self.dzialki, 
                self.budynki, 
                self.kontury_klasyfikacyjne, 
                self.kontury_uzytkow, 
                self.jednostki_ewidencyjne, 
                self.obreby_ewidencyjne, 
                self.obiekty_trwale_zwiazane, 
                self.bloki, 
                self.punkty_graniczne,
            ) = read_gml(file)
            self.create_map()
        else:
            return
    
    def popup_dzialka(self, dzialka):
        popup = f"""
        <h3><b>{dzialka.nrDzialki}</b></h3>
        <p><b>działka</b>: {dzialka.idDzialki}</p>
        <p><b>obręb ewidencyjny</b>: {dzialka.obreb_id} ({self.obreby_ewidencyjne[dzialka.obreb_id].nazwaWlasna})</p>
        <p><b>jednostka ewidencyjna</b>: {self.obreby_ewidencyjne[dzialka.obreb_id].jednostkaEwid_id} ({self.jednostki_ewidencyjne[self.obreby_ewidencyjne[dzialka.obreb_id].jednostkaEwid_id].nazwaWlasna})</p>
        <p><b>numer KW</b>: {dzialka.numerKW}</p>
        <p><b>pole ewidencyjne</b>: {dzialka.poleEwidencyjne} ha</p>
        <p><b>klasoużytki</b>: {format_klasouzytki(dzialka.klasouzytki)}</p>
        <p><b>udziały</b>: {format_udzialy(dzialka.udzialy)}</p>
        <p><b>budynki</b>: {format_budynki(dzialka.budynki)}</p>
    """ 
        return popup

    def popup_obreb_ewidencyjny(self, obreb):
        popup = f"""
        <h3><b>{obreb.nazwaWlasna}</b></h3>
        <p><b>obręb</b>: {obreb.idObrebu}</p>
        <p><b>jednostka </b>: {obreb.jednostkaEwid_id} ({self.jednostki_ewidencyjne[obreb.jednostkaEwid_id].nazwaWlasna})</p>
    """
        return popup

    def popup_kontur_uzytku(self, kontur):
        popup = f"""
        <h3> <b>{kontur.OFU}</b></h3>
        <p><b>użytek</b>: {kontur.idKonturu}</p>
        <p><b>obręb ewidencyjny</b>: {kontur.obreb_id} ({self.obreby_ewidencyjne[kontur.obreb_id].nazwaWlasna})</p>
        <p><b>jednostka ewidencyjna</b>: {self.obreby_ewidencyjne[kontur.obreb_id].jednostkaEwid_id} ({self.jednostki_ewidencyjne[self.obreby_ewidencyjne[kontur.obreb_id].jednostkaEwid_id].nazwaWlasna})</p>
        <p><b>OFU</b>: {kontur.OFU} ({grunty_dict[kontur.OFU]})</p>
    """
        return popup

    def popup_kontur_klasyfikacyjny(self, kontur):
        popup = f"""
        <h3><b>{kontur.OZU}{kontur.OZK}</b></h3>
        <p><b>kontur</b>: {kontur.idKonturu}</p>
        <p><b>obręb ewidencyjny</b>: {kontur.obreb_id} ({self.obreby_ewidencyjne[kontur.obreb_id].nazwaWlasna})</p>
        <p><b>jednostka ewidencyjna</b>: {self.obreby_ewidencyjne[kontur.obreb_id].jednostkaEwid_id} ({self.jednostki_ewidencyjne[self.obreby_ewidencyjne[kontur.obreb_id].jednostkaEwid_id].nazwaWlasna})</p>
        <p><b>OZU</b>: {kontur.OZU} ({grunty_dict[kontur.OZU]})</p>
        <p><b>OZK</b>: {kontur.OZK}</p>
    """
        return popup

    def popup_budynek(self, budynek):
        popup = f"""
        <h3><b>budynek {wg_kst[budynek.rodzajWgKST]}</b></h3>
        <p><b>budynek</b>: {budynek.idBudynku}</p>
        <p><b>działka</b>: {budynek.dzialka.idDzialki}</p>
        <p><b>obręb ewidencyjny</b>: {budynek.dzialka.obreb_id} ({self.obreby_ewidencyjne[budynek.dzialka.obreb_id].nazwaWlasna})</p>
        <p><b>jednostka ewidencyjna</b>: {self.obreby_ewidencyjne[budynek.dzialka.obreb_id].jednostkaEwid_id} ({self.jednostki_ewidencyjne[self.obreby_ewidencyjne[budynek.dzialka.obreb_id].jednostkaEwid_id].nazwaWlasna})</p>
        <p><b>rodzaj wg KST</b>: {budynek.rodzajWgKST}</p>
        <p><b>liczba kondygnacji nadziemnych</b>: {budynek.liczbaKondygnacjiNadziemnych}</p>
        <p><b>liczba kondygnacji podziemnych</b>: {budynek.liczbaKondygnacjiPodziemnych}</p>
        <p><b>powierzchnia zabudowy</b>: {budynek.powZabudowy} m<sup>2</sup></p>
    """
        return popup

    def popup_obiekt_zwiazany(self, obiekt):
        popup = f"""
        <h3><b>obiekt trwale związany</b></h3>
        <p><b>z budynkiem</b>: {obiekt.idBudynku}</p>
        <p><b>rodzaj obiektu</b>: {obiekt.rodzaj} ({rodzaj_obiektu_dict[obiekt.rodzaj]})</p>
    """ 
        return popup 
    
    def popup_blok(self, blok):
        popup = f"""
        <h3><b>blok</b></h3>
        <p><b>budynek</b>: {blok.idBudynku}</p>
        <p><b>rodzaj</b>: {rodzaj_bloku_dict[blok.rodzaj]}</p>
        <p><b>oznaczenie</b>: {blok.oznaczenie}</p>
        <p><b>numer najwyższej kondygnacji</b>: {blok.numerNajwyzszejKondygnacji}</p>
        <p><b>numer najniższej kondygnacji</b>: {blok.numerNajnizszejKondygnacji}</p>
    """
        return popup
    
    def popup_punkt_graniczny(self, punkt):
        popup = f"""
        <h3><b>punkt graniczny</b></h3>
        <p><b>identyfikator</b>: {punkt.idPunktu}</p>
        <p><b>sposób pozyskania</b>: {sposob_pozyskania_dict[punkt.sposobPozyskania]}</p>
        <p><b>spełnienie warunków</b>: {spelnienie_warunkow_dict[punkt.spelnienieWarunkowDokl]}</p>
        <p><b>rodzaj stabilizacji</b>: {kod_stabilizacji_dict[punkt.rodzajStabilizacji]}</p>
        <p><b>oznaczenie w materiale źródłowym</b>: {punkt.oznWMaterialeZrodlowym}</p>
        <p><b>numer operatu technicznego</b>: {punkt.numerOperatuTechnicznego}</p>
        <p><b>dodatkowe informacje</b>: {punkt.dodatkoweInformacje}</p>
    """
        return popup

    def create_map(self):
        self.map = folium.Map(location=[52.26548704146309, 20.552917654453303], zoom_start=17, tiles="CartoDB Positron")
        css_link = r'<link rel="stylesheet" type="text/css" href="C:\Users\adria\Desktop\STUDIA_FOLDERY\zinformatyzowane-systemy-katastralne\projekt-2-gml\web\static\css\wspolny.css"/>'
        folium.Element(css_link).add_to(self.map.get_root().html)
        js_link = r'<script src="C:\Users\adria\Desktop\STUDIA_FOLDERY\zinformatyzowane-systemy-katastralne\projekt-2-gml\web\static\js\control.js"></script>'
        folium.Element(js_link).add_to(self.map.get_root().html)
        
        jednostki_ewidencyjne_fg = folium.FeatureGroup(name="jednostki ewidencyjne")
        for jednostka in self.jednostki_ewidencyjne.values():
            coords = geostring_to_coords(jednostka.geometria)

            poly = folium.Polygon(
                locations=coords,
                color='gray',
                fill=False,
                fill_color='red',
                fill_opacity=0,
                weight=1,
                popup=popup_jednostka_ewidencyjna(jednostka)
            ).add_to(jednostki_ewidencyjne_fg)
        jednostki_ewidencyjne_fg.add_to(self.map)

        obreby_ewidencyjne_fg = folium.FeatureGroup(name="obręby ewidencyjne")
        for obreb in self.obreby_ewidencyjne.values():
            coords = geostring_to_coords(obreb.geometria)
            folium.Polygon(
                locations=coords,
                color='black',
                fill=False,
                weight=1,
                fill_color='red',
                fill_opacity=0,
                popup=self.popup_obreb_ewidencyjny(obreb),
            ).add_to(obreby_ewidencyjne_fg)
        obreby_ewidencyjne_fg.add_to(self.map)

        kontury_uzytkow_fg = folium.FeatureGroup(name="kontury użytków")
        for kontur in self.kontury_uzytkow:
            coords = geostring_to_coords(kontur.geometria)
            folium.Polygon(
                locations=coords,
                color=UZYTEK_GRUNTOWY_KOLOR,
                fill=False,
                weight=1,
                fill_color='red',
                fill_opacity=0,
                popup=self.popup_kontur_uzytku(kontur)
            ).add_to(kontury_uzytkow_fg)

            centroid = Polygon(coords).centroid
            folium.Marker(
                location=[centroid.x, centroid.y],
                icon=folium.DivIcon(html=f'<div class="marker" style="color:{UZYTEK_GRUNTOWY_KOLOR}">{kontur.OFU}</div>')
            ).add_to(kontury_uzytkow_fg)
        kontury_uzytkow_fg.add_to(self.map)

        kontury_klasyfikacyjne_fg = folium.FeatureGroup(name="kontury klasyfikacyjne")
        for kontur in self.kontury_klasyfikacyjne:
            coords = geostring_to_coords(kontur.geometria)
            folium.Polygon(
                locations=coords,
                color=KONTUR_KLASYFIKACYJNY_KOLOR,
                fill=False,
                weight=1,
                fill_color='red',
                fill_opacity=0,
                popup=self.popup_kontur_klasyfikacyjny(kontur)
            ).add_to(kontury_klasyfikacyjne_fg)

            centroid = Polygon(coords).centroid
            folium.Marker(
                location=[centroid.x, centroid.y],
                icon=folium.DivIcon(html=f'<div class="marker" style="color:{KONTUR_KLASYFIKACYJNY_KOLOR}">{kontur.OZU}{kontur.OZK}</div>')
            ).add_to(kontury_klasyfikacyjne_fg)
        kontury_klasyfikacyjne_fg.add_to(self.map)

        dzialki_fg = folium.FeatureGroup(name="działki")
        for dzialka in self.dzialki.values():
            coords = geostring_to_coords(dzialka.geometria)
            folium.Polygon(
                locations=coords,
                color=DZIALKA_KOLOR,
                fill=False,
                weight=2,
                fill_color='red',
                fill_opacity=0,
                popup=self.popup_dzialka(dzialka)
            ).add_to(dzialki_fg)

            centroid = Polygon(coords).centroid
            folium.Marker(
                location=[centroid.x, centroid.y],
                icon=folium.DivIcon(html=f'<div class="marker" style="color:{DZIALKA_KOLOR}">{dzialka.nrDzialki}</div>')
            ).add_to(dzialki_fg)
        dzialki_fg.add_to(self.map)

        budynki_fg = folium.FeatureGroup(name="budynki")
        for budynek in self.budynki:
            coords = geostring_to_coords(budynek.geometria)
            poly = folium.Polygon(
                locations=coords,
                color=BUDYNEK_KOLOR,
                fill=False,
                weight=3,
                fill_color='red',
                fill_opacity=0,
                popup=self.popup_budynek(budynek)
            ).add_to(budynki_fg)

            centroid = Polygon(coords).centroid
            folium.Marker(
                location=[centroid.x, centroid.y],
                icon=folium.DivIcon(html=f'<div class="marker" style="color:{BUDYNEK_KOLOR}">{budynek.rodzajWgKST}</div>')
            ).add_to(budynki_fg)
        budynki_fg.add_to(self.map)

        obiekty_trwale_zwiazane_fg = folium.FeatureGroup(name="obiekty trwale związane")
        for obiekt in self.obiekty_trwale_zwiazane:
            coords = geostring_to_coords(obiekt.geometria)
            folium.Polygon(
                locations=coords,
                color='black',
                fill=False,
                fill_color='black',
                fill_opacity=0,
                weight=3,
                popup=self.popup_obiekt_zwiazany(obiekt)
            ).add_to(obiekty_trwale_zwiazane_fg)
        obiekty_trwale_zwiazane_fg.add_to(self.map)

        bloki_fg = folium.FeatureGroup(name="bloki")
        for blok in self.bloki:
            coords = geostring_to_coords(blok.geometria)
            folium.Polygon(
                locations=coords,
                color='black',
                fill=False,
                fill_color='black',
                fill_opacity=0,
                weight=3,
                popup=self.popup_blok(blok)
            ).add_to(bloki_fg)
        bloki_fg.add_to(self.map)

        punkty_graniczne_fg = folium.FeatureGroup(name="punkty graniczne")
        for punkt in self.punkty_graniczne:
            coords = geostring_to_coords(punkt.geometria)
            folium.CircleMarker(
                location=coords[0], 
                radius=2,
                color='red',
                fill=True,
                fill_color='red',
                fill_opacity=0.5,
                popup=self.popup_punkt_graniczny(punkt)
            ).add_to(punkty_graniczne_fg)
        punkty_graniczne_fg.add_to(self.map)

        folium.LayerControl(collapsed=False).add_to(self.map)
        self.map.save(self.out_map)

if __name__ == '__main__':
    gml = GML()
    gml.load_gml(args.gml_file)



