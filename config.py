#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configurações do Projeto Email Classifier
"""

import os
from typing import Dict, Any

class Config:
    """Configurações base da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    # Configurações do servidor
    HOST = os.environ.get('FLASK_HOST', '0.0.0.0')
    PORT = int(os.environ.get('FLASK_PORT', 5000))
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf'}
    
    # Configurações de IA
    AI_MODEL_PATH = os.environ.get('AI_MODEL_PATH', 'models/')
    CONFIDENCE_THRESHOLD = 0.6
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Configurações de segurança
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')
    
    # Configurações de performance
    MAX_WORKERS = int(os.environ.get('MAX_WORKERS', 4))
    REQUEST_TIMEOUT = int(os.environ.get('REQUEST_TIMEOUT', 30))
    
    # Configurações de email (para futuras funcionalidades)
    SMTP_SERVER = os.environ.get('SMTP_SERVER', 'localhost')
    SMTP_PORT = int(os.environ.get('SMTP_PORT', 587))
    SMTP_USERNAME = os.environ.get('SMTP_USERNAME', '')
    SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', '')
    
    @staticmethod
    def get_database_url() -> str:
        """Obter URL do banco de dados"""
        return os.environ.get('DATABASE_URL', 'sqlite:///email_classifier.db')
    
    @staticmethod
    def get_redis_url() -> str:
        """Obter URL do Redis (para cache)"""
        return os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:8000', 'http://127.0.0.1:5000']

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY deve ser definida em produção")

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    UPLOAD_FOLDER = 'test_uploads'

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """
    Obter configuração baseada no ambiente
    
    Args:
        config_name: Nome da configuração
        
    Returns:
        Classe de configuração
    """
    if not config_name:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    return config.get(config_name, config['default'])

# Configurações específicas do classificador
CLASSIFIER_CONFIG = {
    'productive_keywords': {
        'trabalho': ['reunião', 'projeto', 'cliente', 'negócio', 'estratégia', 'deadline', 
                    'relatório', 'apresentação', 'planejamento', 'objetivo', 'meta', 'resultado',
                    'análise', 'desenvolvimento', 'implementação', 'cooperação', 'colaboração',
                    'parceria', 'contrato', 'proposta', 'orçamento', 'cronograma', 'equipe'],
        'profissional': ['curriculum', 'cv', 'entrevista', 'vaga', 'emprego', 'carreira', 
                       'formação', 'experiência', 'competência', 'habilidade', 'treinamento',
                       'certificação', 'especialização', 'graduação', 'pós-graduação'],
        'comercial': ['venda', 'compra', 'produto', 'serviço', 'preço', 'desconto', 'oferta',
                     'promoção', 'marketing', 'publicidade', 'campanha', 'mercado', 'concorrência']
    },
    'unproductive_keywords': {
        'spam': ['corrente', 'sorte', 'loteria', 'herança', 'prêmio', 'ganhe', 'grátis', 'urgente',
                'limitado', 'exclusivo', 'confidencial', 'secreto', 'oportunidade única'],
        'corrente': ['fwd:', 'reencaminhar', 'encaminhar', 'passe adiante', 'envie para', 
                    'reze por', 'bênção', 'maldição', '7 dias', '24 horas'],
        'marketing_agressivo': ['promoção imperdível', 'oferta limitada', 'última chance', 
                              'não perca', 'garantido', '100% seguro', 'sem risco'],
        'phishing': ['verificar conta', 'atualizar dados', 'confirmar identidade', 'segurança',
                    'suspensão', 'bloqueio', 'acesso restrito', 'clique aqui']
    },
    'keyword_weights': {
        'trabalho': 2.0,
        'profissional': 1.5,
        'comercial': 1.0,
        'spam': -2.0,
        'corrente': -1.5,
        'marketing_agressivo': -1.0,
        'phishing': -2.5
    }
}

# Configurações de resposta
RESPONSE_CONFIG = {
    'max_response_length': 500,
    'tone': 'professional',
    'language': 'portuguese',
    'include_emojis': False,
    'custom_signature': True
}

# Configurações de API
API_CONFIG = {
    'version': '1.0.0',
    'title': 'Email Classifier API',
    'description': 'API para classificação inteligente de emails usando IA',
    'contact': {
        'name': 'Email Classifier Team',
        'email': 'contato@emailclassifier.com'
    },
    'license': {
        'name': 'MIT',
        'url': 'https://opensource.org/licenses/MIT'
    }
}
