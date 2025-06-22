# 🎵 Trilha-Sonora

## 📖 Sobre o Projeto

**Trilha-Sonora** é um aplicativo inovador que revoluciona a experiência de leitura através da geração automática de trilhas sonoras personalizadas e sincronizadas com o conteúdo dos livros. Utilizando inteligência artificial avançada e análise de texto em tempo real, o app cria uma atmosfera sonora única que se adapta ao ritmo, ambiente e emoções de cada página.

## ✨ Funcionalidades Principais

- 📚 **Upload de Livros**: Suporte para múltiplos formatos (PDF, EPUB, MOBI)
- 🧠 **Análise Inteligente**: Detecção automática de sentimentos, ambientes e ritmo narrativo
- 🎵 **Geração Musical Adaptativa**: Combinação de busca no Spotify e geração por IA
- 🔊 **Processamento de Áudio Avançado**: Normalização e efeitos sonoros personalizados
- 🎧 **Reprodução Sincronizada**: Player integrado que acompanha o progresso da leitura
- 📊 **Analytics e Otimização**: Sistema de feedback contínuo para melhorar a experiência

## 🏗️ Arquitetura do Sistema

```mermaid
flowchart TB
    subgraph "📥 INPUT & PRÉ-PROCESSAMENTO"
        A[📚 Upload Livro] -->|PyMuPDF/ebooklib| B[Extração de Texto]
        B -->|spaCy + langdetect| C[Limpeza e Detecção de Idioma]
        C -->|NLTK tokenizer| D[Divisão em Chunks de 3 páginas]
    end
    
    subgraph "🧠 ANÁLISE DE CONTEXTO"
        D -->|BERTimbau/XLM-RoBERTa| E[Análise de Sentimentos]
        D -->|spaCy NER + Custom Model| F[Detecção de Ambiente]
        D -->|Transformers Pipeline| G[Análise de Ritmo/Ação]
        
        E -->|Redis Cache| H[(Cache de Análises)]
        F --> H
        G --> H
    end
    
    subgraph "🎵 GERAÇÃO MUSICAL"
        H -->|FastAPI WebSocket| I{Decisão de Geração}
        
        I -->|Busca Rápida| J[Spotify API + Audio Features]
        I -->|Geração IA| K[MusicGen/Stable Audio]
        
        J -->|spotipy + asyncio| L[Busca por Mood/Energia]
        K -->|audiocraft + GPU| M[Geração com Prompt]
        
        L --> N[Fila de Músicas]
        M --> N
    end
    
    subgraph "🔊 PROCESSAMENTO DE ÁUDIO"
        N -->|librosa + pydub| O[Normalização de Áudio]
        O -->|pedalboard| P[Aplicar Efeitos/Transições]
        P -->|MinIO/S3| Q[(Armazenamento de Cache)]
    end
    
    subgraph "🎧 REPRODUÇÃO SINCRONIZADA"
        Q -->|Howler.js + WebSocket| R[Player no Frontend]
        R -->|React Query + Zustand| S[Sincronização com Leitura]
        S -->|Framer Motion| T[UI Reativa]
    end
    
    subgraph "📊 FEEDBACK & OTIMIZAÇÃO"
        T -->|PostHog/Mixpanel| U[Analytics de Uso]
        U -->|PostgreSQL + TimescaleDB| V[(Banco de Dados)]
        V -->|Celery + Redis| W[Reprocessamento Assíncrono]
        W --> I
    end
```

## 🛠️ Tecnologias Utilizadas

### Backend
- **FastAPI**: Framework web moderno e rápido para APIs
- **Python 3.9+**: Linguagem principal do projeto
- **PostgreSQL + TimescaleDB**: Banco de dados principal e analytics
- **Redis**: Cache e message broker
- **Celery**: Processamento assíncrono de tarefas

### Inteligência Artificial e ML
- **BERTimbau/XLM-RoBERTa**: Análise de sentimentos multilíngue
- **spaCy**: Processamento de linguagem natural e NER
- **NLTK**: Tokenização e análise de texto
- **Transformers (Hugging Face)**: Pipeline de análise de contexto
- **MusicGen/Stable Audio**: Geração musical por IA
- **audiocraft**: Processamento de áudio com GPU

