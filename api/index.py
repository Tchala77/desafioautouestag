#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Classifier API para Vercel
Função serverless adaptada do Flask app
"""

import sys
import os
from http.server import BaseHTTPRequestHandler
import json
import logging
from urllib.parse import parse_qs, urlparse

# Adicionar o diretório backend ao path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

try:
    from classifier import EmailClassifier
    from response_generator import ResponseGenerator
except ImportError as e:
    print(f"Erro ao importar módulos: {e}")

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Inicializar classificador e gerador de respostas
try:
    classifier = EmailClassifier()
    response_generator = ResponseGenerator()
except Exception as e:
    logger.error(f"Erro ao inicializar modelos: {e}")
    classifier = None
    response_generator = None

class EmailClassifierHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        """Handler para requisições GET"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/health':
            self.handle_health_check()
        elif path == '/api/models':
            self.handle_models_info()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Endpoint não encontrado'}).encode())
    
    def do_POST(self):
        """Handler para requisições POST"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        
        if path == '/api/analyze':
            self.handle_analyze_email()
        elif path == '/api/analyze-batch':
            self.handle_analyze_batch()
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Endpoint não encontrado'}).encode())
    
    def handle_health_check(self):
        """Verificação de saúde da API"""
        try:
            if classifier:
                models_status = classifier.check_models_status()
            else:
                models_status = {'status': 'error', 'message': 'Modelos não carregados'}
            
            response = {
                'status': 'healthy' if classifier else 'unhealthy',
                'timestamp': '2024-01-01T00:00:00Z',
                'models': models_status,
                'version': '1.0.0'
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Erro no health check: {str(e)}")
            response = {
                'status': 'unhealthy',
                'error': str(e),
                'timestamp': '2024-01-01T00:00:00Z'
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
    
    def handle_models_info(self):
        """Informações sobre os modelos de IA utilizados"""
        try:
            if classifier:
                models_info = classifier.get_models_info()
            else:
                models_info = {'error': 'Modelos não carregados'}
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(models_info).encode())
            
        except Exception as e:
            logger.error(f"Erro ao obter informações dos modelos: {str(e)}")
            response = {'error': str(e)}
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
    
    def handle_analyze_email(self):
        """Análise de email individual"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            if not post_data:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Dados não fornecidos'}).encode())
                return
            
            data = json.loads(post_data.decode('utf-8'))
            email_content = data.get('content', '')
            
            if not email_content:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Conteúdo do email não fornecido'}).encode())
                return
            
            # Classificar email
            if classifier:
                classification_result = classifier.classify_email(email_content)
                
                # Gerar resposta
                ai_response = response_generator.generate_response(
                    classification_result['category'],
                    email_content,
                    classification_result['confidence']
                )
                
                response = {
                    'success': True,
                    'category': classification_result['category'],
                    'confidence': classification_result['confidence'],
                    'response': ai_response
                }
            else:
                response = {
                    'success': False,
                    'error': 'Modelos não carregados'
                }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Erro na análise de email: {str(e)}")
            response = {
                'success': False,
                'error': 'Erro interno do servidor',
                'details': str(e)
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
    
    def handle_analyze_batch(self):
        """Análise em lote de múltiplos emails"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            
            if not post_data:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Dados não fornecidos'}).encode())
                return
            
            data = json.loads(post_data.decode('utf-8'))
            emails = data.get('emails', [])
            
            if not isinstance(emails, list) or len(emails) > 50:
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({'error': 'Lista inválida ou muito longa. Máximo: 50 emails'}).encode())
                return
            
            if not classifier:
                response = {
                    'success': False,
                    'error': 'Modelos não carregados'
                }
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response).encode())
                return
            
            results = []
            for i, email_data in enumerate(emails):
                try:
                    if isinstance(email_data, str):
                        email_content = email_data
                    elif isinstance(email_data, dict) and 'content' in email_data:
                        email_content = email_data['content']
                    else:
                        results.append({
                            'index': i,
                            'success': False,
                            'error': 'Formato inválido'
                        })
                        continue
                    
                    # Classificar email
                    classification_result = classifier.classify_email(email_content)
                    
                    # Gerar resposta
                    ai_response = response_generator.generate_response(
                        classification_result['category'],
                        email_content,
                        classification_result['confidence']
                    )
                    
                    results.append({
                        'index': i,
                        'success': True,
                        'category': classification_result['category'],
                        'confidence': classification_result['confidence'],
                        'response': ai_response
                    })
                    
                except Exception as e:
                    results.append({
                        'index': i,
                        'success': False,
                        'error': str(e)
                    })
            
            response = {
                'success': True,
                'total_processed': len(emails),
                'results': results
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            logger.error(f"Erro na análise em lote: {str(e)}")
            response = {
                'success': False,
                'error': 'Erro interno do servidor',
                'details': str(e)
            }
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
    
    def do_OPTIONS(self):
        """Handler para requisições OPTIONS (CORS preflight)"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

# Função principal para Vercel
def handler(request, context):
    """Função principal para Vercel"""
    if request.method == 'GET':
        handler = EmailClassifierHandler(request, context, None)
        handler.do_GET()
    elif request.method == 'POST':
        handler = EmailClassifierHandler(request, context, None)
        handler.do_POST()
    elif request.method == 'OPTIONS':
        handler = EmailClassifierHandler(request, context, None)
        handler.do_OPTIONS()
    else:
        return {
            'statusCode': 405,
            'body': json.dumps({'error': 'Método não permitido'})
        }
    
    return {
        'statusCode': handler.response_code if hasattr(handler, 'response_code') else 200,
        'body': handler.response_body if hasattr(handler, 'response_body') else ''
    }
