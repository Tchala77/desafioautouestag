#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Response Generator
Gerador de respostas automáticas para emails
"""

import random
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ResponseGenerator:
    """
    Gerador de respostas automáticas para emails
    """
    
    def __init__(self):
        """Inicializar o gerador de respostas"""
        
        # Templates de resposta para emails produtivos
        self.productive_templates = {
            'trabalho': [
                "Obrigado pelo seu email. Vou analisar as informações e retornarei em breve com uma resposta detalhada.",
                "Perfeito! Este é um assunto importante que merece nossa atenção. Vou agendar uma reunião para discutirmos em detalhes.",
                "Excelente proposta! Gostaria de agendar uma conversa para explorarmos melhor essa oportunidade.",
                "Obrigado pelo contato profissional. Vou revisar o material e entrarei em contato nos próximos dias.",
                "Interessante! Este projeto parece muito promissor. Vou analisar a viabilidade e retornarei com feedback."
            ],
            'profissional': [
                "Obrigado pelo interesse em nossa empresa. Vou analisar seu perfil e entrarei em contato em breve.",
                "Perfeito! Sua experiência é muito relevante. Vou agendar uma entrevista para conhecermos melhor.",
                "Excelente currículo! Vou compartilhar com nossa equipe de RH e retornarei com informações sobre o processo seletivo.",
                "Obrigado pela candidatura. Vou analisar suas qualificações e entrarei em contato em breve.",
                "Interessante perfil! Vou agendar uma conversa para discutirmos as oportunidades disponíveis."
            ],
            'comercial': [
                "Obrigado pelo interesse em nossos produtos/serviços. Vou preparar uma proposta personalizada para você.",
                "Perfeito! Vou analisar suas necessidades e retornarei com uma solução adequada.",
                "Excelente oportunidade! Vou agendar uma demonstração para apresentarmos nossas soluções.",
                "Obrigado pelo contato comercial. Vou preparar um orçamento detalhado e entrarei em contato em breve.",
                "Interessante projeto! Vou analisar a viabilidade e retornarei com uma proposta comercial."
            ]
        }
        
        # Templates de resposta para emails improdutivos
        self.unproductive_templates = {
            'spam': [
                "Obrigado pelo contato, mas não posso participar deste tipo de proposta.",
                "Agradeço o envio, mas não tenho interesse neste tipo de oportunidade.",
                "Obrigado, mas não posso atender a este tipo de solicitação.",
                "Agradeço o contato, mas não posso participar desta iniciativa.",
                "Obrigado, mas não tenho interesse neste tipo de proposta."
            ],
            'corrente': [
                "Obrigado pelo envio, mas não participo de correntes de email.",
                "Agradeço o contato, mas não encaminho correntes de email.",
                "Obrigado, mas não participo deste tipo de corrente.",
                "Agradeço o envio, mas não posso participar de correntes.",
                "Obrigado, mas não encaminho correntes de email."
            ],
            'marketing_agressivo': [
                "Obrigado pelo contato, mas não tenho interesse em promoções agressivas.",
                "Agradeço a oferta, mas não posso aceitar este tipo de proposta.",
                "Obrigado, mas não tenho interesse em ofertas limitadas.",
                "Agradeço o contato, mas não posso aceitar esta oferta.",
                "Obrigado, mas não tenho interesse em promoções imperdíveis."
            ],
            'phishing': [
                "Obrigado pelo contato, mas não forneço informações pessoais por email.",
                "Agradeço o aviso, mas não clico em links suspeitos.",
                "Obrigado, mas não verifico contas através de links em email.",
                "Agradeço o contato, mas não atualizo dados pessoais por email.",
                "Obrigado, mas não clico em links de verificação de conta."
            ]
        }
        
        # Respostas neutras para casos especiais
        self.neutral_templates = [
            "Obrigado pelo seu email. Vou analisar o conteúdo e retornarei em breve.",
            "Agradeço o contato. Vou revisar as informações e entrarei em contato em breve.",
            "Obrigado pela mensagem. Vou analisar o assunto e retornarei em breve.",
            "Agradeço o email. Vou revisar o conteúdo e entrarei em contato em breve.",
            "Obrigado pelo contato. Vou analisar as informações e retornarei em breve."
        ]
        
        logger.info("ResponseGenerator inicializado com sucesso")
    
    def generate_response(self, category: str, email_content: str, confidence: float) -> str:
        """
        Gerar resposta automática baseada na categoria do email
        
        Args:
            category: Categoria do email (produtivo/improdutivo)
            email_content: Conteúdo do email
            confidence: Nível de confiança da classificação
            
        Returns:
            Resposta automática gerada
        """
        try:
            if category == 'produtivo':
                return self._generate_productive_response(email_content, confidence)
            else:
                return self._generate_unproductive_response(email_content, confidence)
                
        except Exception as e:
            logger.error(f"Erro ao gerar resposta: {str(e)}")
            return random.choice(self.neutral_templates)
    
    def _generate_productive_response(self, email_content: str, confidence: float) -> str:
        """
        Gerar resposta para email produtivo
        
        Args:
            email_content: Conteúdo do email
            confidence: Nível de confiança
            
        Returns:
            Resposta produtiva
        """
        # Determinar subcategoria baseada no conteúdo
        subcategory = self._identify_productive_subcategory(email_content)
        
        # Selecionar template apropriado
        if subcategory in self.productive_templates:
            templates = self.productive_templates[subcategory]
        else:
            templates = self.productive_templates['trabalho']  # Default
        
        # Selecionar resposta baseada na confiança
        if confidence >= 0.9:
            # Alta confiança - resposta mais específica
            response = random.choice(templates)
            response += " Estou confiante de que podemos trabalhar juntos neste projeto."
        elif confidence >= 0.8:
            # Média-alta confiança - resposta padrão
            response = random.choice(templates)
        else:
            # Baixa confiança - resposta mais genérica
            response = random.choice(self.neutral_templates)
            response += " Gostaria de entender melhor suas necessidades."
        
        return response
    
    def _generate_unproductive_response(self, email_content: str, confidence: float) -> str:
        """
        Gerar resposta para email improdutivo
        
        Args:
            email_content: Conteúdo do email
            confidence: Nível de confiança
            
        Returns:
            Resposta improdutiva
        """
        # Determinar subcategoria baseada no conteúdo
        subcategory = self._identify_unproductive_subcategory(email_content)
        
        # Selecionar template apropriado
        if subcategory in self.unproductive_templates:
            templates = self.unproductive_templates[subcategory]
        else:
            templates = self.unproductive_templates['spam']  # Default
        
        # Selecionar resposta baseada na confiança
        if confidence >= 0.9:
            # Alta confiança - resposta mais direta
            response = random.choice(templates)
            response += " Por favor, não envie mais este tipo de email."
        elif confidence >= 0.8:
            # Média-alta confiança - resposta padrão
            response = random.choice(templates)
        else:
            # Baixa confiança - resposta mais educada
            response = random.choice(self.neutral_templates)
            response += " Por favor, entre em contato apenas para assuntos profissionais."
        
        return response
    
    def _identify_productive_subcategory(self, email_content: str) -> str:
        """
        Identificar subcategoria de email produtivo
        
        Args:
            email_content: Conteúdo do email
            
        Returns:
            Subcategoria identificada
        """
        content_lower = email_content.lower()
        
        # Verificar palavras-chave para cada subcategoria
        work_keywords = ['reunião', 'projeto', 'cliente', 'negócio', 'estratégia', 'deadline']
        professional_keywords = ['curriculum', 'cv', 'entrevista', 'vaga', 'emprego', 'carreira']
        commercial_keywords = ['venda', 'compra', 'produto', 'serviço', 'preço', 'oferta']
        
        work_score = sum(1 for keyword in work_keywords if keyword in content_lower)
        professional_score = sum(1 for keyword in professional_keywords if keyword in content_lower)
        commercial_score = sum(1 for keyword in commercial_keywords if keyword in content_lower)
        
        # Retornar subcategoria com maior pontuação
        scores = {
            'trabalho': work_score,
            'profissional': professional_score,
            'comercial': commercial_score
        }
        
        return max(scores, key=scores.get)
    
    def _identify_unproductive_subcategory(self, email_content: str) -> str:
        """
        Identificar subcategoria de email improdutivo
        
        Args:
            email_content: Conteúdo do email
            
        Returns:
            Subcategoria identificada
        """
        content_lower = email_content.lower()
        
        # Verificar palavras-chave para cada subcategoria
        spam_keywords = ['corrente', 'sorte', 'loteria', 'herança', 'prêmio', 'ganhe']
        chain_keywords = ['fwd:', 'reencaminhar', 'encaminhar', 'passe adiante', 'envie para']
        aggressive_marketing_keywords = ['promoção imperdível', 'oferta limitada', 'última chance', 'não perca']
        phishing_keywords = ['verificar conta', 'atualizar dados', 'confirmar identidade', 'segurança']
        
        spam_score = sum(1 for keyword in spam_keywords if keyword in content_lower)
        chain_score = sum(1 for keyword in chain_keywords if keyword in content_lower)
        aggressive_score = sum(1 for keyword in aggressive_marketing_keywords if keyword in content_lower)
        phishing_score = sum(1 for keyword in phishing_keywords if keyword in content_lower)
        
        # Retornar subcategoria com maior pontuação
        scores = {
            'spam': spam_score,
            'corrente': chain_score,
            'marketing_agressivo': aggressive_score,
            'phishing': phishing_score
        }
        
        return max(scores, key=scores.get)
    
    def generate_custom_response(self, category: str, context: Dict[str, Any]) -> str:
        """
        Gerar resposta customizada baseada em contexto específico
        
        Args:
            category: Categoria do email
            context: Contexto adicional para personalização
            
        Returns:
            Resposta customizada
        """
        try:
            # Verificar se há contexto específico
            if 'urgency' in context and context['urgency'] == 'high':
                if category == 'produtivo':
                    return "URGENTE: Vou analisar este assunto com prioridade máxima e retornarei em até 2 horas."
                else:
                    return "URGENTE: Este assunto não é relacionado ao trabalho. Por favor, entre em contato apenas para assuntos profissionais urgentes."
            
            if 'formality' in context and context['formality'] == 'high':
                if category == 'produtivo':
                    return "Prezado(a), agradeço seu contato profissional. Vou analisar as informações e retornarei em breve com uma resposta detalhada. Atenciosamente."
                else:
                    return "Prezado(a), agradeço seu contato. No entanto, este assunto não é relacionado ao trabalho. Por favor, entre em contato apenas para assuntos profissionais. Atenciosamente."
            
            # Resposta padrão se não houver contexto específico
            return self.generate_response(category, "", 0.8)
            
        except Exception as e:
            logger.error(f"Erro ao gerar resposta customizada: {str(e)}")
            return random.choice(self.neutral_templates)
    
    def get_response_templates(self, category: str = None) -> Dict[str, Any]:
        """
        Obter templates de resposta disponíveis
        
        Args:
            category: Categoria específica (opcional)
            
        Returns:
            Dicionário com templates disponíveis
        """
        if category:
            if category == 'produtivo':
                return {
                    'templates': self.productive_templates,
                    'count': sum(len(templates) for templates in self.productive_templates.values())
                }
            elif category == 'improdutivo':
                return {
                    'templates': self.unproductive_templates,
                    'count': sum(len(templates) for templates in self.unproductive_templates.values())
                }
            else:
                return {'error': 'Categoria inválida'}
        
        return {
            'productive': {
                'templates': self.productive_templates,
                'count': sum(len(templates) for templates in self.productive_templates.values())
            },
            'unproductive': {
                'templates': self.unproductive_templates,
                'count': sum(len(templates) for templates in self.unproductive_templates.values())
            },
            'neutral': {
                'templates': self.neutral_templates,
                'count': len(self.neutral_templates)
            }
        }
