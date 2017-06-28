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
            for index in range(dist - max_dist, dist + max_dist):
                if index in tmp_root.keys():
                    analize.append(tmp_root[index])
        return ret
   
