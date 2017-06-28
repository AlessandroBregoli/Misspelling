var ldiv = document.getElementById("log");
function log(str, end){
    if(end == undefined){
        end = "\n";
    }
    var txt = document.createTextNode(str + end);
    ldiv.appendChild(txt);
    ldiv.scrollTop = ldiv.scrollHeight;
}
log("Correttore v 0.0");
var typ = document.getElementById("typing");
var chWidth = document.getElementById("provalarghezza").offsetWidth;
var tt = document.getElementById("tooltip");
var glob_word = "";
var invalida = false;
var timeout = null;
typ.mustSetTimeout = 0;
var txt_edited = function(){
    var cpos = typ.selectionStart;
    typ.value = typ.value.replace(/\s+/g, " ")
    var text = typ.value;
    for (var ss in stop_symbols) {
        try{
            if (text[cpos - 1] == stop_symbols[ss]){
                return;
            }
        } catch(e){}
    }
    var word = "";
    var words = text.split(" ")
    var scanpos = 0;
    var wcount = 0;
    var wstart = 0;
    while (scanpos < cpos) { 
        wstart = scanpos;
        scanpos += words[wcount].length + 1;
        wcount += 1;
    }
    var wnumb = wcount - 1;
    
    word = words[wnumb];
    if (word == "" || word == undefined){
        tt.style.visibility = "hidden";
        return;
    }
    typ.wstart = wstart;
    glob_word = word;
    //log("edit, posizione: " + cpos + ", parola: " + word + ", wstart: " + wstart);
    //pop_tooltip([word, "pota", "non sai scrivere", "studia"], wstart, word);
    var time = 200
    if (!lock) {
        time = 50
        ask(text, word, wnumb, wstart)
    } else {
        invalida = true;
        while (mat.length <= wnumb){
            mat.push([])
        }
        var tmp = mat[wnumb].slice(0,6)
        tmp.push(word)
        pop_tooltip(tmp, wstart, wnumb);
    }
    clearTimeout(timeout)
    if (this == typ){
        typ.mustSetTimeout = 2 //volte
    }
    if(typ.mustSetTimeout > 0){
        timeout = setTimeout(txt_edited, time)
        typ.mustSetTimeout -= 1
    }
    tooltip(this.wstart)
}
typ.addEventListener("input", txt_edited);

typ.addEventListener("scroll", function() {
    tooltip(this.wstart);
})
function tooltip(wstart) {
    tt.style.visibility = "visible";
    if (typ.scrollLeft > 0.1) {
        wstart -= (typ.scrollLeft / chWidth);
    }
    if (wstart < 0)
        wstart = 0;
    tt.style.left = (5 + wstart) + "ch";
}
var sugg = document.getElementById("suggestions");
function pop_tooltip (parole, wstart, wnumb) {
    sugg.innerHTML = "";
    for (var x in parole) {
        var li = document.createElement("a");
        li.setAttribute("href", "#")
        li.innerHTML = parole[x];
        li.setAttribute("tabindex",6);
        add_click_event(li, wstart,  parole[x], wnumb);
        sugg.appendChild(li);
    }
}
function add_click_event(li, wstart, parola, wnumb) {
    li.addEventListener("click", function() {
        subst_word(wstart,  parola, wnumb);
    })
}
function subst_word(wstart, new_word, wnumb) {
    typ.value = typ.value.substring(0, wstart) + new_word + typ.value.substring(wstart + glob_word.length)
    tt.style.visibility = "hidden";
    typ.focus();
    typ.selectionStart  = typ.selectionEnd = wstart + new_word.length;
    mat[wnumb] = [new_word];
}
var mat = [];
var lock = 0;
function max(a,b){
    return a>b?a:b
}
function ask (phrase, word, wnumb, wstart) {
    lock = 1;
    var req = {
        "phrase" : phrase.substring(0, wstart + word.length),
        "mat" : mat.slice(0, max(0, wnumb-1))
    }
    if (req["phrase"] == ""){
    	lock = 0;
    	return;
    }
    var ajax = new XMLHttpRequest()
    ajax.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            // Typical action to be performed when the document is ready
            lock = 0
            var resp = JSON.parse(this.responseText)
            	mat = resp['mat']
                var tmp = resp['mat'][wnumb].slice(0,6)
                tmp.push(word)
                pop_tooltip(tmp, wstart, wnumb)
                tooltip(wstart)
            log(resp['viterbi'].join(" "))
        }
    }
    ajax.open("POST", "/viterbi/" + input_model, true);
    ajax.send(JSON.stringify(req));
}
var stop_symbols = [];
function load_stop_symbols () {
    var ajax = new XMLHttpRequest()
    ajax.open("GET", "/stop_symbols", true)
    ajax.onreadystatechange = function() {
        console.log(this.readyState)
        if (this.readyState == 4 && this.status == 200) {
            stop_symbols = JSON.parse(this.responseText)
            stop_symbols.push(" ")
        }
    }
    ajax.send()
}
load_stop_symbols()
