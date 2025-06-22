import fitz

def processar_pdf_em_chunks(caminho_pdf, tamanho_chunk=5):
    doc = fitz.open(caminho_pdf)

    # Agora lê todas as páginas do PDF
    paginas = [doc[i].get_text() for i in range(len(doc))]

    doc.close()

    # Divide as páginas em chunks de 5
    chunks = [paginas[i:i + tamanho_chunk] for i in range(0, len(paginas), tamanho_chunk)]
    textos_chunks = [" ".join(chunk) for chunk in chunks]

    return textos_chunks