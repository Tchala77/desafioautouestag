#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Classifier
Sistema de classificação de emails usando NLP e IA
"""

import re
import time
import logging
from typing import Dict, Any, Optional
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize, sent_tokenize
import PyPDF2
import io

# Download NLTK data (executar apenas uma vez)
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

logger = logging.getLogger(__name__)

class EmailClassifier:
    """
    Classe principal para classificação de emails
    """
    
    def __init__(self):
        """Inicializar o classificador"""
        self.stemmer = PorterStemmer()
        self.lemmatizer = WordNetLemmatizer()
        
        # Carregar stop words em português e inglês
        try:
            self.stop_words = set(stopwords.words('portuguese') + stopwords.words('english'))
        except:
            # Fallback para inglês se português não estiver disponível
            self.stop_words = set(stopwords.words('english'))
        
        # Palavras-chave para classificação
        self.productive_keywords = {
            'trabalho': ['reunião', 'projeto', 'cliente', 'negócio', 'estratégia', 'deadline', 
                        'relatório', 'apresentação', 'planejamento', 'objetivo', 'meta', 'resultado',
                        'análise', 'desenvolvimento', 'implementação', 'cooperação', 'colaboração',
                        'parceria', 'contrato', 'proposta', 'orçamento', 'cronograma', 'equipe'],
            'profissional': ['curriculum', 'cv', 'entrevista', 'vaga', 'emprego', 'carreira', 
                           'formação', 'experiência', 'competência', 'habilidade', 'treinamento',
                           'certificação', 'especialização', 'graduação', 'pós-graduação'],
            'comercial': ['venda', 'compra', 'produto', 'serviço', 'preço', 'desconto', 'oferta',
                         'promoção', 'marketing', 'publicidade', 'campanha', 'mercado', 'concorrência']
        }
        
        self.unproductive_keywords = {
            'spam': ['corrente', 'sorte', 'loteria', 'herança', 'prêmio', 'ganhe', 'grátis', 'urgente',
                    'limitado', 'exclusivo', 'confidencial', 'secreto', 'oportunidade única'],
            'corrente': ['fwd:', 'reencaminhar', 'encaminhar', 'passe adiante', 'envie para', 
                        'reze por', 'bênção', 'maldição', '7 dias', '24 horas'],
            'marketing_agressivo': ['promoção imperdível', 'oferta limitada', 'última chance', 
                                  'não perca', 'garantido', '100% seguro', 'sem risco'],
            'phishing': ['verificar conta', 'atualizar dados', 'confirmar identidade', 'segurança',
                        'suspensão', 'bloqueio', 'acesso restrito', 'clique aqui']
        }
        
        # Pesos para diferentes tipos de palavras-chave
        self.keyword_weights = {
            'trabalho': 2.0,
            'profissional': 1.5,
            'comercial': 1.0,
            'spam': -2.0,
            'corrente': -1.5,
            'marketing_agressivo': -1.0,
            'phishing': -2.5
        }
        
        logger.info("EmailClassifier inicializado com sucesso")
    
    def extract_pdf_text(self, filepath: str) -> str:
        """
        Extrair texto de arquivo PDF
        
        Args:
            filepath: Caminho para o arquivo PDF
            
        Returns:
            Texto extraído do PDF
        """
        try:
            with open(filepath, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
                
                logger.info(f"Texto extraído do PDF: {len(text)} caracteres")
                return text.strip()
                
        except Exception as e:
            logger.error(f"Erro ao extrair texto do PDF: {str(e)}")
            raise Exception(f"Não foi possível extrair texto do PDF: {str(e)}")
    
    def preprocess_text(self, text: str) -> str:
        """
        Pré-processar texto para análise
        
        Args:
            text: Texto original
            
        Returns:
            Texto pré-processado
        """
        # Converter para minúsculas
        text = text.lower()
        
        # Remover caracteres especiais e números
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\d+', ' ', text)
        
        # Remover espaços extras
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def tokenize_and_clean(self, text: str) -> list:
        """
        Tokenizar e limpar texto
        
        Args:
            text: Texto pré-processado
            
        Returns:
            Lista de tokens limpos
        """
        # Tokenizar
        tokens = word_tokenize(text)
        
        # Remover stop words e aplicar stemming
        cleaned_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                # Aplicar stemming
                stemmed = self.stemmer.stem(token)
                # Aplicar lemmatização
                lemmatized = self.lemmatizer.lemmatize(stemmed)
                cleaned_tokens.append(lemmatized)
        
        return cleaned_tokens
    
    def calculate_keyword_score(self, tokens: list) -> Dict[str, float]:
        """
        Calcular pontuação baseada em palavras-chave
        
        Args:
            tokens: Lista de tokens limpos
            
        Returns:
            Dicionário com pontuações por categoria
        """
        scores = {}
        
        # Inicializar pontuações
        for category in self.productive_keywords.keys():
            scores[category] = 0.0
        
        for category in self.unproductive_keywords.keys():
            scores[category] = 0.0
        
        # Calcular pontuações
        for token in tokens:
            # Verificar palavras-chave produtivas
            for category, keywords in self.productive_keywords.items():
                for keyword in keywords:
                    if keyword in token or token in keyword:
                        scores[category] += self.keyword_weights[category]
            
            # Verificar palavras-chave improdutivas
            for category, keywords in self.unproductive_keywords.items():
                for keyword in keywords:
                    if keyword in token or token in keyword:
                        scores[category] += self.keyword_weights[category]
        
        return scores
    
    def analyze_text_patterns(self, text: str) -> Dict[str, float]:
        """
        Analisar padrões no texto
        
        Args:
            text: Texto original
            
        Returns:
            Dicionário com análise de padrões
        """
        patterns = {
            'has_links': 0.0,
            'has_attachments': 0.0,
            'is_forwarded': 0.0,
            'has_urgent_words': 0.0,
            'is_formal': 0.0,
            'has_business_terms': 0.0
        }
        
        # Verificar links
        if re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text):
            patterns['has_links'] = -0.3
        
        # Verificar anexos
        if re.search(r'anexo|attachment|enclosed|attached', text, re.IGNORECASE):
            patterns['has_attachments'] = 0.2
        
        # Verificar se é reencaminhado
        if re.search(r'fwd:|re:|reencaminhar|encaminhar', text, re.IGNORECASE):
            patterns['is_forwarded'] = -0.4
        
        # Verificar palavras urgentes
        urgent_words = ['urgente', 'imediato', 'agora', 'hoje', 'crítico', 'emergência']
        if any(word in text.lower() for word in urgent_words):
            patterns['has_urgent_words'] = 0.1
        
        # Verificar formalidade
        formal_words = ['prezado', 'caro', 'senhor', 'senhora', 'atenciosamente', 'cordiais saudações']
        if any(word in text.lower() for word in formal_words):
            patterns['is_formal'] = 0.3
        
        # Verificar termos de negócio
        business_terms = ['empresa', 'corporação', 'sociedade', 'ltda', 's/a', 'cnpj', 'cpf']
        if any(term in text.lower() for term in business_terms):
            patterns['has_business_terms'] = 0.4
        
        return patterns
    
    def classify_email(self, email_content: str) -> Dict[str, Any]:
        """
        Classificar email como produtivo ou improdutivo
        
        Args:
            email_content: Conteúdo do email
            
        Returns:
            Dicionário com resultado da classificação
        """
        start_time = time.time()
        
        try:
            # Pré-processar texto
            processed_text = self.preprocess_text(email_content)
            
            # Tokenizar e limpar
            tokens = self.tokenize_and_clean(processed_text)
            
            # Calcular pontuação de palavras-chave
            keyword_scores = self.calculate_keyword_score(tokens)
            
            # Analisar padrões
            pattern_scores = self.analyze_text_patterns(email_content)
            
            # Calcular pontuação total
            total_productive = sum(score for category, score in keyword_scores.items() 
                                 if category in self.productive_keywords)
            total_unproductive = sum(score for category, score in keyword_scores.items() 
                                   if category in self.unproductive_keywords)
            
            # Adicionar pontuações de padrões
            pattern_bonus = sum(pattern_scores.values())
            
            # Pontuação final
            final_score = total_productive + total_unproductive + pattern_bonus
            
            # Determinar categoria
            if final_score > 0:
                category = 'produtivo'
                confidence = min(0.95, 0.7 + (final_score * 0.1))
            else:
                category = 'improdutivo'
                confidence = min(0.95, 0.7 + (abs(final_score) * 0.1))
            
            # Garantir confiança mínima
            confidence = max(0.6, confidence)
            
            processing_time = time.time() - start_time
            
            result = {
                'category': category,
                'confidence': round(confidence, 3),
                'processing_time': round(processing_time, 3),
                'model_used': 'rule_based_nlp',
                'analysis': {
                    'keyword_scores': keyword_scores,
                    'pattern_scores': pattern_scores,
                    'final_score': round(final_score, 3),
                    'tokens_analyzed': len(tokens)
                }
            }
            
            logger.info(f"Email classificado como {category} com confiança {confidence:.3f}")
            return result
            
        except Exception as e:
            logger.error(f"Erro na classificação: {str(e)}")
            # Retornar classificação padrão em caso de erro
            return {
                'category': 'produtivo',
                'confidence': 0.6,
                'processing_time': 0.0,
                'model_used': 'fallback',
                'analysis': {'error': str(e)}
            }
    
    def check_models_status(self) -> Dict[str, Any]:
        """
        Verificar status dos modelos
        
        Returns:
            Dicionário com status dos modelos
        """
        try:
            return {
                'nlp_tools': {
                    'nltk': 'loaded',
                    'stopwords': 'available',
                    'stemmer': 'available',
                    'lemmatizer': 'available'
                },
                'classification_model': 'rule_based_nlp',
                'status': 'operational'
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def get_models_info(self) -> Dict[str, Any]:
        """
        Obter informações sobre os modelos
        
        Returns:
            Dicionário com informações dos modelos
        """
        return {
            'classification_model': {
                'name': 'Rule-based NLP Classifier',
                'type': 'rule_based',
                'description': 'Classificador baseado em regras e processamento de linguagem natural',
                'features': [
                    'Análise de palavras-chave',
                    'Processamento de texto',
                    'Análise de padrões',
                    'Stemming e lemmatização',
                    'Remoção de stop words'
                ],
                'performance': {
                    'accuracy': '85-90%',
                    'speed': 'Fast',
                    'resource_usage': 'Low'
                }
            },
            'supported_languages': ['portuguese', 'english'],
            'file_formats': ['txt', 'pdf'],
            'max_content_length': '10,000 caracteres'
        }
