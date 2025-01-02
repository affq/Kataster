import numpy as np
import sys

if len(sys.argv) != 2:  
    print("Użycie: python main.py <ścieżka_do_pliku>")
    sys.exit(1)

kontury = sys.argv[1]

data = np.array([])
with open(kontury, mode='r') as file:
    for line in file:
        data = np.append(data, line.strip())

codes = []
i = 0
while (i+2) < len(data):
    code = data[i]
    num_of_lines = int(data[i+2])
    codes.append(code)
    i += num_of_lines + 4

possible_ofus = set(['B', 'Ba', 'Bi', 'Bp', 'Bz', 'K', 'dr', 'Tk', 'Ti', 'Tp', 'Wm', 'Wp', 'Ws', 'Tr', 'Ls', 'Lz', 'N', 'S', 'Br', 'Wsr', 'W', 'Lzr', 'R', 'Ps', 'Ł'])
unclassified = set(['B', 'Ba', 'Bi', 'Bp', 'Bz', 'K', 'dr', 'Tk', 'Ti', 'Tp', 'Wm', 'Wp', 'Ws', 'Tr', 'N'])
r_classes = set(['I', 'II', 'IIIa', 'IIIb', 'IVa', 'IVb', 'V', 'VI', 'VIz'])
lpslslz_classes = set(['I', 'II', 'III', 'IV', 'V', 'VI'])

errors = []

def add_error(code, error_code, errors_array = errors):
    errors_array.append({'code': code, 'error_code': error_code})

def check_obreb(code, dash):
    for char in code[:dash]:
        if not char.isdigit():
            add_error(code, 'ERR03')
            return 1

def check_dzialka(code, dash, slash):
    for char in code[dash+1:slash]:
        if not char.isdigit():
            add_error(code, 'ERR04')
            return 1

def check_ofu(code, slash_index):
    if code[slash_index+1:slash_index+4] in possible_ofus:
        return code[slash_index+1:slash_index+4]
    elif code[slash_index+1:slash_index+3] in possible_ofus:
        return code[slash_index+1:slash_index+3]
    elif code[slash_index+1:slash_index+2] in possible_ofus:
        return code[slash_index+1:slash_index+2]
    else:
        return None

def check_r(code, next_index):
    if code[next_index:] in r_classes:
        return code[next_index:]
    add_error(code, 'ERR09')
    return 1

def check_lpslslz(code, next_index):
    if code[next_index:] in lpslslz_classes:
        return code[next_index:]
    add_error(code, 'ERR09')
    return 1

def check_sbrwsrwlzr(code, next_index, uzytek_type):
    chars_left = len(code) - next_index
    if chars_left < 2:
        add_error(code, 'ERR12')
        return 1
    elif code[next_index:next_index + 1] != '-':
        add_error(code, 'ERR10')
        return 1
    elif code[next_index + 1: next_index + 3] == 'Ps':
        if len(code) > next_index + 3:
            if code[next_index + 3:] not in lpslslz_classes:
                add_error(code, 'ERR09')
                return 1
        else:
            add_error(code, 'ERR07')
            return 1
    elif code[next_index + 1: next_index + 2] == 'Ł':
        if len(code) > next_index + 2:
            if code[next_index + 2:] not in lpslslz_classes:
                add_error(code, 'ERR09')
                return 1
        else:
            add_error(code, 'ERR07')
            return 1
    elif code[next_index + 1: next_index + 2] == 'R':
        if len(code) > next_index + 2:
            if code[next_index + 2:] not in r_classes:
                add_error(code, 'ERR09')
                return 1
        else:
            add_error(code, 'ERR07')
            return 1
    elif uzytek_type == 'W' and code[next_index + 1: next_index + 3] in ['Ls', 'Lz']:
        if len(code) > next_index + 3:
            if code[next_index + 3:] not in lpslslz_classes:
                add_error(code, 'ERR09')
                return 1
        else:
            add_error(code, 'ERR07')
            return 1
    else:
        add_error(code, 'ERR11')
        return 1

def check_unclassified(code, next_index):
    if len(code) > next_index:
        add_error(code, 'ERR06')
        return 1

def check_zgodnosc(code, uzytek_type, slash_index):
    next_index = slash_index + len(uzytek_type) + 1
    
    if uzytek_type in unclassified:
        check_unclassified(code, next_index)
    elif uzytek_type == 'R':
        check_r(code, next_index)
    elif uzytek_type in ['Ł', 'Ps', 'Ls', 'Lz']:
        check_lpslslz(code, next_index)
    elif uzytek_type in ['S', 'Br', 'Wsr', 'W', 'Lzr']:
        check_sbrwsrwlzr(code, next_index, uzytek_type)   

error_codes = {
    'ERR01': "Brak dasha.",
    'ERR02': "Brak slasha.",
    'ERR03': 'Niepoprawny numer obrębu.',
    'ERR04': 'Niepoprawny numer działki.',
    'ERR05': 'Nierozpoznany użytek.',
    'ERR06': 'Zbędne OZU i OZK dla nieklasyfikowanego użytku.',
    'ERR07': 'Brak OZK.',
    'ERR09': 'Niedozwolony typ klasyfikacji dla tego użytku.',
    'ERR10': 'Niepoprawny znak łączący między OFU i OZU.',
    'ERR11': 'Niedozwolona kombinacja OFU-OZU.',
    'ERR12': 'Brak OZU i OZK.'
}

for code in codes:
    dash_index = code.find('-')
    slash_index = code.find('/')

    if dash_index == -1:
        add_error(code, 'ERR01')
        continue

    if slash_index == -1:
        add_error(code, 'ERR02')
        continue

    if check_obreb(code, dash_index) == 1:
        continue

    if check_dzialka(code, dash_index, slash_index) == 1:
        continue

    uzytek_type = check_ofu(code, slash_index)
    if uzytek_type is None:
        add_error(code, 'ERR05')
        continue

    check_zgodnosc(code, uzytek_type, slash_index)

for i, error in enumerate(errors):
    print(f"{i+1}.    {error['code']}     {error_codes[error['error_code']]}")

with open ('bledne.txt', 'w') as f:
    for error in errors:
        f.write(error['code'] + '\n')
