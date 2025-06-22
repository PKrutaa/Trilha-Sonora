import fitz

def processar_pdf_em_chunks(caminho_pdf, tamanho_chunk=3):
    doc = fitz.open(caminho_pdf)
    paginas = [pagina.get_text() for pagina in doc]
    doc.close()

    chunks = [paginas[i:i + tamanho_chunk] for i in range(0, len(paginas), tamanho_chunk)]
    textos_chunks = [" ".join(chunk) for chunk in chunks]

    return textos_chunks
