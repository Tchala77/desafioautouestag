#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Email Classifier Backend
Sistema de classificação inteligente de emails usando IA
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from werkzeug.utils import secure_filename
from classifier import EmailClassifier
from response_generator import ResponseGenerator
import traceback

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Habilitar CORS para desenvolvimento

# Configurações
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024  # 10MB max
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf'}

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Inicializar classificador e gerador de respostas
classifier = EmailClassifier()
response_generator = ResponseGenerator()

def allowed_file(filename):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def home():
    """Endpoint raiz"""
    return jsonify({
        'message': 'Email Classifier API',
        'version': '1.0.0',
        'status': 'active',
        'endpoints': {
            '/analyze': 'POST - Analisar email (texto ou arquivo)',
            '/health': 'GET - Status da API',
            '/models': 'GET - Informações dos modelos de IA'
        }
    })

@app.route('/health')
def health_check():
    """Verificação de saúde da API"""
    try:
        # Verificar se os modelos estão carregados
        models_status = classifier.check_models_status()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': '2024-01-01T00:00:00Z',
            'models': models_status,
            'version': '1.0.0'
        })
    except Exception as e:
        logger.error(f"Erro no health check: {str(e)}")
        return jsonify({
            'status': 'unhealthy',
            'error': str(e),
            'timestamp': '2024-01-01T00:00:00Z'
        }), 500

@app.route('/models')
def models_info():
    """Informações sobre os modelos de IA utilizados"""
    try:
        models_info = classifier.get_models_info()
        return jsonify(models_info)
    except Exception as e:
        logger.error(f"Erro ao obter informações dos modelos: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/analyze', methods=['POST'])
def analyze_email():
    """
    Endpoint principal para análise de emails
    Aceita texto direto ou arquivo (.txt, .pdf)
    """
    try:
        # Verificar se há arquivo ou texto
        if 'file' in request.files:
            file = request.files['file']
            
            if file.filename == '':
                return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
            
            if not allowed_file(file.filename):
                return jsonify({'error': 'Tipo de arquivo não suportado. Use apenas .txt ou .pdf'}), 400
            
            # Salvar arquivo temporariamente
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Extrair texto do arquivo
                if filename.endswith('.txt'):
                    with open(filepath, 'r', encoding='utf-8') as f:
                        email_content = f.read()
                elif filename.endswith('.pdf'):
                    email_content = classifier.extract_pdf_text(filepath)
                else:
                    return jsonify({'error': 'Tipo de arquivo não suportado'}), 400
                
            finally:
                # Limpar arquivo temporário
                if os.path.exists(filepath):
                    os.remove(filepath)
                    
        elif 'text' in request.form:
            email_content = request.form['text'].strip()
            if not email_content:
                return jsonify({'error': 'Texto do email não fornecido'}), 400
        else:
            return jsonify({'error': 'Forneça um arquivo ou texto para análise'}), 400
        
        # Validar tamanho do conteúdo
        if len(email_content) > 10000:  # Máximo 10k caracteres
            return jsonify({'error': 'Conteúdo muito longo. Máximo: 10.000 caracteres'}), 400
        
        logger.info(f"Analisando email com {len(email_content)} caracteres")
        
        # Classificar email
        classification_result = classifier.classify_email(email_content)
        
        # Gerar resposta automática
        ai_response = response_generator.generate_response(
            classification_result['category'],
            email_content,
            classification_result['confidence']
        )
        
        # Preparar resposta
        result = {
            'success': True,
            'category': classification_result['category'],
            'confidence': classification_result['confidence'],
            'response': ai_response,
            'analysis': {
                'content_length': len(email_content),
                'processing_time': classification_result.get('processing_time', 0),
                'model_used': classification_result.get('model_used', 'default')
            }
        }
        
        logger.info(f"Email classificado como {classification_result['category']} com {classification_result['confidence']:.2f} de confiança")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro na análise: {str(e)}")
        logger.error(traceback.format_exc())
        
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'details': str(e) if app.debug else 'Erro durante a análise'
        }), 500

@app.route('/analyze/batch', methods=['POST'])
def analyze_batch():
    """
    Endpoint para análise em lote de múltiplos emails
    """
    try:
        data = request.get_json()
        
        if not data or 'emails' not in data:
            return jsonify({'error': 'Lista de emails não fornecida'}), 400
        
        emails = data['emails']
        if not isinstance(emails, list) or len(emails) > 50:  # Máximo 50 emails por lote
            return jsonify({'error': 'Lista inválida ou muito longa. Máximo: 50 emails'}), 400
        
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
        
        return jsonify({
            'success': True,
            'total_processed': len(emails),
            'results': results
        })
        
    except Exception as e:
        logger.error(f"Erro na análise em lote: {str(e)}")
        return jsonify({
            'success': False,
            'error': 'Erro interno do servidor',
            'details': str(e) if app.debug else 'Erro durante a análise em lote'
        }), 500

@app.errorhandler(413)
def too_large(e):
    """Handler para arquivos muito grandes"""
    return jsonify({'error': 'Arquivo muito grande. Tamanho máximo: 10MB'}), 413

@app.errorhandler(404)
def not_found(e):
    """Handler para rotas não encontradas"""
    return jsonify({'error': 'Endpoint não encontrado'}), 404

@app.errorhandler(500)
def internal_error(e):
    """Handler para erros internos"""
    logger.error(f"Erro interno: {str(e)}")
    return jsonify({'error': 'Erro interno do servidor'}), 500

if __name__ == '__main__':
    # Configurações de desenvolvimento
    debug_mode = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = int(os.getenv('FLASK_PORT', 5000))
    
    logger.info(f"Iniciando Email Classifier API em {host}:{port}")
    logger.info(f"Modo debug: {debug_mode}")
    
    app.run(
        host=host,
        port=port,
        debug=debug_mode,
        threaded=True
    )
