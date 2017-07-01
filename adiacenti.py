
class ModelloErrore:
    p_inserzione = 0.05
    p_omissione = 0.02
    def calcola_adiacenze(self, fname = "tasti_adiacenti.txt", azzecca = 0.92, ditone = 0.5):
        sbagliato =  1 - azzecca - ditone
        self.azzecca = azzecca
        adiacenza = {}
        vere = set()
        false = set()
        with open(fname, "r") as f:
            lines = f.readlines()
            for l in lines:
                l = l[:-1]
                vera = l[0]
                vere.add(vera)
                f = [ l[x] for x in range(1, len(l)) ]
                adiacenza[vera] = f
                false = false.union(set(f))
        
        self.vere = vere
        self.false = false
        self.adiacenza = adiacenza
        self.lontane = { x : false.difference(adiacenza[x] + [x]) for x in vere}
        #print(adiacenza)

        probs = {x: {y: 0 for y in false} for x in vere}
        n_f = len(false)
        for v in vere:
            for f in false:
                #numero adiacenti:
                n_ad = len(adiacenza[v])
                if f in adiacenza[v]:
                    probs[v][f] = ditone / n_ad
                else:
                    probs[v][f] = sbagliato / (n_f - n_ad - 1)
            probs[v][v] = azzecca
        self.probs = probs
