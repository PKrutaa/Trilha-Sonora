from fastapi import FastAPI, UploadFile, File
import shutil
import os
from leitura.pdf_processor import processar_pdf_em_chunks
from nltk.tokenize import RegexpTokenizer

app = FastAPI()

UPLOAD_DIR = "./uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Tokenizador que pega apenas palavras (sem pontuação)
tokenizer = RegexpTokenizer(r'\w+')

@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    # Salva o arquivo PDF
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Processa o PDF e divide em chunks
    textos_chunks = processar_pdf_em_chunks(file_path)

    # Tokeniza todos os chunks com RegexpTokenizer
    if textos_chunks:
        primeiro_chunk = textos_chunks[0]
        tokens = tokenizer.tokenize(primeiro_chunk)
        print("\n==== Primeiro Chunk ====")
        print(f"{len(tokens)} tokens")
        print(tokens)
    else:
        primeiro_chunk = "Nenhum texto encontrado"
        tokens = []

    return {
        "total_chunks": len(textos_chunks),
        "exemplo_chunk": primeiro_chunk,
        "exemplo_tokens": tokens
    }