### Processamento de Texto e Áudio
- **PyMuPDF/ebooklib**: Extração de texto de livros
- **langdetect**: Detecção automática de idiomas
- **librosa + pydub**: Análise e manipulação de áudio
- **pedalboard**: Aplicação de efeitos sonoros

### Frontend
- **React**: Framework de interface de usuário
- **TypeScript**: Tipagem estática para JavaScript
- **Zustand**: Gerenciamento de estado
- **React Query**: Cache e sincronização de dados
- **Framer Motion**: Animações fluidas
- **Howler.js**: Player de áudio avançado

### Integração e Storage
- **Spotify API (spotipy)**: Busca e análise de músicas
- **MinIO/S3**: Armazenamento de arquivos de áudio
- **WebSocket**: Comunicação em tempo real
- **PostHog/Mixpanel**: Analytics e tracking de usuário

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.9+
- Node.js 16+
- PostgreSQL 14+
- Redis 6+
- GPU CUDA (opcional, para geração musical por IA)

### Configuração do Ambiente

1. **Clone o repositório**:
```bash
git clone https://github.com/seu-usuario/trilha-sonora.git
cd trilha-sonora
```

2. **Configure o backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente**:
```bash
cp .env.example .env
# Edite o arquivo .env com suas configurações
```

4. **Execute as migrações do banco**:
```bash
alembic upgrade head
```

5. **Inicie o backend**:
```bash
uvicorn main:app --reload
```

6. **Configure o frontend**:
```bash
cd frontend
npm install
npm run dev
```

### Variáveis de Ambiente Necessárias

```env
# Banco de Dados
DATABASE_URL=postgresql://user:password@localhost/trilha_sonora
REDIS_URL=redis://localhost:6379

# APIs Externas
SPOTIFY_CLIENT_ID=seu_client_id
SPOTIFY_CLIENT_SECRET=seu_client_secret
HUGGINGFACE_API_KEY=seu_token_hf

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Analytics
POSTHOG_API_KEY=seu_posthog_key
```

## 📁 Estrutura do Projeto

```
trilha-sonora/
├── backend/
│   ├── app/
│   │   ├── api/              # Endpoints da API
│   │   │   ├── sentiment/        # Análise de sentimentos
│   │   │   ├── music_gen/        # Geração musical
│   │   │   └── audio_processing/ # Processamento de áudio
│   │   ├── core/             # Configurações e segurança
│   │   ├── models/           # Modelos do banco de dados
│   │   └── utils/            # Utilitários
│   ├── ml/
│   │   ├── sentiment/        # Análise de sentimentos
│   │   ├── music_gen/        # Geração musical
│   │   └── audio_processing/ # Processamento de áudio
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/       # Componentes React
│   │   │   ├── pages/           # Páginas da aplicação
│   │   │   └── utils/           # Utilitários
│   │   └── stores/          # Estados globais (Zustand)
│   └── package.json
├── docker-compose.yml        # Configuração para desenvolvimento
└── README.md
```

## 🎯 Roadmap

### Versão 1.0 (MVP)
- [x] Upload e processamento básico de livros
- [x] Análise de sentimentos simples
- [x] Integração com Spotify API
- [x] Player básico sincronizado

### Versão 1.1
- [ ] Geração musical por IA
- [ ] Análise avançada de ambiente e ritmo
- [ ] Efeitos sonoros personalizados
- [ ] Interface mobile responsiva

### Versão 2.0
- [ ] Suporte para audiolivros
- [ ] Compartilhamento social de trilhas
- [ ] Recomendações personalizadas
- [ ] API pública para desenvolvedores

## 🤝 Contribuindo

Adoramos receber contribuições! Veja como você pode ajudar:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvedor Principal* - [@seu-usuario](https://github.com/seu-usuario)

## 🙏 Agradecimentos

- Comunidade open source pelas bibliotecas incríveis
- Pesquisadores em ML/AI por tornarem possível a análise de texto avançada
- Spotify pela API aberta que permite busca musical
- Todos os beta testers que ajudaram a moldar o produto

---

*"A música é a trilha sonora da vida. Agora, também é a trilha sonora da sua leitura."*