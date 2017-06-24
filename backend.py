from flask import Flask,request, g
import json
from hyperviterbi import Hyperviterbi
from freq_analizer import PriorGenerator

app = Flask(__name__)

def get_prior_generator():
    priorGenerator = getattr(g,"PriorGenerator",None)
    if priorGenerator in None:
        priorGenerator = g.PriorGenerator = PriorGenerator(1e-20)
        priorGenerator.deserialize("freq_analized.json")
    return priorGenerator


@app.route('/viterbi', method=['POST'])
def viterbi():
    pre_analized = json.load(request.form['mat'])
    phrase = json.load(request.form['phrase'])
    priorGenerator = get_prior_generator()
    v = Hyperviterbi(phrase, 25)
    corrected_phrase = v.viterbi(phrase, pre_analized)
    ret_dic = {"mat":pre_analized,"viterbi":corrected_phrase}
    return json.dump(ret_dic)
    

app.run()