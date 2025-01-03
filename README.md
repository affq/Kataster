## Projekt 1 - weryfikacja poprawności oznaczeń klasoużytków w pliku
Program sprawdza poprawność oznaczeń klasoużytków w pliku. 
W przypadku błędnego oznaczenia informuje użytkownika o tym, co jest nie tak w oznaczeniu.

---

Wg Rozporządzenia Ministra Rozwoju, Pracy i Technologii z dnia 27 lipca 2021 r. w sprawie ewidencji gruntów i budynków:

> 1. Oznaczenie klasoużytku przyjmuje wartość OFU w przypadku:
>    1. gruntów, które nie podlegają gleboznawczej klasyfikacji gruntów, tj. oznaczonych jako
>użytki gruntowe o OFU = B, Ba, Bi, Bp, Bz, K, dr, Tk, Ti, Tp, Wm, Wp, Ws oraz Tr,
>    2. gruntów rolnych lub gruntów leśnych, które podlegają gleboznawczej klasyfikacji
>gruntów, ale w odniesieniu do których taka klasyfikacja nie została przeprowadzona;
>dotyczy to w szczególności użytków gruntowych o wartości OFU = Ls, Lz, N.
>2. Oznaczenie klasoużytku przyjmuje postać składającą się z dwóch usytuowanych
>kolejno elementów: OZU oraz OZK, jeżeli OFU jest równe OZU.
>3. Oznaczenie klasoużytku przyjmuje postać składającą się z trzech usytuowanych kolejno
>elementów: OFU, OZU oraz OZK, jeżeli OFU jest różne od OZU; element OFU jest
>oddzielony od elementu OZU myślnikiem.

oraz

>Przyjęcie przez OFU wartości: ('R' lub 'S' lub 'Br' lub 'Wsr' lub 'W' lub 'Lzr') i przez OZU
>wartości 'R' powoduje, że OZK może przyjąć jedną z wartości ('I' lub 'II' lub 'IIIa' lub 'IIIb'
>lub 'IVa' lub 'IVb' lub 'V' lub 'VI' lub 'VIz').
>
>Przyjęcie przez OFU wartości: ('Ł' lub 'S' lub 'Br' lub 'Wsr' lub 'W' lub 'Lzr') i przez OZU
>wartości 'Ł' lub przyjęcie przez OFU wartości ('Ps' lub 'S' lub 'Br' lub 'Wsr' lub 'W' lub
>'Lzr') i przez OZU wartości 'Ps' lub przyjęcie przez OFU wartości ('Ls' lub 'W') i przez
>OZU wartości 'Ls' lub przyjęcie przez OFU wartości ('Lz' lub 'W') i przez OZU wartości
>'Lz' powoduje, że OZK może przyjąć jedną z wartości ('I' lub 'II' lub 'III' lub 'IV' lub 'V'
>lub 'VI').

---

W związku z tym oznaczenia klasoużytków mogą przyjmować następujące wartości:
| OZU                                                 | OFU  | OZK | ? |
| --------------------------------------------------- | ---- | --- | --- |
| - | B, Ba, Bi, Bp, Bz, K, dr, Tk, Ti, Tp, Wm, Wp, Ws, Tr | - | OFU |
| - | Ls, Lz, N | - | OFU |
| R | < | I, II, IIIa, IIIb, IVa, IVb, V, VI, VIz | OFU = OZU |
| Ł, Ps, Ls, Lz | < | I, II, III, IV, V, VI | OFU = OZU |
| R | S, Br, Wsr, W, Lzr | I, II, IIIa, IIIb, IVa, IVb, V, VI, VIz | OFU ≠ OZU |
| Ł, Ps | S, Br, Wsr, W, Lzr | I, II, III, IV, V, VI| OFU ≠ OZU |
| Ls, Lz | W | I, II, III, IV, V, VI| OFU ≠ OZU |

---

Budowa oznaczenia:
- dla OFU: [OFU], np. 25-20/B
- dla OFU = OZU: [OFU=OZU][OZK], np. 25-20/RIIIa
- dla OFU ≠ OZU: [OFU]-[OZU][OZK], np. 25-20/Br-RIIIa

---
### Przykład działania programu - wypis błędów w konsoli
![image](https://github.com/user-attachments/assets/819d12c7-a48f-470c-ba48-231666e91e4f)

---
## Projekt 2 - program czytający oraz rysujący działki, budynki oraz użytki z pliku GML

