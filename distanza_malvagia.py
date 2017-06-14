import numpy
def distanza_malvagia(s1, s2, m_err):
    """
        S1 è evidenza
    """
    mat = numpy.zeros((len(s2)+1,len(s1)+1), dtype="float")
    mat[0][0] = m_err.azzecca
    for i in range(len(s1)+1):
        mat[0][i] = m_err.p_inserzione ** i
        print("1")
    for j in range(len(s2)+1):
        mat[j][0] = m_err.p_omissione ** j
        print("2")
    for j in range(1,len(s2)+1):
        for i in range(1, len(s1)+1):
            if s1[i-1] == s2[j-1]:
                mat[j][i] = mat[j-1][i-1] * m_err.azzecca
            else:
                inserz = mat[j-1][i] * m_err.p_inserzione
                omiss = mat[j][i-1] * m_err.p_omissione
                sostit = mat[j-1][i-1] * m_err.probs[s2[j-1]][s1[i-1]]
                mat[j][i] = max(inserz, omiss, sostit)
    return mat[len(s2),len(s1)]
import adiacenti
asd = adiacenti.ModelloErrore()
asd.calcola_adiacenze()