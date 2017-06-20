import freq_analizer
import hyperviterbi
import sys
import os 

p = freq_analizer.PriorGenerator(1e-20)
print("Scansione dataset... ", end="")
sys.stdout.flush()
#carico simboli brutti
p.load_stop_symbols_from_file("stop_symbols.txt")
#carico il dataset
for filename in os.listdir("dataset"):
    p.analize_freq("dataset/" + filename)

#normalizza
p.finalize()
print("ok")
#crea correttore
v = hyperviterbi.Hyperviterbi(p, 25)

while True:
    print("> ",end="")
    phrase = input()
    print(v.viterbi(phrase))

