"""
Módulo de Análise de Emoções Multilíngue Granular
Parte do sistema Trilha-Sonora para análise de contexto emocional de textos literários
"""

import os
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalisadorEmocoesMultilingue:
    """
    Analisador de emoções granulares multilíngue
    Suporta português, inglês, espanhol e mais 20+ idiomas
    """
    
    def __init__(self, modelo_principal: str = "tabularisai/multilingual-sentiment-analysis"):
        """
        Inicializa o analisador com diferentes modelos dependendo da necessidade
        
        Args:
            modelo_principal: Modelo base para análise multilíngue
        """
        self.modelos_disponiveis = {
            # Modelo principal - Multilíngue com sentimentos granulares
            "multilingual_sentiment": "tabularisai/multilingual-sentiment-analysis",
            
            # Modelo específico para português (GoEmotions traduzido)
            "portuguese_emotions": "Luzo0/GoEmotions_portuguese",
            
            # Modelo GoEmotions original (inglês) - 27 emoções
            "goemotions_original": "monologg/bert-base-cased-goemotions-original",
            
            # Backup multilíngue
            "xlm_emotions": "j-hartmann/emotion-english-distilroberta-base",
        }
        
        # Mapeamento de emoções para trilhas sonoras
        self.emocao_trilha_mapping = {
            # Sentimentos básicos -> Trilhas
            'very positive': {'trilha': 'alegre', 'energia': 0.9, 'valencia': 0.9},
            'positive': {'trilha': 'otimista', 'energia': 0.7, 'valencia': 0.7},
            'neutral': {'trilha': 'ambiente', 'energia': 0.5, 'valencia': 0.5},
            'negative': {'trilha': 'melancólica', 'energia': 0.3, 'valencia': 0.3},
            'very negative': {'trilha': 'sombria', 'energia': 0.1, 'valencia': 0.1},
            
            # GoEmotions granulares -> Trilhas específicas
            'joy': {'trilha': 'alegre', 'energia': 0.8, 'valencia': 0.8},
            'love': {'trilha': 'romântica', 'energia': 0.6, 'valencia': 0.9},
            'sadness': {'trilha': 'melancólica', 'energia': 0.2, 'valencia': 0.2},
            'anger': {'trilha': 'intensa', 'energia': 0.9, 'valencia': 0.1},
            'fear': {'trilha': 'suspense', 'energia': 0.7, 'valencia': 0.2},
            'surprise': {'trilha': 'dramática', 'energia': 0.8, 'valencia': 0.6},
            'disgust': {'trilha': 'sombria', 'energia': 0.4, 'valencia': 0.1},
            'excitement': {'trilha': 'energética', 'energia': 0.9, 'valencia': 0.8},
            'admiration': {'trilha': 'inspiradora', 'energia': 0.6, 'valencia': 0.8},
            'curiosity': {'trilha': 'misteriosa', 'energia': 0.7, 'valencia': 0.6},
            'confusion': {'trilha': 'incerta', 'energia': 0.4, 'valencia': 0.4},
            'nervousness': {'trilha': 'tensa', 'energia': 0.6, 'valencia': 0.3},
            'pride': {'trilha': 'épica', 'energia': 0.8, 'valencia': 0.8},
            'embarrassment': {'trilha': 'suave', 'energia': 0.3, 'valencia': 0.4},
            'disappointment': {'trilha': 'triste', 'energia': 0.2, 'valencia': 0.2},
            'relief': {'trilha': 'calma', 'energia': 0.4, 'valencia': 0.7},
            'gratitude': {'trilha': 'harmoniosa', 'energia': 0.5, 'valencia': 0.8},
            'grief': {'trilha': 'lamentosa', 'energia': 0.2, 'valencia': 0.1},
            'desire': {'trilha': 'sedutora', 'energia': 0.7, 'valencia': 0.7},
            'optimism': {'trilha': 'esperançosa', 'energia': 0.7, 'valencia': 0.8},
            'annoyance': {'trilha': 'irritante', 'energia': 0.6, 'valencia': 0.2},
            'remorse': {'trilha': 'arrependida', 'energia': 0.3, 'valencia': 0.2},
            'disapproval': {'trilha': 'desaprovadora', 'energia': 0.5, 'valencia': 0.3},
            'amusement': {'trilha': 'divertida', 'energia': 0.8, 'valencia': 0.8},
            'caring': {'trilha': 'carinhosa', 'energia': 0.5, 'valencia': 0.8},
        }
        
        # Inicializar modelo principal
        try:
            logger.info(f"Carregando modelo multilíngue: {modelo_principal}")
            self.pipeline_principal = pipeline(
                "text-classification", 
                model=modelo_principal,
                return_all_scores=True
            )
            logger.info("Modelo multilíngue carregado com sucesso!")
        except Exception as e:
            logger.error(f"Erro ao carregar modelo principal: {e}")
            # Fallback para modelo básico
            self.pipeline_principal = pipeline(
                "text-classification",
                model="cardiffnlp/twitter-xlm-roberta-base-sentiment",
                return_all_scores=True
            )
    
    def analisar_emocoes(self, texto: str, threshold: float = 0.1) -> Dict:
        """
        Analisa emoções granulares em texto multilíngue
        
        Args:
            texto: Texto para análise
            threshold: Limite mínimo de confiança para incluir emoção
            
        Returns:
            Dicionário com emoções detectadas e metadados
        """
        try:
            # Análise principal
            resultados = self.pipeline_principal(texto)
            
            # Processar resultados
            emocoes_detectadas = {}
            for resultado in resultados[0]:  # Pipeline retorna lista de listas
                label = resultado['label'].lower()
                score = resultado['score']
                
                if score >= threshold:
                    emocoes_detectadas[label] = {
                        'score': float(score),
                        'trilha_info': self.emocao_trilha_mapping.get(
                            label, 
                            {'trilha': 'ambiente', 'energia': 0.5, 'valencia': 0.5}
                        )
                    }
            
            # Encontrar emoção dominante
            emocao_dominante = max(emocoes_detectadas.items(), key=lambda x: x[1]['score'])
            
            return {
                'texto_analisado': texto,
                'emocoes_detectadas': emocoes_detectadas,
                'emocao_dominante': {
                    'emocao': emocao_dominante[0],
                    'confianca': emocao_dominante[1]['score'],
                    'trilha_recomendada': emocao_dominante[1]['trilha_info']['trilha'],
                    'energia': emocao_dominante[1]['trilha_info']['energia'],
                    'valencia': emocao_dominante[1]['trilha_info']['valencia']
                },
                'total_emocoes': len(emocoes_detectadas),
                'modelo_usado': 'multilingual_sentiment'
            }
            
        except Exception as e:
            logger.error(f"Erro na análise de emoções: {e}")
            return {
                'erro': str(e),
                'texto_analisado': texto,
                'emocao_dominante': {
                    'emocao': 'neutral',
                    'confianca': 0.5,
                    'trilha_recomendada': 'ambiente',
                    'energia': 0.5,
                    'valencia': 0.5
                }
            }
    
    def analisar_capitulo(self, texto_capitulo: str, chunks: List[str] = None) -> Dict:
        """
        Analisa um capítulo inteiro dividindo em chunks ou usando texto completo
        
        Args:
            texto_capitulo: Texto completo do capítulo
            chunks: Lista de chunks já divididos (opcional)
            
        Returns:
            Análise agregada do capítulo
        """
        if not chunks:
            # Dividir em chunks de ~500 palavras
            palavras = texto_capitulo.split()
            chunk_size = 500
            chunks = [
                ' '.join(palavras[i:i + chunk_size]) 
                for i in range(0, len(palavras), chunk_size)
            ]
        
        analises_chunks = []
        emocoes_agregadas = {}
        
        for i, chunk in enumerate(chunks):
            if len(chunk.strip()) < 10:  # Skip chunks muito pequenos
                continue
                
            analise = self.analisar_emocoes(chunk)
            analises_chunks.append({
                'chunk_id': i,
                'analise': analise
            })
            
            # Agregar emoções
            if 'emocoes_detectadas' in analise:
                for emocao, info in analise['emocoes_detectadas'].items():
                    if emocao not in emocoes_agregadas:
                        emocoes_agregadas[emocao] = []
                    emocoes_agregadas[emocao].append(info['score'])
        
        # Calcular médias das emoções
        emocoes_medias = {}
        for emocao, scores in emocoes_agregadas.items():
            emocoes_medias[emocao] = {
                'score_medio': np.mean(scores),
                'frequencia': len(scores),
                'max_score': max(scores),
                'trilha_info': self.emocao_trilha_mapping.get(
                    emocao,
                    {'trilha': 'ambiente', 'energia': 0.5, 'valencia': 0.5}
                )
            }
        
        # Emoção dominante no capítulo
        if emocoes_medias:
            emocao_dominante_cap = max(
                emocoes_medias.items(), 
                key=lambda x: x[1]['score_medio'] * x[1]['frequencia']
            )
            
            return {
                'capitulo_resumo': {
                    'total_chunks': len(chunks),
                    'chunks_analisados': len(analises_chunks),
                    'emocao_dominante': {
                        'emocao': emocao_dominante_cap[0],
                        'score_medio': emocao_dominante_cap[1]['score_medio'],
                        'frequencia': emocao_dominante_cap[1]['frequencia'],
                        'trilha_recomendada': emocao_dominante_cap[1]['trilha_info']['trilha'],
                        'energia': emocao_dominante_cap[1]['trilha_info']['energia'],
                        'valencia': emocao_dominante_cap[1]['trilha_info']['valencia']
                    }
                },
                'emocoes_agregadas': emocoes_medias,
                'analises_por_chunk': analises_chunks,
                'recomendacao_trilha': self._gerar_recomendacao_trilha(emocoes_medias)
            }
        else:
            return {'erro': 'Nenhuma emoção detectada no capítulo'}
    
    def _gerar_recomendacao_trilha(self, emocoes_medias: Dict) -> Dict:
        """
        Gera recomendação de trilha baseada nas emoções agregadas
        """
        if not emocoes_medias:
            return {
                'trilha_principal': 'ambiente',
                'energia_geral': 0.5,
                'valencia_geral': 0.5
            }
        
        # Calcular energia e valência média ponderada
        energia_total = 0
        valencia_total = 0
        peso_total = 0
        
        for emocao, info in emocoes_medias.items():
            peso = info['score_medio'] * info['frequencia']
            trilha_info = info['trilha_info']
            
            energia_total += trilha_info['energia'] * peso
            valencia_total += trilha_info['valencia'] * peso
            peso_total += peso
        
        energia_media = energia_total / peso_total if peso_total > 0 else 0.5
        valencia_media = valencia_total / peso_total if peso_total > 0 else 0.5
        
        # Determinar trilha baseada em energia e valência
        if energia_media > 0.7 and valencia_media > 0.7:
            trilha = 'alegre'
        elif energia_media > 0.7 and valencia_media < 0.3:
            trilha = 'intensa'
        elif energia_media < 0.3 and valencia_media < 0.3:
            trilha = 'melancólica'
        elif energia_media < 0.3 and valencia_media > 0.7:
            trilha = 'calma'
        elif valencia_media > 0.6:
            trilha = 'otimista'
        elif valencia_media < 0.4:
            trilha = 'sombria'
        else:
            trilha = 'ambiente'
        
        return {
            'trilha_principal': trilha,
            'energia_geral': round(energia_media, 2),
            'valencia_geral': round(valencia_media, 2),
            'descricao': f"Trilha {trilha} com energia {energia_media:.1f} e valência {valencia_media:.1f}"
        }


