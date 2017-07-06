import freq_analizer
import hyperviterbi
import sys
import os 
import random

def perturba(phrase, p_err, m_err):
    perturbata = ""
    for char in phrase:
        rnd = random.random()
        if rnd < p_err and char != " " and char >= "a" and char <= "z":
            if rnd < p_err * m_err.ditone:
                l = list(m_err.lontane[char])
                perturbata += l[random.randint(0,len(l)-1)]
            else:
                l = list(m_err.adiacenza[char])
                perturbata += l[random.randint(0,len(l)-1)]
        else:
            perturbata += char
    return perturbata

def perturba_word(phrase, p_w_err, p_err, m_err):
    perturbata = ""
    for word in phrase.split():
        if random.random() < p_w_err:
            w2 = ""
            for char in word:
                rnd = random.random()
                if rnd < p_err * m_err.ditone:
                    l = list(m_err.lontane[char])
                    w2 += l[random.randint(0,len(l)-1)]
                elif rnd < p_err:
                    l = list(m_err.adiacenza[char])
                    w2 += l[random.randint(0,len(l)-1)]
                else:
                    w2 += char
            perturbata += w2 + " "
        else:
            perturbata += word + " "
    return perturbata[:-1]



p = freq_analizer.PriorGenerator(1e-20)
p.deserialize("freq_analized.json")


v = hyperviterbi.Hyperviterbi(p, 25)
v.offline = True
v.prior_generator.load_stop_symbols_from_file("stop_symbols.txt")
tot = 0
corrette = 0
non_perturbate_corrette = 0
non_corrette_perturbate = 0
non_perturbate = 0
with open("test_set2.txt") as ts:
    for line in ts.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        line = line.lower()
        line = v.prior_generator.remove_stop_symbols(line)
        perturbata  = perturba(line, 0.03, v.m_err)
        correzione = v.viterbi(perturbata, [])
        words = line.split()
        for i in range(len(words)):
            if words[i] == perturbata.split()[i] and words[i] == correzione[i]:
                non_perturbate += 1
            elif correzione[i] == words[i]:
                corrette += 1
            elif words[i] == perturbata.split()[i]:
                non_perturbate_corrette += 1
            else:
                non_corrette_perturbate += 1
            tot += 1
    cm = [[non_perturbate, non_corrette_perturbate],\
            [non_perturbate_corrette,corrette]]
print(cm)

