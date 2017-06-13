import json

class PriorGenerator:
    def __init__(self):
        self.freq = {}
        self.successor = {}
        self.word_successor = {}
        self.dictionary = set()
        self.stopSymbols = []
    
    def load_stop_symbols_from_file(self, path):
        with open(path) as file:
            for x in file.readlines():
                self.stopSymbols.append(x.strip())
    
    def remove_stop_symbols(self, line):
        for x in self.stopSymbols:
            line = line.replace(x, "")
        return line
    
    def analize_freq(self, path):
        with open(path) as file:
            for line in file.readlines():
                line = line[:-1]
                line = self.remove_stop_symbols(line)
                #Solo lettere inglesi?
                line = line.lower()
                
                #Analizzo le frequenze
                for i in range(len(line)):
                    char = line[i]
                    if (char > "z" or char < "a"):
                        continue
                    try:
                        self.freq[char] += 1
                    except:
                        self.freq[char] = 1
                    if i < len(line)-1:
                        try:
                            suc = self.successor[char]
                            try:
                                suc[line[i+1]] += 1
                            except:
                                suc[line[i+1]] = 1
                        except:
                            self.successor[char] = {}
                            self.successor[char][line[i+1]] = 1
                #Se non si lavora solo con l'inglese bisogna considerare anche gli apostrofi e simili
                
                #Analizzo le parole
                line = line.split()
                for word_id in range(len(line)):
                    self.dictionary.add(line[word_id])
                    if word_id < len(line)-1:
                        try:
                            suc = self.word_successor[line[word_id]]
                            try:
                                suc[line[word_id + 1]] += 1
                            except:
                                suc[line[word_id + 1]] = 1
                        except:
                            self.word_successor[line[word_id]] = {}
                            self.word_successor[line[word_id]][line[word_id + 1]] = 1
                        
    
    def finalize(self):
        tot = sum(self.freq.values())
        for key in self.freq.keys():
            self.freq[key] /= tot
            tot2 = sum(self.successor[key].values())
            for key2 in self.successor[key].keys():
                self.successor[key][key2] /= tot2
        for key in self.word_successor.keys():
            tot = sum(self.word_successor[key].values())
            for key2 in self.word_successor[key].keys():
                self.word_successor[key][key2] /= tot
        
    def serialize(self, path):
        tmp_dic = {"Dictionary":list(self.dictionary), "Freq": self.freq, "Successor":self.successor,\
                 "Word_successor": self.word_successor}
        with open(path,"w") as outFile:
            json.dump(tmp_dic,outFile)
