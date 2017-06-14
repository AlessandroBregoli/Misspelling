import numpy
import adiacenti
from freq_analizer import PriorGenerator
import editdistance

class Hyperviterbi:
    def __init__(self,prior_generator, neighbors):
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
            dist = editdistance.eval(word, w)
            if len(tmp_dict) < self.neighbors:
                l_words.append(w)
                l_dist.append(dist)
            elif max_dist > dist:
                l_words.remove(worst_word_id)
                l_dist.remove(worst_word_id)
                l_words.append(w)
                l_dist.append(dist)
            max_dist = max(l_dist)
            worst_word_id = l_dist.index(max_dist)
        return l_words
            

    def distanza_malvagia(s1, s2):
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
    
