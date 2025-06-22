# 🎵 Trilha Sonora - Detector de Ambiente

Sistema para detectar e classificar descrições de ambiente em textos usando Small Language Models (SLM) da DeepSeek rodando localmente.

## 🚀 Características

- **🔒 100% Local**: Executa completamente offline sem envio de dados
- **⚡ SLM Eficiente**: Usa DeepSeek R1 (1.5B parâmetros) via Ollama
- **🎯 Especializado**: Classifica 8 tipos diferentes de ambiente
- **💰 Gratuito**: Sem custos de API
- **🔧 Fácil de usar**: Interface Python simples

## 📋 Tipos de Ambiente Detectados

1. **Jardim/Área Verde**: jardins, parques, plantas
2. **Ambiente Doméstico**: casa, sala, cozinha, quarto
3. **Paisagem Natural**: floresta, montanha, campo
4. **Ambiente Urbano**: cidade, rua, prédios
5. **Ambiente de Trabalho**: escritório, fábrica, loja
6. **Ambiente Rural**: fazenda, sítio, agricultura
7. **Ambiente Aquático**: rio, lago, mar, piscina
8. **Não descreve ambiente**: textos sem descrição de local

## 🛠️ Instalação

### Pré-requisitos

- Python 3.8+
- Git

### 1. Clonar o repositório

```bash
git clone https://github.com/seu-usuario/trilha-sonora.git
cd trilha-sonora
```

### 2. Criar ambiente virtual

```bash
# Linux/macOS
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependências Python

```bash
# Instalar dependências principais
pip install -r requirements.txt

# OU usando o pyproject.toml
pip install -e ./backend

# Para desenvolvimento (opcional)
pip install -e "./backend[dev]"
```

### 4. Instalar e configurar Ollama

#### Linux/macOS:
```bash
curl -fsSL https://ollama.com/install.sh | sh
```

#### Windows:
1. Baixe o instalador: https://ollama.com/download
2. Execute o instalador
3. Abra um novo terminal

### 5. Iniciar Ollama

```bash
ollama serve
```

### 6. Baixar modelo DeepSeek

```bash
# Modelo recomendado (1.5B parâmetros)
ollama pull deepseek-r1:1.5b

# Modelos alternativos (maiores, mais precisos)
# ollama pull deepseek-r1:7b
# ollama pull deepseek-r1:14b
```

## 🔥 Uso Rápido

### Teste básico

```bash
cd backend
python utils/ambiente.py
```

### Usar no seu código

```python
from backend.utils.ambiente import DetectorAmbienteLocal

# Inicializar detector
detector = DetectorAmbienteLocal()

# Analisar texto
resultado = detector.analisar("O jardim estava cheio de flores coloridas")

# Verificar resultado
if resultado["descreve_ambiente"]:
    print(f"Ambiente: {resultado['tipo_ambiente']}")
    print(f"Confiança: {resultado['confianca']:.2f}")
    print(f"Elementos: {resultado['elementos_identificados']}")
```

### Função helper

```python
from backend.utils.ambiente import detectar_ambiente

# Uso direto
resultado = detectar_ambiente("A cozinha estava bem organizada")
print(resultado)
```

## 📖 Exemplos

### Exemplo 1: Ambiente Natural
```python
texto = "As montanhas se estendiam até onde a vista alcançava, cobertas de névoa matinal"
resultado = detectar_ambiente(texto)
# Output: {"tipo_ambiente": "paisagem natural", "confianca": 0.95}
```

### Exemplo 2: Ambiente Doméstico
```python
texto = "Ele abriu a porta da cozinha e viu a mesa posta"
resultado = detectar_ambiente(texto)
# Output: {"tipo_ambiente": "ambiente interno doméstico", "confianca": 0.88}
```

### Exemplo 3: Não é ambiente
```python
texto = "O relatório foi entregue ontem pela manhã"
resultado = detectar_ambiente(texto)
# Output: {"tipo_ambiente": "não descreve ambiente", "confianca": 0.92}
```

## 🔧 Configuração Avançada

### Alterar modelo

```python
# Usar modelo maior (mais preciso, mais lento)
detector = DetectorAmbienteLocal(modelo="deepseek-r1:7b")

# Usar URL personalizada do Ollama
detector = DetectorAmbienteLocal(
    modelo="deepseek-r1:1.5b",
    ollama_url="http://192.168.1.100:11434"
)
```

### Análise em lote

```python
textos = [
    "O jardim estava florido",
    "A reunião foi no escritório",
    "O relatório foi aprovado"
]

resultados = detector.analisar_multiplos(textos)
for resultado in resultados:
    print(f"{resultado['tipo_ambiente']}: {resultado['confianca']:.2f}")
```

## 🧪 Executar Testes

```bash
# Testes básicos
cd backend
python utils/ambiente.py

# Testes com pytest (se instalou dependências de dev)
pytest tests/

# Testes com cobertura
pytest --cov=backend tests/
```

## 🐛 Solução de Problemas

### Ollama não está rodando
```bash
# Verificar se está rodando
curl http://localhost:11434/api/tags

# Se não estiver, iniciar
ollama serve
```

### Modelo não encontrado
```bash
# Listar modelos instalados
ollama list

# Instalar modelo necessário
ollama pull deepseek-r1:1.5b
```

### Erro de memória
```bash
# Usar modelo menor
ollama pull deepseek-r1:1.5b

# Ou ajustar configuração do Ollama
export OLLAMA_NUM_PARALLEL=1
export OLLAMA_MAX_LOADED_MODELS=1
```

### Dependências Python
```bash
# Reinstalar dependências
pip install --upgrade -r requirements.txt

# Verificar versão do Python
python --version  # Deve ser 3.8+
```

## 📊 Performance

| Modelo | Parâmetros | RAM necessária | Velocidade | Precisão |
|--------|-----------|----------------|------------|----------|
| deepseek-r1:1.5b | 1.5B | ~2GB | ⚡⚡⚡ | ⭐⭐⭐ |
| deepseek-r1:7b | 7B | ~8GB | ⚡⚡ | ⭐⭐⭐⭐ |
| deepseek-r1:14b | 14B | ~16GB | ⚡ | ⭐⭐⭐⭐⭐ |

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🙏 Agradecimentos

- [DeepSeek](https://www.deepseek.com/) pelos excelentes modelos SLM
- [Ollama](https://ollama.com/) pela ferramenta incrível de execução local
- Comunidade open source pelos modelos e ferramentas

## 📞 Suporte

- 🐛 [Reportar bug](https://github.com/seu-usuario/trilha-sonora/issues)
- 💡 [Sugerir funcionalidade](https://github.com/seu-usuario/trilha-sonora/issues)
- 📧 Email: seu.email@exemplo.com

---

Feito com ❤️ usando DeepSeek SLM e Ollama