import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import customtkinter as ctk
from tkinter import filedialog
from stworz_obiekty import *
from matplotlib.patches import Polygon

class Canvas:
    def __init__(self, root, main):
        self.dzialki = None
        self.budynki = None
        self.kontury = None
        self.root = root
        self.fig = plt.figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_axis_off()
        self.plt = plt
        self.plt.xticks([])
        self.plt.yticks([])
        self.plt.gca().set_xticks([])
        self.plt.gca().set_yticks([])
        self.plt.grid(False)
        self.ax.set_axis_off()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.root)
        self.canvas.mpl_connect('scroll_event', self.zoom)
        self.canvas.mpl_connect('button_press_event', self.mouse_button)
        self.canvas.mpl_connect('motion_notify_event', self.motion)
        # self.canvas.mpl_connect('pick_event', self.show_info)
        self.canvas.get_tk_widget().pack(fill='both', expand=True)
        self.pencil_color = 'black'
        self.pressed = None
        self.narysowane = {}
        self.main = main
        self.xlim = None
        self.ylim = None
    
    def reset(self):
        self.plt.xticks([])
        self.plt.yticks([])
        self.plt.gca().set_xticks([])
        self.plt.gca().set_yticks([])
        self.plt.grid(False)
        self.ax.set_axis_off()

    def zoom(self, event):
        factor = 0.8 if event.button == 'up' else 1.2
        new_xlim = self.get_lim(self.ax.get_xlim(), event.xdata, factor)
        new_ylim = self.get_lim(self.ax.get_ylim(), event.ydata, factor)
        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()
    
    def get_dist(self, lim, fig_size, xy, pressed_xy):
        dist = (lim[1] - lim[0]) / fig_size * (xy - pressed_xy)
        return lim[0] - dist, lim[1] - dist

    def mouse_button(self, event):
        if event.button == plt.MouseButton.LEFT:
            self.pressed = (event.x, event.y)
            self.xlim = self.ax.get_xlim()
            self.ylim = self.ax.get_ylim()
        if event.dblclick:  # Sprawdzanie podwójnego kliknięcia
            for artist in reversed(self.ax.patches):  # Przeszukiwanie obiektów na osi
                if artist.contains_point((event.x, event.y)):
                    label = artist.get_label()
                    print(f'Podwójne kliknięcie na obiekcie: {label}')
                    return
    
    def get_lim(self, lim, data, factor):
        l_dist = (data - lim[0]) * factor
        r_dist = (lim[1] - data) * factor
        return data - l_dist, data + r_dist

    def motion(self, event):
        try:
            if event.button == plt.MouseButton.LEFT:
                fig_size = self.fig.get_size_inches() * self.fig.dpi
                self.ax.set_xlim(self.get_dist(self.xlim, fig_size[0], event.x, self.pressed[0]))
                self.ax.set_ylim(self.get_dist(self.ylim, fig_size[1], event.y, self.pressed[1]))
                self.canvas.draw()
        except TypeError:
            pass
    
    def draw_polygon(self, obiekt):
        koordynaty = list(map(float, obiekt.geometria.split()))
        x = koordynaty[::2]
        y = koordynaty[1::2]
        polygon = Polygon(list(zip(x, y)), closed=True, color=obiekt.color, alpha=0.5, picker=True, label=obiekt.podpis, fill=False)
        self.ax.add_patch(polygon)

        if isinstance(obiekt, Budynek):
            x = sum(x) / len(x) - 5
        else:
            x = sum(x) / len(x) - 15

        y = sum(y) / len(y)
        self.ax.text(x, y, obiekt.podpis, fontsize=8, color=obiekt.color)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()
        self.narysowane[obiekt.podpis] = obiekt
        obiekt.polygon = polygon
    
    def add_objects(self, dzialki, budynki, kontury):
        self.dzialki = dzialki
        self.budynki = budynki
        self.kontury = kontury
    
    def change_visibility(self, obiekt):
        if obiekt.narysowany:
            obiekt.narysowany = False
            self.narysowane.pop(obiekt.podpis)
        else:
            obiekt.narysowany = True
            self.narysowane[obiekt.podpis] = obiekt
        self.xlim = self.ax.get_xlim()
        self.ylim = self.ax.get_ylim()
        self.redraw()

    def redraw(self):
        self.ax.clear()
        self.reset()
        for obiekt in self.narysowane.values():
            koordynaty = list(map(float, obiekt.geometria.split()))
            x = koordynaty[::2]
            y = koordynaty[1::2]
            polygon = Polygon(list(zip(x, y)), closed=True, color=obiekt.color, alpha=0.5, picker=True, label=obiekt.podpis, fill=False)
            self.ax.add_patch(polygon)

            if isinstance(obiekt, Budynek):
                x = sum(x) / len(x) - 5
            else:
                x = sum(x) / len(x) - 15
            y = sum(y) / len(y)
            self.ax.text(x, y, obiekt.podpis, fontsize=8, color=obiekt.color)
            self.narysowane[obiekt.podpis] = obiekt
            self.ax.set_xlim(self.xlim)
            self.ax.set_ylim(self.ylim)
            self.canvas.draw()
            obiekt.polygon = polygon
    
    def show_info(self, event): 
        if event.mouseevent.name != 'button_press_event':
            return  # Ignoruj inne typy zdarzeń (np. scrollowanie)
        artist = event.artist  # Obiekt graficzny (np. linia wielokąta)
        label = artist.get_label()  # Etykieta przypisana do obiektu
        print(f'Wybrano obiekt: {label}')

