import freq_analizer
import hyperviterbi
import sys

p = freq_analizer.PriorGenerator(1e-20)
print("Scansione dataset... ", end="")
sys.stdout.flush()
#carico simboli brutti
p.load_stop_symbols_from_file("stop_symbols.txt")
#carico il dataset
p.analize_freq("dataset/lotr1.txt")
p.analize_freq("dataset/lotr2.txt")
p.analize_freq("dataset/lotr3.txt")
#normalizza
p.finalize()
print("ok")
#crea correttore
v = hyperviterbi.Hyperviterbi(p, 5)

while True:
    print("> ",end="")
    phrase = input()
    print(v.viterbi(phrase))

