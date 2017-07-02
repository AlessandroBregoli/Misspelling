import freq_analizer
import hyperviterbi
import sys
import os 

p = freq_analizer.PriorGenerator(1e-20)
p.deserialize("freq_analized.json")
p.load_stop_symbols_from_file("stop_symbols.txt")

v = hyperviterbi.Hyperviterbi(p, 10)

while True:
    print("> ",end="")
    phrase = input()
    print(v.viterbi(phrase, []))

