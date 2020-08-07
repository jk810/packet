'''
Ingests original welle_cubesats_original.txt and creates 10000.txt
HAD TO MANUALLY REMOVE ERRONEOUS DECIMAL POINT IN COL 45-52 IN OUTPUT FILE
'''


def checksum(line):
    cksum = 0
    for i in range(68):
        c = line[i]
        # skip character if it is a space, period, +, or letter
        if c == ' ' or c == '.' or c == '+' or c.isalpha():
            continue
        elif c == '-':
            cksum += 1
        else:
            cksum += int(c)
    cksum %= 10
    return cksum


def add_checksum(TLE_path):
    with open(TLE_path, 'r') as fin:
        lines = [line.strip('\n') + f'{checksum(line)}' + '\n' for line in fin]
    lines[-1] = lines[-1].strip('\n')
    with open('10000.txt', 'w') as fout:
        fout.writelines(lines)


TLE_filename = 'welle_cubesats_manifest_v3.txt'

add_checksum(TLE_filename)
