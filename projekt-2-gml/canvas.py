import customtkinter as ctk
from tkinter import filedialog
from stworz_obiekty import *
import folium
from pyproj import Transformer
from shapely.geometry import Polygon

transformer = Transformer.from_proj(2178, 4326)

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


def popup_jednostka_ewidencyjna(jednostka):
    popup = f"""
    <h3><b>{jednostka.nazwaWlasna}</b></h3>
    <p><b>id jednostki</b>: {jednostka.idJednostkiEwid}</p>
"""
    return popup 

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme(r"projekt-2-gml/lavender.json")
        self.title("GML")
        self.geometry("1500x900")
        self.title("GML Reader")
        self.FONT = ("Helvetica", 13, "bold")
        self.dzialki = None
        self.budynki = None
        self.kontury_klasyfikacyjne = None
        self.kontury_uzytkow = None
        self.jednostki_ewidencyjne = None
        self.obreby_ewidencyjne = None
        self.map = None
        self.out_map = "projekt-2-gml/web/map.html"

        choose_file_button = ctk.CTkButton(self, text="Wczytaj plik GML", command=self.load_gml, font=self.FONT)
        choose_file_button.pack(padx=10, pady=10, fill='x')

        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        self.mainloop()

    def load_gml(self):
        file = filedialog.askopenfilename(title="Wybierz plik GML", filetypes=[("Pliki GML", "*.gml, *.xml"), ("Wszystkie pliki", "*.*")])
        if file:
            self.dzialki, self.budynki, self.kontury_klasyfikacyjne, self.kontury_uzytkow, self.jednostki_ewidencyjne, self.obreby_ewidencyjne = read_gml(file)
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

    def create_map(self):
        self.map = folium.Map(location=[52.26548704146309, 20.552917654453303], zoom_start=17, tiles="CartoDB Positron")
        css_link = r'<link rel="stylesheet" type="text/css" href="C:\Users\adria\Desktop\STUDIA_FOLDERY\zinformatyzowane-systemy-katastralne\projekt-2-gml\web\static\css\wspolny.css"/>'
        folium.Element(css_link).add_to(self.map.get_root().html)
        
        jednostki_ewidencyjne_fg = folium.FeatureGroup(name="jednostki ewidencyjne")
        for jednostka in self.jednostki_ewidencyjne.values():
            coords = geostring_to_coords(jednostka.geometria)
            folium.Polygon(
                locations=coords,
                color='gray',
                fill=False,
                weight=1,
                fill_color='red',
                fill_opacity=0,
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
                popup=self.popup_obreb_ewidencyjny(obreb)
            ).add_to(obreby_ewidencyjne_fg)
        obreby_ewidencyjne_fg.add_to(self.map)

        kontury_uzytkow_fg = folium.FeatureGroup(name="kontury użytków")
        for kontur in self.kontury_uzytkow:
            coords = geostring_to_coords(kontur.geometria)
            folium.Polygon(
                locations=coords,
                color='#90ee90',
                fill=False,
                weight=1,
                fill_color='green',
                fill_opacity=0,
                popup=self.popup_kontur_uzytku(kontur)
            ).add_to(kontury_uzytkow_fg)
        kontury_uzytkow_fg.add_to(self.map)

        kontury_klasyfikacyjne_fg = folium.FeatureGroup(name="kontury klasyfikacyjne")
        for kontur in self.kontury_klasyfikacyjne:
            coords = geostring_to_coords(kontur.geometria)
            folium.Polygon(
                locations=coords,
                color='#adfc33',
                fill=False,
                weight=1,
                fill_color='green',
                fill_opacity=0,
                popup=self.popup_kontur_klasyfikacyjny(kontur)
            ).add_to(kontury_klasyfikacyjne_fg)
        kontury_klasyfikacyjne_fg.add_to(self.map)

        dzialki_fg = folium.FeatureGroup(name="działki")
        for dzialka in self.dzialki.values():
            folium.Polygon(
                locations=geostring_to_coords(dzialka.geometria),
                color='black',
                fill=False,
                fill_color='blue',
                fill_opacity=0,
                weight=2,
                popup=self.popup_dzialka(dzialka)
            ).add_to(dzialki_fg)
        dzialki_fg.add_to(self.map)

        budynki_fg = folium.FeatureGroup(name="budynki")
        for budynek in self.budynki:
            coords = geostring_to_coords(budynek.geometria)
            poly = folium.Polygon(
                locations=coords,
                color='black',
                fill=False,
                fill_color='black',
                fill_opacity=0,
                weight=3,
                popup=self.popup_budynek(budynek)
            ).add_to(budynki_fg)
        budynki_fg.add_to(self.map)

        folium.LayerControl().add_to(self.map)
        self.map.save(self.out_map)
            



