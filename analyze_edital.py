from collections import Counter
from flask import Flask, render_template
import os

app = Flask(__name__)

# Lista de palavras-chave do edital (sem tópicos)
edital_terms = [
    "compreensão", "análise", "interpretação de textos", "tipos textuais", "gêneros textuais",
    "funções da linguagem", "figuras de linguagem", "coesão textual", "fonética", "ortografia",
    "pontuação", "acentuação gráfica", "estrutura de palavras", "formação de palavras", 
    "derivação", "composição", "substantivo", "artigo", "adjetivo", "pronome", "numeral",
    "verbo", "advérbio", "preposição", "conjunção", "interjeição", "colocação pronominal",
    "regência nominal", "regência verbal", "crase", "concordância nominal", "concordância verbal",
    "aspectos sintáticos", "aspectos semânticos", "sentido conotativo", "sentido denotativo",
    "análise sintática", "período simples", "período composto", "significação das palavras",
    "sinônimos", "antônimos", "homônimos", "parônimos", "semântica", "pragmática", "textos argumentativos", 
    "textos narrativos", "textos descritivos", "textos expositivos", "textos instrucionais"
]

def analyze_text(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read().lower()
    
    # Contar a ocorrência de palavras-chave
    word_count = Counter(word for word in text.split() if word in edital_terms)
    
    return word_count

@app.route('/analyze/<path:text_file>', methods=['GET'])
def analyze(text_file):
    file_path = os.path.join('uploads', text_file)
    if not os.path.exists(file_path):
        return "Arquivo não encontrado", 404
    
    results = analyze_text(file_path)
    return render_template('resultados.html', results=results)

if __name__ == '__main__':
    app.run(debug=True)