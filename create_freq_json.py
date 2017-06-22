import freq_analizer
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
p.finalize()
print("ok")

p.serialize("freq_analized.json")