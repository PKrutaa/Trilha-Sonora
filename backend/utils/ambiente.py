# Exemplo com transformers
from transformers import pipeline
import requests
import json
import re
from typing import Dict, List, Optional

classifier = pipeline("text-classification", 
                     model="neuralmind/bert-base-portuguese-cased")

texto = "O jardim estava repleto de flores coloridas..."
resultado = classifier(texto)
print(resultado)

class DetectorAmbienteLocal:
    """
    Detector de ambiente usando DeepSeek SLM rodando localmente via Ollama
    """
    
    def __init__(self, modelo: str = "deepseek-r1:1.5b", ollama_url: str = "http://localhost:11434"):
        """
        Inicializa o detector local
        
        Args:
            modelo: Modelo DeepSeek a ser usado
            ollama_url: URL do Ollama local
        """
        self.modelo = modelo
        self.ollama_url = ollama_url
        
        # Tipos de ambiente que podemos detectar
        self.tipos_ambiente = {
            "nao_ambiente": "não descreve ambiente",
            "jardim": "jardim ou área verde",
            "domestico": "ambiente interno doméstico",
            "natural": "paisagem natural",
            "urbano": "ambiente urbano", 
            "trabalho": "ambiente de trabalho",
            "rural": "ambiente rural",
            "aquatico": "ambiente aquático"
        }
        
        # Palavras-chave para fallback heurístico
        self.palavras_chave = {
            "jardim": ["jardim", "flores", "árvores", "plantas", "verde", "parque", "gramado", "canteiro"],
            "domestico": ["casa", "sala", "cozinha", "quarto", "sofá", "mesa", "cama", "banheiro"],
            "natural": ["floresta", "montanha", "rio", "natureza", "selvagem", "mato", "campo aberto"],
            "urbano": ["cidade", "rua", "prédio", "urbano", "construção", "avenida", "calçada"],
            "trabalho": ["escritório", "trabalho", "empresa", "fábrica", "loja", "hospital"],
            "rural": ["fazenda", "campo", "rural", "agricultura", "plantação", "sítio"],
            "aquatico": ["água", "mar", "lago", "rio", "piscina", "praia", "córrego"]
        }
    
    def verificar_ollama(self) -> bool:
        """Verifica se Ollama está rodando"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            return response.status_code == 200
        except:
            return False
    
    def verificar_modelo(self) -> bool:
        """Verifica se o modelo está disponível"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags")
            if response.status_code == 200:
                modelos = response.json()
                nomes_modelos = [m['name'] for m in modelos.get('models', [])]
                return self.modelo in nomes_modelos
            return False
        except:
            return False
    
    def _criar_prompt(self, texto: str) -> str:
        """Cria prompt otimizado para DeepSeek"""
        return f"""Analise este texto e determine se descreve o ambiente de um local:

TEXTO: "{texto}"

TAREFA: Classifique em uma destas categorias:
1. não descreve ambiente - texto não menciona cenário/local
2. jardim ou área verde - jardins, parques, plantas
3. ambiente interno doméstico - casa, sala, cozinha, quarto  
4. paisagem natural - floresta, montanha, campo, natureza
5. ambiente urbano - cidade, rua, prédios, construções
6. ambiente de trabalho - escritório, fábrica, loja
7. ambiente rural - fazenda, sítio, agricultura
8. ambiente aquático - rio, lago, mar, piscina

RESPOSTA (apenas JSON):
{{"categoria": "nome_da_categoria", "confianca": 0.9, "elementos": ["elemento1", "elemento2"]}}"""

    def analisar_com_deepseek(self, texto: str) -> Dict:
        """Analisa texto usando DeepSeek via Ollama"""
        
        # Verifica se Ollama está rodando
        if not self.verificar_ollama():
            return self._resultado_erro(texto, "Ollama não está rodando")
        
        # Verifica se modelo está disponível
        if not self.verificar_modelo():
            return self._resultado_erro(texto, f"Modelo {self.modelo} não encontrado")
        
        url = f"{self.ollama_url}/api/generate"
        
        payload = {
            "model": self.modelo,
            "prompt": self._criar_prompt(texto),
            "stream": False,
            "options": {
                "temperature": 0.1,
                "top_p": 0.9,
                "num_predict": 150
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=30)
            response.raise_for_status()
            
            resultado = response.json()
            resposta_modelo = resultado.get('response', '')
            
            return self._processar_resposta(texto, resposta_modelo)
            
        except Exception as e:
            return self._resultado_erro(texto, f"Erro na requisição: {str(e)}")
    
    def _processar_resposta(self, texto: str, resposta: str) -> Dict:
        """Processa a resposta do modelo"""
        
        # Tenta extrair JSON da resposta
        try:
            # Procura por JSON na resposta
            json_match = re.search(r'\{.*\}', resposta, re.DOTALL)
            if json_match:
                json_data = json.loads(json_match.group())
                categoria = json_data.get("categoria", "").lower()
                confianca = float(json_data.get("confianca", 0.5))
                elementos = json_data.get("elementos", [])
                
                return {
                    "texto": texto,
                    "descreve_ambiente": categoria != "não descreve ambiente",
                    "tipo_ambiente": categoria,
                    "confianca": confianca,
                    "elementos_identificados": elementos,
                    "metodo": "deepseek_local",
                    "resposta_completa": resposta
                }
        except:
            pass
        
        # Fallback: análise heurística
        return self._analise_heuristica(texto, resposta)
    
    def _analise_heuristica(self, texto: str, resposta: str) -> Dict:
        """Análise heurística quando o JSON falha"""
        
        texto_lower = texto.lower()
        resposta_lower = resposta.lower()
        
        melhor_categoria = "não descreve ambiente"
        melhor_score = 0
        elementos_encontrados = []
        
        for categoria, palavras in self.palavras_chave.items():
            # Conta palavras-chave no texto original
            score_texto = sum(1 for palavra in palavras if palavra in texto_lower)
            # Conta palavras-chave na resposta do modelo
            score_resposta = sum(0.5 for palavra in palavras if palavra in resposta_lower)
            
            score_total = score_texto + score_resposta
            
            if score_total > melhor_score:
                melhor_score = score_total
                melhor_categoria = categoria
                elementos_encontrados = [p for p in palavras if p in texto_lower]
        
        confianca = min(0.9, melhor_score * 0.15)
        
        return {
            "texto": texto,
            "descreve_ambiente": melhor_categoria != "não descreve ambiente",
            "tipo_ambiente": melhor_categoria,
            "confianca": confianca,
            "elementos_identificados": elementos_encontrados,
            "metodo": "heuristica",
            "resposta_completa": resposta
        }
    
    def _resultado_erro(self, texto: str, erro: str) -> Dict:
        """Retorna resultado de erro"""
        return {
            "texto": texto,
            "descreve_ambiente": False,
            "tipo_ambiente": "erro",
            "confianca": 0.0,
            "elementos_identificados": [],
            "erro": erro,
            "metodo": "erro"
        }
    
    def analisar(self, texto: str) -> Dict:
        """
        Método principal para análise de ambiente
        
        Args:
            texto: Texto para analisar
            
        Returns:
            Dict com resultado da análise
        """
        if not texto or not texto.strip():
            return self._resultado_erro(texto, "Texto vazio")
        
        return self.analisar_com_deepseek(texto.strip())
    
    def analisar_multiplos(self, textos: List[str]) -> List[Dict]:
        """Analisa múltiplos textos"""
        return [self.analisar(texto) for texto in textos]

# Função helper para uso direto
def detectar_ambiente(texto: str, modelo: str = "deepseek-r1:1.5b") -> Dict:
    """
    Função helper para detectar ambiente rapidamente
    
    Args:
        texto: Texto para analisar
        modelo: Modelo DeepSeek a usar
        
    Returns:
        Dict com resultado da análise
    """
    detector = DetectorAmbienteLocal(modelo=modelo)
    return detector.analisar(texto)

# Testes
if __name__ == "__main__":
    print("=== Detector de Ambiente Local com DeepSeek ===\n")
    
    # Inicializa detector
    detector = DetectorAmbienteLocal()
    
    # Verifica se tudo está funcionando
    print("🔧 Verificando Ollama...")
    if detector.verificar_ollama():
        print("✅ Ollama está rodando")
    else:
        print("❌ Ollama não está rodando. Execute: ollama serve")
        exit(1)
    
    print(f"🔧 Verificando modelo {detector.modelo}...")
    if detector.verificar_modelo():
        print("✅ Modelo encontrado")
    else:
        print(f"❌ Modelo não encontrado. Execute: ollama pull {detector.modelo}")
        exit(1)
    
    # Textos de teste
    textos_teste = [
        "O jardim estava repleto de flores coloridas, com árvores frondosas e um pequeno lago cristalino ao centro.",
        "Ele abriu a porta da cozinha e viu a mesa posta com pratos e copos brilhantes.",
        "A reunião aconteceu no escritório principal da empresa na segunda-feira.",
        "O relatório foi entregue ontem pela manhã conforme solicitado.",
        "As montanhas se estendiam até onde a vista alcançava, cobertas de névoa matinal.",
        "A fazenda tinha um grande celeiro vermelho e campos de milho ondulando no vento."
    ]
    
    print("\n🧪 Testando classificação:\n")
    
    for i, texto in enumerate(textos_teste, 1):
        print(f"Teste {i}:")
        print(f"Texto: {texto}")
        
        resultado = detector.analisar(texto)
        
        if resultado.get("erro"):
            print(f"❌ Erro: {resultado['erro']}")
        else:
            emoji = "✅" if resultado["descreve_ambiente"] else "❌"
            print(f"{emoji} Ambiente: {resultado['tipo_ambiente']}")
            print(f"📊 Confiança: {resultado['confianca']:.2f}")
            if resultado.get("elementos_identificados"):
                print(f"🔍 Elementos: {', '.join(resultado['elementos_identificados'])}")
        
        print("-" * 50)