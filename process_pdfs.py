import os
from PyPDF2 import PdfReader

def process_pdfs(directory="pdfs"):
    """
    Extrai texto de todos os PDFs em um diretório.

    Args:
        directory (str): Caminho para o diretório que contém os PDFs.

    Returns:
        str: Texto extraído de todos os PDFs concatenados.
    """
    all_text = ""
    
    if not os.path.exists(directory):
        print(f"A pasta '{directory}' não existe. Crie a pasta e adicione os PDFs.")
        return all_text

    for filename in os.listdir(directory):
        if filename.endswith(".pdf"):
            pdf_path = os.path.join(directory, filename)
            print(f"Processando arquivo: {filename}")
            try:
                reader = PdfReader(pdf_path)
                for page in reader.pages:
                    text = page.extract_text()
                    if text:  # Verifica se o texto não é None
                        all_text += text
            except Exception as e:
                print(f"Erro ao processar {filename}: {e}")

    return all_text

if __name__ == "__main__":
    text = process_pdfs()
    with open("texto_processado.txt", "w", encoding="utf-8") as f:
        f.write(text)
    print("Texto extraído salvo em 'texto_processado.txt'.")