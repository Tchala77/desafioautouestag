# 🚀 Guia de Início Rápido - Email Classifier

## ⚡ Início Super Rápido (5 minutos)

### 1. Pré-requisitos
- Python 3.8 ou superior
- Conexão com internet

### 2. Instalação e Execução
```bash
# Clone o repositório (se aplicável)
# cd email-classifier

# Instalar dependências
python run.py --install

# Configurar ambiente
python run.py --setup

# Iniciar sistema completo
python run.py --full
```

### 3. Acessar o Sistema
- **Frontend**: http://localhost:8000
- **Backend**: http://localhost:5000

## 🎯 Como Usar

### Opção 1: Upload de Arquivo
1. Clique em "Escolher Arquivo"
2. Selecione um arquivo .txt ou .pdf
3. Clique em "Analisar Email"
4. Veja os resultados!

### Opção 2: Texto Direto
1. Cole o conteúdo do email na caixa de texto
2. Clique em "Analisar Email"
3. Veja os resultados!

## 📊 Exemplos de Teste

Use os emails de exemplo em `examples/test_emails.txt` para testar o sistema:

- **Emails Produtivos**: Reuniões, projetos, candidaturas
- **Emails Improdutivos**: Spam, correntes, phishing

## 🔧 Comandos Úteis

```bash
# Apenas backend
python run.py --backend

# Apenas frontend  
python run.py --frontend

# Sistema completo
python run.py --full

# Verificar status
curl http://localhost:5000/health
```

## 🆘 Solução de Problemas

### Erro: "Dependências não encontradas"
```bash
python run.py --install
```

### Erro: "Porta já em uso"
```bash
# Parar processos na porta 5000 ou 8000
# Ou usar portas diferentes
```

### Erro: "NLTK não configurado"
```bash
python run.py --setup
```

## 📱 Funcionalidades

- ✅ Upload de arquivos .txt e .pdf
- ✅ Entrada direta de texto
- ✅ Classificação automática (Produtivo/Improdutivo)
- ✅ Geração de respostas inteligentes
- ✅ Interface responsiva e moderna
- ✅ Drag & drop de arquivos
- ✅ Análise em lote (via API)

## 🌟 Destaques

- **IA Inteligente**: Classificação baseada em NLP
- **Interface Moderna**: Design com Tailwind CSS
- **Processamento Rápido**: Análise em segundos
- **Respostas Contextuais**: Sugestões personalizadas
- **Fácil Uso**: Interface intuitiva e responsiva

## 📞 Suporte

- **Documentação**: README.md
- **Exemplos**: examples/test_emails.txt
- **API**: http://localhost:5000 (quando backend estiver rodando)

---

**🎉 Pronto! Seu sistema de classificação de emails está funcionando!**