class MainWindow(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_default_color_theme(r"projekt-2-gml/lavender.json")
        self.title("GML")
        self.geometry("1500x900")
        self.title("GML Reader")
        self.FONT = ("Helvetica", 13, "bold")
        self.canvas = None
        self.dzialki = None
        self.budynki = None
        self.kontury = None
        
        choose_file_button = ctk.CTkButton(self, text="Wczytaj plik GML", command=self.load_gml, font=self.FONT)
        choose_file_button.pack(padx=10, pady=10, fill='x')

        frame = ctk.CTkFrame(self)
        frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.obiekty_frame = ctk.CTkFrame(frame)
        self.obiekty_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

        self.obiekty_frame_label = ctk.CTkLabel(self.obiekty_frame, text="OBIEKTY", font=self.FONT)
        self.obiekty_frame_label.pack()

        self.dzialki_frame = ctk.CTkFrame(self.obiekty_frame)
        self.dzialki_frame.configure(width=10, height=40)

        self.dzialki_nad_button = ctk.CTkFrame(self.dzialki_frame)
        self.dzialki_nad_button.pack(side=ctk.TOP, padx=10, pady=10, fill='x')

        self.dzialki_frame_label = ctk.CTkLabel(self.dzialki_nad_button, text="DZIAŁKI", font=self.FONT)
        self.dzialki_frame_label.pack(fill="both", expand=True)

        self.dzialki_left_frame = ctk.CTkFrame(self.dzialki_nad_button)
        self.dzialki_left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="x", expand=True)

        self.dzialki_right_frame = ctk.CTkFrame(self.dzialki_nad_button)
        self.dzialki_right_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="x", expand=True)

        self.canvas_frame = ctk.CTkFrame(frame)
        self.canvas_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

        self.canvas = Canvas(self.canvas_frame, self)

        self.budynki_frame = ctk.CTkFrame(self.obiekty_frame)
        self.budynki_frame.configure(width=10, height=40)

        self.budynki_frame_label = ctk.CTkLabel(self.budynki_frame, text="BUDYNKI", font=self.FONT)
        self.budynki_frame_label.pack()

        self.budynki_left_frame = ctk.CTkFrame(self.budynki_frame)
        self.budynki_left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

        self.budynki_right_frame = ctk.CTkFrame(self.budynki_frame)
        self.budynki_right_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

        self.kontury_frame = ctk.CTkFrame(self.obiekty_frame)
        self.kontury_frame.configure(width=10, height=40)

        self.kontury_nad_button = ctk.CTkFrame(self.kontury_frame)
        self.kontury_nad_button.pack(side=ctk.TOP, padx=10, pady=10, fill='x')

        self.kontury_frame_label = ctk.CTkLabel(self.kontury_nad_button, text="KONTURY", font=self.FONT)
        self.kontury_frame_label.pack()

        self.kontury_left_frame = ctk.CTkFrame(self.kontury_nad_button)
        self.kontury_left_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

        self.kontury_right_frame = ctk.CTkFrame(self.kontury_nad_button)
        self.kontury_right_frame.pack(side=ctk.LEFT, padx=10, pady=10, fill="both", expand=True)

        self.mainloop()

    def load_gml(self):
        file = filedialog.askopenfilename(title="Wybierz plik GML", filetypes=[("Pliki GML", "*.gml, *.xml"), ("Wszystkie pliki", "*.*")])
        if file:
            dzialki, budynki, kontury = read_gml(file)
            self.canvas.narysowane = {}
            self.canvas.add_objects(dzialki, budynki, kontury)
            self.add_objects(dzialki, budynki, kontury)
            self.add_objects_to_list(dzialki, budynki, kontury)
        else:
            return

    def add_objects_to_list(self, dzialki, budynki, kontury):
        widgets = [self.dzialki_left_frame, self.dzialki_right_frame, self.kontury_left_frame, self.kontury_right_frame, self.budynki_left_frame, self.budynki_right_frame]
        for widget in widgets:
            for w in widget.winfo_children():
                w.destroy()
        
        if dzialki:
            self.dzialki_frame.pack_propagate(True)
            self.dzialki_frame.pack(side=ctk.TOP, padx=10, pady=10, fill='x')
        if budynki:
            self.budynki_frame.pack_propagate(True)
            self.budynki_frame.pack(side=ctk.TOP, padx=10, pady=10, fill='x')
        if kontury:
            self.kontury_frame.pack_propagate(True)
            self.kontury_frame.pack(side=ctk.TOP, padx=10, pady=10, fill='x')

        for i, dzialka in enumerate(dzialki.values()):
            self.canvas.draw_polygon(dzialka)
            dzialka.narysowany = True
            var = ctk.BooleanVar(value=True)
            if (i % 2) == 0:
                checkbox = ctk.CTkCheckBox(self.dzialki_right_frame, text=f"{dzialka.idDzialki}", command=lambda dzialka=dzialka: self.canvas.change_visibility(dzialka), variable=var)
            else:
                checkbox = ctk.CTkCheckBox(self.dzialki_left_frame, text=f"{dzialka.idDzialki}", command=lambda dzialka=dzialka: self.canvas.change_visibility(dzialka), variable=var)
            checkbox.pack(side=ctk.TOP, pady=3, padx=3, anchor=ctk.W)

        for i, kontur in enumerate(kontury):
            var = ctk.BooleanVar(value=False)
            if (i % 2) == 0:
                checkbox = ctk.CTkCheckBox(self.kontury_right_frame, text=f"{kontur.idUzytku}", command=lambda kontur=kontur: self.canvas.change_visibility(kontur), variable=var)
            else:
                checkbox = ctk.CTkCheckBox(self.kontury_left_frame, text=f"{kontur.idUzytku}", command=lambda kontur=kontur: self.canvas.change_visibility(kontur), variable=var)
            checkbox.pack(side=ctk.TOP, pady=3, padx=3, anchor=ctk.W)

        for i, budynek in enumerate(budynki):
            self.canvas.draw_polygon(budynek)
            budynek.narysowany = True
            var = ctk.BooleanVar(value=True)
            if (i % 2) == 0:
                checkbox = ctk.CTkCheckBox(self.budynki_right_frame, text=f"{budynek.idBudynku}", command=lambda budynek=budynek: self.canvas.change_visibility(budynek), variable=var)
            else:
                checkbox = ctk.CTkCheckBox(self.budynki_left_frame, text=f"{budynek.idBudynku}", command=lambda budynek=budynek: self.canvas.change_visibility(budynek), variable=var)
            checkbox.pack(side=ctk.TOP, pady=3, padx=3, anchor=ctk.W)
    
    def add_objects(self, dzialki, budynki, kontury):
        self.dzialki = dzialki
        self.budynki = budynki
        self.kontury = kontury
