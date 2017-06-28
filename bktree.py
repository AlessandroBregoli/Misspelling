import Levenshtein
class BKTree:
    NODE_DATA = "NodeData"
    def __init__(self):
        self.root = {}
    def addWord(self, word):
        tmp_root = self.root
        while True:
            if BKTree.NODE_DATA not in tmp_root.keys():
                tmp_root[BKTree.NODE_DATA] = word
                return
            else:
                dist = Levenshtein.distance(word, tmp_root[BKTree.NODE_DATA])
                if dist == 0:
                    return
                elif dist in tmp_root.keys():
                    tmp_root = tmp_root[dist]
                else:
                    tmp_root[dist] = {BKTree.NODE_DATA: word}
                    return
   
    def search(self, word, max_dist):
        ret = []
        analize = []
        analize.append(self.root)
        while len(analize) > 0:
            tmp_root = analize.pop()
            dist = Levenshtein.distance(word, tmp_root[BKTree.NODE_DATA])
            if dist <= max_dist:
                ret.append(tmp_root[BKTree.NODE_DATA])
            for index in range(dist - max_dist, dist + max_dist + 1):
                if str(index) in tmp_root.keys():
                    analize.append(tmp_root[str(index)])
        return ret
   
#TODO La conversione da json fa shifo:
#Tutti i pesi degli archi rappresentati come chiave nel dizionario durante la conversione passano da interi a stringhe
#quindi per utilizzarli in questa funzione vengono convertiti; tuttavia bisognerebbe aggiostare a monte il problema invece di usare questo trick
    def bounded_search(self, word, max_dist, ret_dim):
        ret = []
        l_ret = []
        worst_word_id = -1
        analize = []
        analize.append(self.root)
        while len(analize) > 0:
            tmp_root = analize.pop()
            dist = Levenshtein.distance(word, tmp_root[BKTree.NODE_DATA])
            if dist <= max_dist:
                if len(ret) < ret_dim:
                    ret.append(tmp_root[BKTree.NODE_DATA])
                    l_ret.append(dist)
                elif l_ret[worst_word_id] > dist:
                    ret[worst_word_id] = tmp_root[BKTree.NODE_DATA]
                    l_ret[worst_word_id] = dist
                max_dist = max(l_ret)
                worst_word_id = l_ret.index(max_dist)
            
            for index in range(dist - max_dist, dist + max_dist + 1):
                if str(index) in tmp_root.keys():
                    analize.append(tmp_root[str(index)])
        return ret