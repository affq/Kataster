import matplotlib.pyplot as plt


coordinates = [
    (5792575.7, 7469493.44), (5792608.68, 7469497.78),
    (5792648.98, 7469503.08), (5792689.29, 7469508.38),
    (5792729.58, 7469513.68), (5792769.88, 7469518.97),
    (5792810.17, 7469524.28), (5792811.95, 7469516.45),
    (5792794.11, 7469514.1), (5792754.2, 7469508.85),
    (5792709.69, 7469503.0), (5792665.18, 7469497.15),
    (5792620.97, 7469491.32), (5792576.75, 7469485.5),
    (5792575.7, 7469493.44)  # Zamknięcie pętli
]

def draw_dzialke(dzialka):
    plt.plot(dzialka.x, dzialka.y, 'o', color='black')

x, y = zip(*coordinates)

plt.figure(figsize=(8, 8))
plt.plot(x, y, marker='o', label='Obiekt geometrii')
plt.title("Wizualizacja geometrii")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.legend()
plt.axis('equal')  # Zachowanie proporcji
plt.show()