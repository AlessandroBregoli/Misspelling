import freq_analizer
import hyperviterbi
import sys

p = freq_analizer.PriorGenerator(1e-20)
print("Scansione dataset... ", end="")
sys.stdout.flush()
p.load_stop_symbols_from_file("stop_symbols.txt")
p.analize_freq("dataset/lotr1.txt")
p.analize_freq("dataset/lotr2.txt")
p.analize_freq("dataset/lotr3.txt")
p.finalize()
print("ok")
v = hyperviterbi.Hyperviterbi(p, 5)

while True:
    print("> ",end="")
    phrase = input()
    print(v.viterbi(phrase))

