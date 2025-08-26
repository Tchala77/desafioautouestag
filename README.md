# 📧 Email Classifier - Sistema de Classificação Inteligente de Emails

## 🎯 Descrição do Projeto

Sistema inteligente que classifica emails automaticamente como **Produtivo** ou **Improdutivo** e gera respostas automáticas personalizadas usando técnicas de Processamento de Linguagem Natural (NLP) e Inteligência Artificial.

## ✨ Funcionalidades

- **Upload de Arquivos**: Suporte para arquivos .txt e .pdf
- **Entrada Direta de Texto**: Interface para inserção manual de conteúdo de email
- **Classificação Automática**: IA determina se o email é produtivo ou improdutivo
- **Respostas Inteligentes**: Geração automática de respostas baseadas na categoria
- **Interface Moderna**: Design responsivo e intuitivo com Tailwind CSS

## 🚀 Tecnologias Utilizadas

### Frontend
- **HTML5** - Estrutura semântica
- **Tailwind CSS** - Framework de utilitários CSS
- **JavaScript** - Interatividade e comunicação com backend

### Backend
- **Python 3.8+** - Linguagem principal
- **Flask** - Framework web para API
- **Transformers (Hugging Face)** - Modelos de IA para NLP
- **NLTK** - Processamento de linguagem natural
- **PyPDF2** - Leitura de arquivos PDF

## 📁 Estrutura do Projeto

```
email-classifier/
├── frontend/
│   ├── index.html
│   ├── styles.css
│   └── script.js
├── backend/
│   ├── app.py
│   ├── classifier.py
│   ├── requirements.txt
│   └── models/
├── README.md
└── .gitignore
```

## 🛠️ Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- Navegador web moderno
- Conexão com internet (para download dos modelos de IA)

### Backend

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd email-classifier
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

3. **Instale as dependências**
```bash
cd backend
pip install -r requirements.txt
```

4. **Execute o servidor**
```bash
python app.py
```

O backend estará rodando em `http://localhost:5000`

### Frontend

1. **Abra o arquivo `frontend/index.html` em seu navegador**
2. **Ou use um servidor local simples**
```bash
cd frontend
python -m http.server 8000
```

## 📖 Como Usar

1. **Acesse a interface web**
2. **Escolha uma das opções de entrada:**
   - Upload de arquivo (.txt ou .pdf)
   - Inserção direta de texto
3. **Clique em "Analisar Email"**
4. **Visualize os resultados:**
   - Categoria atribuída (Produtivo/Improdutivo)
   - Resposta automática sugerida
   - Confiança da classificação

## 🔧 Configurações Avançadas

### Modelos de IA
O sistema utiliza modelos pré-treinados do Hugging Face. Para personalizar:

1. Edite `backend/classifier.py`
2. Altere o modelo de classificação
3. Ajuste os parâmetros de processamento

### Personalização de Respostas
Edite `backend/response_generator.py` para:
- Modificar o tom das respostas
- Adicionar novas categorias
- Personalizar templates de resposta

## 📊 Exemplos de Uso

### Email Produtivo
```
Assunto: Reunião de Planejamento Q4
Conteúdo: Precisamos agendar uma reunião para discutir as estratégias do próximo trimestre...
```

**Resultado**: Produtivo (95% confiança)
**Resposta**: "Perfeito! Vou agendar a reunião para o próximo trimestre..."

### Email Improdutivo
```
Assunto: Fwd: Corrente da Sorte
Conteúdo: Envie esta mensagem para 10 pessoas e terá sorte...
```

**Resultado**: Improdutivo (98% confiança)
**Resposta**: "Obrigado pelo envio, mas não posso participar de correntes..."

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 👥 Autores

- **Seu Nome** - *Desenvolvimento inicial* - [SeuGitHub](https://github.com/seugithub)

## 🙏 Agradecimentos

- Hugging Face pela disponibilização dos modelos de IA
- Comunidade Python por ferramentas e bibliotecas
- Tailwind CSS pela framework de estilização

## 📞 Suporte

Para dúvidas, sugestões ou problemas:
- Abra uma [Issue](../../issues)
- Entre em contato: seuemail@exemplo.com

---

⭐ **Se este projeto te ajudou, considere dar uma estrela!**
