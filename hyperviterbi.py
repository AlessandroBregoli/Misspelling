import numpy
import adiacenti
from freq_analizer import PriorGenerator
import Levenshtein

class Hyperviterbi:
    def __init__(self, prior_generator, neighbors):
        self.m_err = adiacenti.ModelloErrore()
        self.m_err.calcola_adiacenze()
        self.prior_generator = prior_generator
        self.neighbors = neighbors

    def find_neighbors(self, word):
        l_words = []
        l_dist = []
        max_dist = 5000 #TODO: mettere un valore sensato tipo max int
        worst_word_id = -1
        for w in self.prior_generator.dictionary:
            dist = Levenshtein.distance(word, w)
            if len(l_words) < self.neighbors:
                l_words.append(w)
                l_dist.append(dist)
            elif max_dist > dist:
                l_words[worst_word_id] = w
                l_dist[worst_word_id] = dist
            max_dist = max(l_dist)
            worst_word_id = l_dist.index(max_dist)
        return l_words
            

    def distanza_malvagia(self, s1, s2):
        """
            S1 è evidenza
        """
        mat = numpy.zeros((len(s2)+1,len(s1)+1), dtype="float")
        mat[0][0] = self.m_err.azzecca
        for i in range(len(s1)+1):
            mat[0][i] = self.m_err.p_inserzione ** i
        for j in range(len(s2)+1):
            mat[j][0] = self.m_err.p_omissione ** j
        for j in range(1,len(s2)+1):
            for i in range(1, len(s1)+1):
                if s1[i-1] == s2[j-1]:
                    mat[j][i] = mat[j-1][i-1] * self.m_err.azzecca
                else:
                    inserz = mat[j-1][i] * self.m_err.p_inserzione
                    omiss = mat[j][i-1] * self.m_err.p_omissione
                    try: 
                        prob_sost = self.m_err.probs[s2[j-1]][s1[i-1]]
                    except KeyError:
                        prob_sost = 0
                    sostit = mat[j-1][i-1] * prob_sost
                    mat[j][i] = max(inserz, omiss, sostit)
        return mat[len(s2),len(s1)]
    
    #This function split the phrase using the space character; can be enanched considering
    #the possibility of multiple words without space or words splitted in two parts
    def pre_viterbi(self, pharase):
        ret = []
        for x in pharase.split():
            ret.append(self.find_neighbors(x))
        return ret
    

    def viterbi(self, phrase):
        data = self.pre_viterbi(phrase)
        splitted_phrase = phrase.split()
        vit_struct = []
        tmp_state = []
       
        for j in range(0,self.neighbors):
            tmp_dict = {}
            tmp_dict["best_pred"] = 0
            tmp_dict["prob"] = self.distanza_malvagia(splitted_phrase[0], data[0][j])
            tmp_state.append(tmp_dict)
        vit_struct.append(tmp_state)

        for i in range(1,len(data)):
            tmp_state = []
            for j in range(self.neighbors):
                tmp_dict = {}
                tmp_dict["best_pred"] = 0
                tmp_dict["prob"] = 0
                for k in range(self.neighbors):
                    prob = vit_struct[i-1][k]["prob"] * \
                        self.prior_generator.get_word_successor(data[i-1][k], data[i][j]) * \
                        self.distanza_malvagia(splitted_phrase[i],data[i][j])
                    if tmp_dict["prob"]  < prob:
                        tmp_dict["prob"] = prob
                        tmp_dict["best_pred"] = k
                tmp_state.append(tmp_dict)
            vit_struct.append(tmp_state)
        ret = ["" for x in range(len(data))]
        tmp_max = 0
        max_pos = -1
        for x in range(0,self.neighbors):
            if tmp_max < vit_struct[-1][x]["prob"]:
                max_pos = x
                tmp_max = vit_struct[-1][x]["prob"]
        for x in range(len(data)-1, -1, -1):
            ret[x] = data[x][max_pos]
            max_pos = vit_struct[x][max_pos]["best_pred"]
        return ret   