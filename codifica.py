import sys
def cod(stringa):
    return stringa.encode(encoding='iso-8859-1',errors='ignore')

def decod(i_byte):
    return i_byte.decode('iso-8859-1')

def pulisci(i_byte):
    s = bytearray()
    for x in i_byte:
        if bel_carattere(x):
            s += x.to_bytes(1, sys.byteorder)
    return s

def bel_carattere(char): 
    """Restitusice stampabilità carattere"""
    if char % 128 >= 0x20 and char % 128 <= 0x7e:
        return True
    return char == 0xff