# Exemplo de uso
if __name__ == "__main__":
    analisador = AnalisadorEmocoesMultilingue()
    
    # Textos de teste em diferentes idiomas
    textos_teste = [
        "Kurapika está se afogando em um vazio indescritível", # Português
        "I am absolutely thrilled about this amazing discovery!", # Inglês
        "Estoy muy triste por lo que pasó ayer", # Espanhol
        "Je suis vraiment content de te voir", # Francês
    ]
    
    print("=== ANÁLISE DE EMOÇÕES MULTILÍNGUE ===\n")
    
    for texto in textos_teste:
        print(f"📝 Texto: {texto}")
        resultado = analisador.analisar_emocoes(texto)
        
        if 'erro' not in resultado:
            print(f"🎭 Emoção dominante: {resultado['emocao_dominante']['emocao']}")
            print(f"🎵 Trilha recomendada: {resultado['emocao_dominante']['trilha_recomendada']}")
            print(f"⚡ Energia: {resultado['emocao_dominante']['energia']}")
            print(f"😊 Valência: {resultado['emocao_dominante']['valencia']}")
            print(f"🎯 Confiança: {resultado['emocao_dominante']['confianca']:.2f}")
        else:
            print(f"❌ Erro: {resultado['erro']}")
        
        print("-" * 50)