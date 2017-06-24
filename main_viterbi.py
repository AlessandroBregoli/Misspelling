import freq_analizer
import hyperviterbi
import sys
import os 

p = freq_analizer.PriorGenerator(1e-20)
p.deserialize("freq_analized.json")


v = hyperviterbi.Hyperviterbi(p, 25)

while True:
    print("> ",end="")
    phrase = input()
    print(v.viterbi(phrase, []))

