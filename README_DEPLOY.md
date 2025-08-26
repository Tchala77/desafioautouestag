# 🚀 Deploy na Vercel - Email Classifier

## 📋 Pré-requisitos

- Conta na [Vercel](https://vercel.com)
- Projeto no GitHub/GitLab/Bitbucket
- Python 3.9+ (configurado na Vercel)

## 🔧 Configuração do Projeto

### 1. Estrutura de Arquivos para Vercel

```
email-classifier/
├── api/
│   └── index.py          # Função serverless principal
├── backend/              # Código do backend
├── frontend/             # Interface web
├── vercel.json           # Configuração da Vercel
├── requirements.txt      # Dependências Python
├── package.json          # Configuração Node.js
└── .vercelignore         # Arquivos ignorados no deploy
```

### 2. Configurações Importantes

#### `vercel.json`
- Define as rotas da API (`/api/*`)
- Configura o build do Python
- Define o runtime Python 3.9

#### `api/index.py`
- Função serverless adaptada do Flask
- Endpoints: `/api/health`, `/api/analyze`, `/api/analyze-batch`
- Suporte a CORS

#### `frontend/script.js`
- Configurado para usar `/api/analyze`
- Fallback para lógica local se API falhar
- Detecção automática de ambiente (localhost vs produção)

## 🚀 Deploy na Vercel

### Opção 1: Deploy via Dashboard Web

1. **Acesse [vercel.com](https://vercel.com)**
2. **Faça login** com sua conta
3. **Clique em "New Project"**
4. **Importe seu repositório** do GitHub/GitLab/Bitbucket
5. **Configure o projeto:**
   - Framework Preset: `Other`
   - Root Directory: `.` (raiz do projeto)
   - Build Command: `echo "Build completed"`
   - Output Directory: `.`
6. **Clique em "Deploy"**

### Opção 2: Deploy via CLI

1. **Instale a CLI da Vercel:**
```bash
npm i -g vercel
```

2. **Faça login:**
```bash
vercel login
```

3. **Deploy:**
```bash
vercel
```

4. **Para produção:**
```bash
vercel --prod
```

## 🔍 Verificação do Deploy

### 1. Teste os Endpoints da API

```bash
# Health Check
curl https://seu-projeto.vercel.app/api/health

# Análise de Email
curl -X POST https://seu-projeto.vercel.app/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"content": "Precisamos agendar uma reunião para discutir o projeto."}'
```

### 2. Teste a Interface Web

- Acesse: `https://seu-projeto.vercel.app`
- Teste o upload de arquivos
- Teste a entrada direta de texto

## ⚠️ Limitações da Vercel

### 1. Funções Serverless
- **Timeout**: Máximo 10 segundos por requisição
- **Memória**: Máximo 1024MB por função
- **Tamanho**: Máximo 50MB por função

### 2. Modelos de IA
- Os modelos são carregados a cada requisição (cold start)
- Primeira requisição pode ser mais lenta
- Considere usar modelos menores para produção

### 3. Upload de Arquivos
- Não suporta upload direto de arquivos
- Use base64 ou texto direto
- Máximo 4.5MB por requisição

## 🔧 Otimizações para Produção

### 1. Modelos de IA
```python
# Em api/index.py, considere usar modelos menores
from transformers import pipeline

# Em vez de modelos grandes, use modelos otimizados
classifier = pipeline("text-classification", model="distilbert-base-uncased")
```

### 2. Cache
```python
# Implemente cache simples para evitar recarregar modelos
import hashlib
import pickle

def get_cached_result(content):
    content_hash = hashlib.md5(content.encode()).hexdigest()
    # Implementar lógica de cache
```

### 3. Rate Limiting
```python
# Implemente rate limiting básico
from collections import defaultdict
import time

request_counts = defaultdict(list)

def check_rate_limit(ip, limit=10, window=60):
    now = time.time()
    request_counts[ip] = [t for t in request_counts[ip] if now - t < window]
    
    if len(request_counts[ip]) >= limit:
        return False
    
    request_counts[ip].append(now)
    return True
```

## 🐛 Solução de Problemas

### Erro: "Module not found"
- Verifique se `requirements.txt` está na raiz
- Certifique-se de que todas as dependências estão listadas

### Erro: "Function timeout"
- Reduza o tamanho dos modelos de IA
- Implemente cache para evitar recarregar modelos

### Erro: "Memory limit exceeded"
- Use modelos menores
- Otimize o código para usar menos memória

### Erro: "CORS"
- Verifique se os headers CORS estão configurados
- Teste com diferentes origens

## 📊 Monitoramento

### 1. Logs da Vercel
- Dashboard → Projeto → Functions → Logs
- Monitore erros e performance

### 2. Métricas
- Dashboard → Projeto → Analytics
- Acompanhe requisições e tempo de resposta

### 3. Alertas
- Configure alertas para erros
- Monitore timeout e memory usage

## 🔄 Atualizações

### 1. Deploy Automático
- Conecte com GitHub para deploy automático
- Cada push na branch principal gera novo deploy

### 2. Deploy Manual
```bash
vercel --prod
```

### 3. Rollback
- Dashboard → Projeto → Deployments
- Clique em "Redeploy" em versões anteriores

## 📞 Suporte

- **Documentação Vercel**: [vercel.com/docs](https://vercel.com/docs)
- **Comunidade**: [github.com/vercel/vercel/discussions](https://github.com/vercel/vercel/discussions)
- **Status**: [vercel-status.com](https://vercel-status.com)

---

**🎉 Seu Email Classifier está funcionando na Vercel!**

**URL da API**: `https://seu-projeto.vercel.app/api/*`
**URL do Frontend**: `https://seu-projeto.vercel.app`
