kontury = "kataster\Kontury_eksport_dz.txt"

with open(kontury, mode='r') as file:
    content = file.read()
    print(content)

# 1. Oznaczenie klasoużytku przyjmuje wartość OFU w przypadku: 
# 1) gruntów, które nie podlegają gleboznawczej klasyfikacji gruntów, tj. oznaczonych jako 
# użytki gruntowe o OFU = B, Ba, Bi, Bp, Bz, K, dr, Tk, Ti, Tp, Wm, Wp, Ws oraz Tr, 
# 2)  gruntów  rolnych  lub  gruntów  leśnych,  które  podlegają  gleboznawczej  klasyfikacji 
# gruntów,  ale  w  odniesieniu  do  których  taka  klasyfikacja  nie  została  przeprowadzona; 
# dotyczy to w szczególności użytków gruntowych o wartości OFU = Ls, Lz, N. 
# 2.  Oznaczenie  klasoużytku  przyjmuje  postać  składającą  się  z  dwóch  usytuowanych 
# kolejno elementów: OZU oraz OZK, jeżeli OFU jest równe OZU. 
# 3. Oznaczenie klasoużytku przyjmuje postać składającą się z trzech usytuowanych kolejno 
# elementów:  OFU,  OZU  oraz  OZK,  jeżeli  OFU  jest  różne  od  OZU;  element  OFU  jest  
# oddzielony od elementu OZU myślnikiem. 

# Dla OZU = Ł, Ps, Ls, Lz, OZK przyjmuje jedną z następujących wartości: I, II, III, IV, V, 
# VI. Dla OZU = R, OZK przyjmuje jedną z następujących wartości: I, II, IIIa, IIIb, IVa, 
# IVb, V, VI, VIz.

ofu_nieklasyfikowane = ['B', 'Ba', 'Bi', 'Bp', 'Bz', 'K', 'dr', 'Tk', 'Ti', 'Tp', 'Wm', 'Wp', 'Ws', 'Tr']

ozk_dla_ozu_rownego_r = ['I', 'II', 'IIIa', 'IIIb', 'IVa', 'IVb', 'V', 'VI', 'VIz']
ozk_dla_ozu_rownego_l_ps_ls_lz = ['I', 'II', 'III', 'IV', 'V', 'VI']

# Kontur klasyfikacyjny obejmuje tylko kontury użytków gruntowych o oznaczeniach OFU 
# = R, S, Ł, Ps, Br, Wsr, W, Lzr, Ls, Lz.

# Przyjęcie przez OFU wartości: ('R' lub 'S' lub 'Br' lub 'Wsr' lub 'W' lub 'Lzr') i przez OZU 
# wartości 'R' powoduje, że OZK może przyjąć jedną z wartości ('I' lub 'II' lub 'IIIa' lub 'IIIb' 
# lub 'IVa' lub 'IVb' lub 'V' lub 'VI' lub 'VIz'). 
# Przyjęcie przez OFU wartości: ('Ł' lub 'S' lub 'Br' lub 'Wsr' lub 'W' lub 'Lzr') i przez OZU 
# wartości 'Ł' lub przyjęcie przez OFU wartości ('Ps' lub 'S' lub 'Br' lub 'Wsr' lub 'W' lub 
# 'Lzr') i przez OZU wartości 'Ps' lub przyjęcie przez OFU wartości ('Ls' lub 'W') i przez 
# OZU wartości 'Ls' lub przyjęcie przez OFU wartości ('Lz' lub 'W') i przez OZU wartości 
# 'Lz' powoduje, że OZK może przyjąć jedną z wartości ('I' lub 'II' lub 'III' lub 'IV' lub 'V' 
# lub 'VI').


# [A-Z]{2}[1-9]{1}[A-Z]{1}/[0-9]{8}/[0-9]{1} 