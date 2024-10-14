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