from flask import Flask, request, redirect, url_for, render_template
import subprocess
import os
import uuid

app = Flask(__name__)

# Configuração do diretório de upload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Certifique-se de que o diretório de uploads existe
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_pdfs', methods=['POST'])
def process_pdfs():
    # Verifica se o arquivo foi enviado
    if 'file' not in request.files:
        return 'Nenhum arquivo enviado.', 400

    file = request.files['file']
    if file.filename == '':
        return 'Nenhum arquivo selecionado.', 400

    # Salva o arquivo com um nome único
    unique_filename = str(uuid.uuid4()) + "_" + file.filename
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(file_path)

    # Chama o script de processamento de PDFs
    result = subprocess.run(['python', 'process_pdfs.py'], capture_output=True, text=True)
    
    # Verifica se o processamento foi bem-sucedido
    if result.returncode == 0:
        # Aqui você pode processar o texto extraído e contar as ocorrências, se necessário
        return redirect(url_for('index'))  # Redireciona para a página inicial
    else:
        return render_template('resultados.html', resultados={'erro': 'Erro ao processar PDFs'})

@app.route('/analyze_edital', methods=['POST'])
def analyze_edital():
    # Caminho para o arquivo de texto processado
    text_file_path = "texto_processado.txt"

    # Verifica se o arquivo de texto processado existe
    if not os.path.exists(text_file_path):
        return 'Arquivo de texto processado não encontrado.', 404

    # Chama o script de análise de edital
    result = subprocess.run(['python', 'analyze_edital.py', text_file_path], capture_output=True, text=True)
    
    # Redireciona para resultados.html com os resultados
    return render_template('resultados.html', resultados=result.stdout if result.returncode == 0 else 'Erro ao analisar edital')

if __name__ == '__main__':
    app.run(debug=True)