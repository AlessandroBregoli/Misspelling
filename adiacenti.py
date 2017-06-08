import numpy as np

import codifica


size = 255
azzecca = 0.9
eps = 0.001

osserv = np.eye(size, dtype=float) * (azzecca - eps) + (np.ones((size, size), dtype=float) * eps)
with open("tasti_adiacenti.txt", "rb") as f:
    lines = f.readlines()
    for l in lines:
        l = codifica.pulisci(l.strip())
        vera = l[0]
        n_adiac = len(l) - 1
        val = azzecca - (azzecca - eps * 255)
        for x in l[1:]:
            osserv[vera][x] = val
print(osserv)