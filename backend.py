from flask import Flask,request, g
import json
from hyperviterbi import Hyperviterbi
from freq_analizer import PriorGenerator

app = Flask(__name__)
priorGenerator = None 
def get_prior_generator():
    global priorGenerator
    if priorGenerator is None:
        priorGenerator = PriorGenerator(1e-20)
        priorGenerator.deserialize("freq_analized.json")
        priorGenerator.load_stop_symbols_from_file("stop_symbols.txt")
    return priorGenerator

@app.route('/stop_symbols')
def get_stop_symbols():
     return json.dumps(get_prior_generator().stopSymbols)

@app.route('/viterbi', methods=['POST'])
def viterbi():
    js = request.get_json(force=True)
    pre_analized = js['mat']
    phrase = js['phrase']
    priorGenerator = get_prior_generator()
    v = Hyperviterbi(priorGenerator, 10)
    corrected_phrase = v.viterbi(phrase, pre_analized)
    ret_dic = {"mat":pre_analized,"viterbi":corrected_phrase}
    return json.dumps(ret_dic)

@app.route('/')
def root():
    with open("ui_spastica/index.html", "r") as f:
        return f.read()

app.run()