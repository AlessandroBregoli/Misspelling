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
        mat = numpy.zeros((len(s2) + 1, len(s1) + 1), dtype="float")
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
        #frase minuscola
        phrase = phrase.lower()
        #estraggo parole più vicine del dizionario
        data = self.pre_viterbi(phrase)
        #divido frase in parole
        splitted_phrase = phrase.split()
        vit_struct = [] #conterrà la bella di viterbi
        tmp_state = []  #conterrà la colonna corrente di viterbi
        #la singola cella di viterbi contiene una probabilità
        #e l'indice del predecessore

        #calcolo la prima colonna
        for j in range(0,self.neighbors):
            tmp_dict = {}
            tmp_dict["best_pred"] = 0
            tmp_dict["prob"] = self.distanza_malvagia(splitted_phrase[0], data[0][j])
            tmp_state.append(tmp_dict)
        #aggiungo la prima colonna
        vit_struct.append(tmp_state)
        
        #ciclo sulle colonne da 1 in poi
        for i in range(1, len(data)):
            tmp_state = []
            #ciclo sulle righe della colonna
            for j in range(self.neighbors):
                tmp_dict = {}
                #inizializzo a 0 i campi della cella
                tmp_dict["best_pred"] = 0
                tmp_dict["prob"] = 0
                #ciclo sulle celle della colonna
                for k in range(self.neighbors):
                    #ciclo sulle celle della colonna precedente
                    #per trove il predecessore più probabile
                    prob = vit_struct[i - 1][k]["prob"] * \
                        self.prior_generator.get_word_successor(data[i-1][k], data[i][j]) * \
                        self.distanza_malvagia(splitted_phrase[i], data[i][j])
                    #se è maggiore della probabilità già salvata, la sostituiamo
                    #e impostiamo il predecessore
                    if tmp_dict["prob"] < prob:
                        tmp_dict["prob"] = prob
                        tmp_dict["best_pred"] = k
                tmp_state.append(tmp_dict)
            vit_struct.append(tmp_state)
        #inizializzo l'output con stringhe vuote
        ret = ["" for x in range(len(data))]
        tmp_max = 0
        max_pos = -1
        #trovo stato finale più probabile
        for x in range(0, self.neighbors):
            if tmp_max < vit_struct[-1][x]["prob"]:
                max_pos = x
                tmp_max = vit_struct[-1][x]["prob"]
        #ricostruisco all'indietro
        for x in range(len(data) - 1, -1, -1):
            ret[x] = data[x][max_pos]
            max_pos = vit_struct[x][max_pos]["best_pred"]
        return ret