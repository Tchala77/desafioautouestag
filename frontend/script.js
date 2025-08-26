// Email Classifier - Frontend JavaScript
class EmailClassifier {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentFile = null;
    }

    initializeElements() {
        this.fileInput = document.getElementById('fileInput');
        this.fileName = document.getElementById('fileName');
        this.emailText = document.getElementById('emailText');
        this.analyzeBtn = document.getElementById('analyzeBtn');
        this.resultsSection = document.getElementById('resultsSection');
        this.loadingSection = document.getElementById('loadingSection');
        this.categoryResult = document.getElementById('categoryResult');
        this.confidenceResult = document.getElementById('confidenceResult');
        this.aiResponse = document.getElementById('aiResponse');
        this.copyResponseBtn = document.getElementById('copyResponseBtn');
        this.newAnalysisBtn = document.getElementById('newAnalysisBtn');
    }

    bindEvents() {
        this.fileInput.addEventListener('change', (e) => this.handleFileSelect(e));
        this.analyzeBtn.addEventListener('click', () => this.analyzeEmail());
        this.copyResponseBtn.addEventListener('click', () => this.copyResponse());
        this.newAnalysisBtn.addEventListener('click', () => this.resetForm());

        // Drag and drop functionality
        this.setupDragAndDrop();

        // Textarea auto-resize
        this.emailText.addEventListener('input', () => this.autoResizeTextarea());
    }

    setupDragAndDrop() {
        const uploadArea = document.querySelector('.border-dashed');

        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, (e) => {
                e.preventDefault();
                e.stopPropagation();
            });
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.add('border-primary', 'bg-blue-50');
            });
        });

        ['dragleave', 'drop'].forEach(eventName => {
            uploadArea.addEventListener(eventName, () => {
                uploadArea.classList.remove('border-primary', 'bg-blue-50');
            });
        });

        uploadArea.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                this.handleFile(files[0]);
            }
        });
    }

    handleFileSelect(event) {
        const file = event.target.files[0];
        if (file) {
            this.handleFile(file);
        }
    }

    handleFile(file) {
        // Validate file type
        const allowedTypes = ['text/plain', 'application/pdf'];
        if (!allowedTypes.includes(file.type)) {
            this.showNotification('Tipo de arquivo não suportado. Use apenas .txt ou .pdf', 'error');
            return;
        }

        // Validate file size (max 5MB)
        if (file.size > 5 * 1024 * 1024) {
            this.showNotification('Arquivo muito grande. Tamanho máximo: 5MB', 'error');
            return;
        }

        this.currentFile = file;
        this.fileName.textContent = `📎 ${file.name}`;
        this.fileName.className = 'mt-3 text-sm text-green-600 font-medium';

        // Clear text input when file is selected
        this.emailText.value = '';

        this.showNotification(`Arquivo "${file.name}" selecionado com sucesso!`, 'success');
    }

    async analyzeEmail() {
        const text = this.emailText.value.trim();

        if (!this.currentFile && !text) {
            this.showNotification('Por favor, selecione um arquivo ou insira o texto do email', 'error');
            return;
        }

        this.showLoading();

        try {
            let emailContent = '';

            if (this.currentFile) {
                emailContent = await this.readFileContent(this.currentFile);
            } else {
                emailContent = text;
            }

            // Simulate API call (replace with actual backend endpoint)
            const result = await this.callBackendAPI(emailContent);
            this.displayResults(result);

        } catch (error) {
            console.error('Erro na análise:', error);
            this.showNotification('Erro ao analisar o email. Tente novamente.', 'error');
        } finally {
            this.hideLoading();
        }
    }

    async readFileContent(file) {
        return new Promise((resolve, reject) => {
            const reader = new FileReader();

            reader.onload = (e) => {
                resolve(e.target.result);
            };

            reader.onerror = () => {
                reject(new Error('Erro ao ler arquivo'));
            };

            if (file.type === 'text/plain') {
                reader.readAsText(file);
            } else if (file.type === 'application/pdf') {
                // For PDF files, we'll need to send the file to backend for processing
                // For now, we'll show a message that PDF processing is handled by backend
                resolve('PDF_FILE_CONTENT');
            }
        });
    }

    async callBackendAPI(emailContent) {
        // Simulate API call delay
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Mock response - replace with actual API call
        if (emailContent === 'PDF_FILE_CONTENT') {
            return {
                category: 'produtivo',
                confidence: 0.87,
                response: 'Este é um email profissional relacionado ao trabalho. Recomendo responder de forma cordial e objetiva, agradecendo o contato e solicitando mais detalhes se necessário.'
            };
        }

        // Simple classification logic for demo
        const productiveKeywords = ['reunião', 'projeto', 'trabalho', 'negócio', 'cliente', 'relatório', 'deadline', 'estratégia'];
        const unproductiveKeywords = ['corrente', 'sorte', 'fwd:', 'reencaminhar', 'spam', 'loteria', 'promoção'];

        const lowerContent = emailContent.toLowerCase();
        let productiveScore = 0;
        let unproductiveScore = 0;

        productiveKeywords.forEach(keyword => {
            if (lowerContent.includes(keyword)) productiveScore++;
        });

        unproductiveKeywords.forEach(keyword => {
            if (lowerContent.includes(keyword)) unproductiveScore++;
        });

        const isProductive = productiveScore > unproductiveScore;
        const confidence = Math.min(0.95, 0.7 + Math.abs(productiveScore - unproductiveScore) * 0.1);

        return {
            category: isProductive ? 'produtivo' : 'improdutivo',
            confidence: confidence,
            response: this.generateResponse(isProductive, emailContent)
        };
    }

    generateResponse(isProductive, content) {
        if (isProductive) {
            const responses = [
                'Excelente! Este email parece ser relacionado ao trabalho. Recomendo responder de forma profissional e objetiva.',
                'Email produtivo identificado. Sugiro uma resposta direta e focada no assunto principal.',
                'Perfeito! Este é um email de trabalho válido. Responda de forma clara e concisa.'
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        } else {
            const responses = [
                'Este email parece ser improdutivo. Considere não responder ou usar uma resposta padrão educada.',
                'Email improdutivo detectado. Recomendo uma resposta breve e neutra, ou simplesmente ignorar.',
                'Este email não parece ser relacionado ao trabalho. Considere arquivá-lo ou responder com uma mensagem padrão.'
            ];
            return responses[Math.floor(Math.random() * responses.length)];
        }
    }

    displayResults(result) {
        // Display category
        const categoryClass = result.category === 'produtivo' ? 'text-green-600' : 'text-red-600';
        const categoryIcon = result.category === 'produtivo' ? '✅' : '❌';
        const categoryText = result.category === 'produtivo' ? 'PRODUTIVO' : 'IMPRODUTIVO';

        this.categoryResult.innerHTML = `
            <div class="text-4xl mb-2">${categoryIcon}</div>
            <div class="text-2xl font-bold ${categoryClass}">${categoryText}</div>
            <p class="text-gray-600 mt-2">Email classificado como ${result.category}</p>
        `;

        // Display confidence
        const confidencePercent = Math.round(result.confidence * 100);
        const confidenceColor = confidencePercent >= 80 ? 'text-green-600' : confidencePercent >= 60 ? 'text-yellow-600' : 'text-red-600';

        this.confidenceResult.innerHTML = `
            <div class="text-4xl font-bold ${confidenceColor} mb-2">${confidencePercent}%</div>
            <div class="w-full bg-gray-200 rounded-full h-3 mb-2">
                <div class="bg-gradient-to-r from-green-400 to-blue-500 h-3 rounded-full transition-all duration-1000" style="width: ${confidencePercent}%"></div>
            </div>
            <p class="text-gray-600">Confiança da classificação</p>
        `;

        // Display AI response
        this.aiResponse.innerHTML = `
            <p class="text-gray-800 leading-relaxed">${result.response}</p>
        `;

        // Show results
        this.resultsSection.classList.remove('hidden');
        this.resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showLoading() {
        this.loadingSection.classList.remove('hidden');
        this.analyzeBtn.disabled = true;
        this.analyzeBtn.classList.add('opacity-50', 'cursor-not-allowed');
    }

    hideLoading() {
        this.loadingSection.classList.add('hidden');
        this.analyzeBtn.disabled = false;
        this.analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');
    }

    copyResponse() {
        const responseText = this.aiResponse.textContent;
        navigator.clipboard.writeText(responseText).then(() => {
            this.showNotification('Resposta copiada para a área de transferência!', 'success');

            // Visual feedback
            this.copyResponseBtn.innerHTML = '<i class="fas fa-check mr-2"></i>Copiado!';
            this.copyResponseBtn.classList.add('bg-green-500');

            setTimeout(() => {
                this.copyResponseBtn.innerHTML = '<i class="fas fa-copy mr-2"></i>Copiar Resposta';
                this.copyResponseBtn.classList.remove('bg-green-500');
            }, 2000);
        }).catch(() => {
            this.showNotification('Erro ao copiar resposta', 'error');
        });
    }

    resetForm() {
        this.currentFile = null;
        this.fileInput.value = '';
        this.fileName.textContent = '';
        this.fileName.className = 'mt-3 text-sm text-gray-500';
        this.emailText.value = '';
        this.resultsSection.classList.add('hidden');

        // Reset button states
        this.analyzeBtn.disabled = false;
        this.analyzeBtn.classList.remove('opacity-50', 'cursor-not-allowed');

        this.showNotification('Formulário resetado. Pronto para nova análise!', 'info');
    }

    autoResizeTextarea() {
        this.emailText.style.height = 'auto';
        this.emailText.style.height = this.emailText.scrollHeight + 'px';
    }

    showNotification(message, type = 'info') {
        // Remove existing notifications
        const existingNotifications = document.querySelectorAll('.notification');
        existingNotifications.forEach(notification => notification.remove());

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification fixed top-4 right-4 z-50 px-6 py-4 rounded-lg shadow-lg transform transition-all duration-300 translate-x-full`;

        const colors = {
            success: 'bg-green-500 text-white',
            error: 'bg-red-500 text-white',
            info: 'bg-blue-500 text-white',
            warning: 'bg-yellow-500 text-white'
        };

        notification.className += ` ${colors[type] || colors.info}`;

        notification.innerHTML = `
            <div class="flex items-center">
                <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'} mr-3"></i>
                <span class="font-semibold">${message}</span>
                <button class="ml-4 text-white hover:text-gray-200" onclick="this.parentElement.parentElement.remove()">
                    <i class="fas fa-times"></i>
                </button>
            </div>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => {
            notification.classList.remove('translate-x-full');
        }, 100);

        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentElement) {
                notification.classList.add('translate-x-full');
                setTimeout(() => {
                    if (notification.parentElement) {
                        notification.remove();
                    }
                }, 300);
            }
        }, 5000);
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new EmailClassifier();

    // Add some nice animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.bg-white').forEach(el => {
        observer.observe(el);
    });
});

// Add custom CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.6s ease-out forwards;
    }
    
    .notification {
        animation: slideIn 0.3s ease-out forwards;
    }
    
    @keyframes slideIn {
        from { transform: translateX(100%); }
        to { transform: translateX(0); }
    }
`;
document.head.appendChild(style);
