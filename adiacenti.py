
adiacenza = {}
vere = set()
false = set()
with open("tasti_adiacenti.txt", "r") as f:
    lines = f.readlines()
    for l in lines:
        l = l.strip()
        vera = l[0]
        vere.add(vera)
        f = [ l[x] for x in range(1, len(l)) ]
        adiacenza[vera] = f
        false = false.union(set(f))

#print(adiacenza)

probs = { x: { y: 0 for y in false } for x in vere }

for v in vere:
    for f in false:
        #numero adiacenti:
        n_ad = len(adiacenza[v])
        if f in adiacenza[v]:
            probs[v][f] = 0.1 / n_ad
    probs[v][v] = 0.9
print(probs)
