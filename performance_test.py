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




p = freq_analizer.PriorGenerator(1e-20)
p.deserialize("freq_analized.json")


v = hyperviterbi.Hyperviterbi(p, 25)
v.prior_generator.load_stop_symbols_from_file("stop_symbols.txt")
tot = 0
corrette = 0
with open("test_set.txt") as ts:
    for line in ts.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        line = line.lower()
        line = v.prior_generator.remove_stop_symbols(line)
        perturbata  = perturba(line, 0.1, v.m_err)
        correzione = v.viterbi(perturbata, [])
        words = line.split()
        for i in range(len(words)):
            if correzione[i] == words[i]:
                corrette += 1
            tot += 1
    print("l'accuratezza è: " + str(corrette/tot))


