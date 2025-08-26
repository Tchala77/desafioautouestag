#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de inicialização do Email Classifier
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_python_version():
    """Verificar versão do Python"""
    if sys.version_info < (3, 8):
        print("❌ Erro: Python 3.8 ou superior é necessário")
        print(f"Versão atual: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detectado")

def check_dependencies():
    """Verificar dependências instaladas"""
    required_packages = [
        'flask', 'flask-cors', 'nltk', 'PyPDF2'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Dependências faltando: {', '.join(missing_packages)}")
        print("Execute: pip install -r backend/requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas")
    return True

def install_dependencies():
    """Instalar dependências"""
    print("📦 Instalando dependências...")
    try:
        subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'backend/requirements.txt'
        ], check=True)
        print("✅ Dependências instaladas com sucesso")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def setup_nltk_data():
    """Configurar dados do NLTK"""
    print("🔧 Configurando NLTK...")
    try:
        import nltk
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
        print("✅ NLTK configurado com sucesso")
        return True
    except Exception as e:
        print(f"❌ Erro ao configurar NLTK: {e}")
        return False

def create_directories():
    """Criar diretórios necessários"""
    directories = ['backend/uploads', 'backend/logs', 'backend/models']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Diretórios criados")

def start_backend():
    """Iniciar o backend"""
    print("🚀 Iniciando backend...")
    try:
        os.chdir('backend')
        subprocess.run([sys.executable, 'app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Backend interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")

def start_frontend():
    """Iniciar o frontend"""
    print("🌐 Iniciando frontend...")
    try:
        os.chdir('frontend')
        subprocess.run([sys.executable, '-m', 'http.server', '8000'])
    except KeyboardInterrupt:
        print("\n🛑 Frontend interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar frontend: {e}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Email Classifier - Sistema de Classificação de Emails')
    parser.add_argument('--install', action='store_true', help='Instalar dependências')
    parser.add_argument('--setup', action='store_true', help='Configurar ambiente')
    parser.add_argument('--backend', action='store_true', help='Iniciar apenas o backend')
    parser.add_argument('--frontend', action='store_true', help='Iniciar apenas o frontend')
    parser.add_argument('--full', action='store_true', help='Iniciar sistema completo')
    
    args = parser.parse_args()
    
    print("📧 Email Classifier - Sistema de Classificação Inteligente de Emails")
    print("=" * 70)
    
    # Verificar versão do Python
    check_python_version()
    
    # Criar diretórios
    create_directories()
    
    if args.install:
        if not install_dependencies():
            sys.exit(1)
    
    if args.setup:
        if not check_dependencies():
            if not install_dependencies():
                sys.exit(1)
        if not setup_nltk_data():
            sys.exit(1)
        print("✅ Ambiente configurado com sucesso")
        return
    
    # Verificar dependências
    if not check_dependencies():
        print("\n💡 Para instalar dependências, execute:")
        print("python run.py --install")
        print("ou")
        print("pip install -r backend/requirements.txt")
        sys.exit(1)
    
    # Configurar NLTK se necessário
    setup_nltk_data()
    
    if args.backend:
        start_backend()
    elif args.frontend:
        start_frontend()
    elif args.full:
        print("🚀 Iniciando sistema completo...")
        print("📖 Backend: http://localhost:5000")
        print("🌐 Frontend: http://localhost:8000")
        print("💡 Pressione Ctrl+C para parar")
        
        try:
            # Iniciar backend em background
            backend_process = subprocess.Popen([
                sys.executable, 'app.py'
            ], cwd='backend')
            
            # Aguardar um pouco para o backend inicializar
            import time
            time.sleep(3)
            
            # Iniciar frontend
            frontend_process = subprocess.Popen([
                sys.executable, '-m', 'http.server', '8000'
            ], cwd='frontend')
            
            print("✅ Sistema iniciado com sucesso!")
            print("🌐 Acesse: http://localhost:8000")
            
            # Aguardar interrupção
            try:
                backend_process.wait()
                frontend_process.wait()
            except KeyboardInterrupt:
                print("\n🛑 Parando sistema...")
                backend_process.terminate()
                frontend_process.terminate()
                print("✅ Sistema parado")
                
        except Exception as e:
            print(f"❌ Erro ao iniciar sistema: {e}")
            if 'backend_process' in locals():
                backend_process.terminate()
            if 'frontend_process' in locals():
                frontend_process.terminate()
    else:
        print("\n💡 Uso:")
        print("python run.py --install     # Instalar dependências")
        print("python run.py --setup       # Configurar ambiente")
        print("python run.py --backend     # Iniciar apenas backend")
        print("python run.py --frontend    # Iniciar apenas frontend")
        print("python run.py --full        # Iniciar sistema completo")
        print("\n🌐 Após iniciar:")
        print("Backend:  http://localhost:5000")
        print("Frontend: http://localhost:8000")

if __name__ == '__main__':
    main()
