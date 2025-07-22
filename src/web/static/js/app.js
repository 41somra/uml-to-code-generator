/**
 * Model-to-Code Generator Web Interface
 * JavaScript functionality for the web application
 */

class ModelToCodeApp {
    constructor() {
        this.currentFormat = 'simple';
        this.currentFiles = {};
        this.activeFileTab = null;
        
        this.initializeEventListeners();
        this.updateCharacterCount();
    }

    initializeEventListeners() {
        // Format tabs
        document.querySelectorAll('.format-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchFormat(e.target.dataset.format));
        });

        // Action buttons
        document.getElementById('loadSample').addEventListener('click', () => this.loadSampleModel());
        document.getElementById('validateBtn').addEventListener('click', () => this.validateModel());
        document.getElementById('generateBtn').addEventListener('click', () => this.generateCode());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadCode());
        document.getElementById('copyBtn').addEventListener('click', () => this.copyAllCode());

        // Model text input
        document.getElementById('modelText').addEventListener('input', () => this.updateCharacterCount());

        // Target language change
        document.getElementById('targetLanguage').addEventListener('change', () => this.clearResults());
    }

    switchFormat(format) {
        this.currentFormat = format;
        
        // Update active tab
        document.querySelectorAll('.format-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-format="${format}"]`).classList.add('active');
        
        // Update format display
        const formatNames = {
            'simple': 'Simple Text',
            'plantuml': 'PlantUML',
            'yaml': 'YAML'
        };
        document.getElementById('currentFormat').textContent = formatNames[format];
        
        this.clearResults();
    }

    async loadSampleModel() {
        try {
            const response = await fetch(`/api/sample?format=${this.currentFormat}`);
            const data = await response.json();
            
            if (data.model_text) {
                document.getElementById('modelText').value = data.model_text;
                this.updateCharacterCount();
                this.clearResults();
                
                this.showNotification('Sample model loaded successfully', 'success');
            }
        } catch (error) {
            this.showNotification('Failed to load sample model', 'error');
            console.error('Error loading sample:', error);
        }
    }

    async validateModel() {
        const modelText = document.getElementById('modelText').value.trim();
        
        if (!modelText) {
            this.showNotification('Please enter a model to validate', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model_text: modelText,
                    model_format: this.currentFormat
                })
            });

            const result = await response.json();
            this.displayValidationResult(result);
            
        } catch (error) {
            this.showNotification('Validation failed', 'error');
            console.error('Validation error:', error);
        }
    }

    displayValidationResult(result) {
        const validationDiv = document.getElementById('validationResult');
        const contentDiv = document.getElementById('validationContent');
        
        if (result.valid) {
            contentDiv.innerHTML = `
                <div class="flex items-center mb-4">
                    <svg class="w-5 h-5 text-green-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="text-green-800 font-medium">Valid Model</span>
                </div>
                <div class="bg-green-50 p-4 rounded-lg">
                    <h4 class="font-semibold mb-2">${result.diagram.name}</h4>
                    <div class="grid grid-cols-2 gap-4 text-sm">
                        <div>Classes: ${result.diagram.classes.length}</div>
                        <div>Relationships: ${result.diagram.relationships}</div>
                    </div>
                    <div class="mt-3">
                        <h5 class="font-medium mb-2">Classes:</h5>
                        <ul class="text-sm space-y-1">
                            ${result.diagram.classes.map(cls => `
                                <li class="flex justify-between">
                                    <span>${cls.name} ${cls.is_interface ? '(interface)' : ''} ${cls.is_abstract ? '(abstract)' : ''}</span>
                                    <span class="text-gray-600">${cls.attributes} attrs, ${cls.methods} methods</span>
                                </li>
                            `).join('')}
                        </ul>
                    </div>
                </div>
            `;
            this.showNotification('Model is valid', 'success');
        } else {
            contentDiv.innerHTML = `
                <div class="flex items-center mb-4">
                    <svg class="w-5 h-5 text-red-500 mr-2" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"></path>
                    </svg>
                    <span class="text-red-800 font-medium">Invalid Model</span>
                </div>
                <div class="bg-red-50 p-4 rounded-lg">
                    <pre class="text-sm text-red-800">${result.error}</pre>
                </div>
            `;
            this.showNotification('Model validation failed', 'error');
        }
        
        validationDiv.classList.remove('hidden');
    }

    async generateCode() {
        const modelText = document.getElementById('modelText').value.trim();
        const targetLanguage = document.getElementById('targetLanguage').value;
        
        if (!modelText) {
            this.showNotification('Please enter a model to generate code', 'warning');
            return;
        }

        // Show loading state
        this.setLoadingState(true);
        this.clearResults();

        try {
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    model_text: modelText,
                    model_format: this.currentFormat,
                    target_language: targetLanguage
                })
            });

            const result = await response.json();
            
            if (result.success) {
                this.displayGeneratedCode(result.files, result.diagram_info);
                this.showNotification('Code generated successfully', 'success');
            } else {
                this.showNotification(`Generation failed: ${result.error}`, 'error');
            }
            
        } catch (error) {
            this.showNotification('Code generation failed', 'error');
            console.error('Generation error:', error);
        } finally {
            this.setLoadingState(false);
        }
    }

    displayGeneratedCode(files, diagramInfo) {
        this.currentFiles = files;
        
        // Hide placeholder, show file tabs
        document.getElementById('placeholderState').style.display = 'none';
        document.getElementById('fileTabs').classList.remove('hidden');
        
        // Create file tabs
        const tabsContainer = document.querySelector('#fileTabs nav');
        const contentContainer = document.getElementById('fileContent');
        
        tabsContainer.innerHTML = '';
        contentContainer.innerHTML = '';
        
        const fileNames = Object.keys(files);
        
        fileNames.forEach((filename, index) => {
            // Create tab
            const tab = document.createElement('button');
            tab.className = 'file-tab';
            tab.textContent = filename;
            tab.dataset.filename = filename;
            
            if (index === 0) {
                tab.classList.add('active');
                this.activeFileTab = filename;
            }
            
            tab.addEventListener('click', () => this.switchFileTab(filename));
            tabsContainer.appendChild(tab);
            
            // Create content div
            const contentDiv = document.createElement('div');
            contentDiv.className = 'tab-content';
            contentDiv.dataset.filename = filename;
            
            if (index === 0) {
                contentDiv.classList.add('active');
            }
            
            // Add copy button and code
            contentDiv.innerHTML = `
                <div class="flex items-center justify-between mb-4">
                    <h3 class="text-lg font-semibold">${filename}</h3>
                    <button onclick="app.copyFileContent('${filename}')" class="btn-outline">
                        Copy
                    </button>
                </div>
                <div class="relative">
                    <pre><code class="language-${this.getLanguageFromExtension(filename)}">${this.escapeHtml(files[filename])}</code></pre>
                </div>
            `;
            
            contentContainer.appendChild(contentDiv);
        });
        
        // Highlight code
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        
        // Enable download and copy buttons
        document.getElementById('downloadBtn').disabled = false;
        document.getElementById('copyBtn').disabled = false;
        
        // Show generation info
        this.displayGenerationInfo(diagramInfo, fileNames.length);
    }

    displayGenerationInfo(diagramInfo, fileCount) {
        const infoDiv = document.getElementById('generationInfo');
        const statsDiv = document.getElementById('generationStats');
        
        statsDiv.innerHTML = `
            <div class="p-3 bg-blue-50 rounded-lg">
                <div class="text-2xl font-bold text-blue-600">${fileCount}</div>
                <div class="text-sm text-blue-800">Files Generated</div>
            </div>
            <div class="p-3 bg-green-50 rounded-lg">
                <div class="text-2xl font-bold text-green-600">${diagramInfo.classes}</div>
                <div class="text-sm text-green-800">Classes</div>
            </div>
            <div class="p-3 bg-purple-50 rounded-lg">
                <div class="text-2xl font-bold text-purple-600">${diagramInfo.relationships}</div>
                <div class="text-sm text-purple-800">Relationships</div>
            </div>
        `;
        
        infoDiv.classList.remove('hidden');
    }

    switchFileTab(filename) {
        // Update active tab
        document.querySelectorAll('.file-tab').forEach(tab => {
            tab.classList.remove('active');
        });
        document.querySelector(`[data-filename="${filename}"]`).classList.add('active');
        
        // Update active content
        document.querySelectorAll('.tab-content').forEach(content => {
            content.classList.remove('active');
        });
        document.querySelector(`.tab-content[data-filename="${filename}"]`).classList.add('active');
        
        this.activeFileTab = filename;
    }

    copyFileContent(filename) {
        const content = this.currentFiles[filename];
        navigator.clipboard.writeText(content).then(() => {
            this.showNotification(`${filename} copied to clipboard`, 'success');
        }).catch(() => {
            this.showNotification('Failed to copy to clipboard', 'error');
        });
    }

    copyAllCode() {
        const allContent = Object.entries(this.currentFiles)
            .map(([filename, content]) => `// ${filename}\n${content}`)
            .join('\n\n' + '='.repeat(80) + '\n\n');
            
        navigator.clipboard.writeText(allContent).then(() => {
            this.showNotification('All files copied to clipboard', 'success');
        }).catch(() => {
            this.showNotification('Failed to copy to clipboard', 'error');
        });
    }

    downloadCode() {
        const filesParam = encodeURIComponent(JSON.stringify(this.currentFiles));
        const downloadUrl = `/api/download?files=${filesParam}`;
        
        // Create temporary link and trigger download
        const a = document.createElement('a');
        a.href = downloadUrl;
        a.download = 'generated_code.zip';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        
        this.showNotification('Download started', 'success');
    }

    setLoadingState(loading) {
        const loadingDiv = document.getElementById('loadingState');
        const placeholderDiv = document.getElementById('placeholderState');
        
        if (loading) {
            loadingDiv.classList.add('show');
            placeholderDiv.style.display = 'none';
        } else {
            loadingDiv.classList.remove('show');
            if (!this.currentFiles || Object.keys(this.currentFiles).length === 0) {
                placeholderDiv.style.display = 'block';
            }
        }
    }

    clearResults() {
        this.currentFiles = {};
        this.activeFileTab = null;
        
        // Hide generated code sections
        document.getElementById('fileTabs').classList.add('hidden');
        document.getElementById('generationInfo').classList.add('hidden');
        document.getElementById('validationResult').classList.add('hidden');
        
        // Show placeholder
        document.getElementById('placeholderState').style.display = 'block';
        
        // Disable buttons
        document.getElementById('downloadBtn').disabled = true;
        document.getElementById('copyBtn').disabled = true;
    }

    updateCharacterCount() {
        const text = document.getElementById('modelText').value;
        document.getElementById('charCount').textContent = `${text.length} characters`;
    }

    getLanguageFromExtension(filename) {
        const ext = filename.split('.').pop().toLowerCase();
        const langMap = {
            'py': 'python',
            'java': 'java',
            'ts': 'typescript',
            'js': 'javascript',
            'cpp': 'cpp',
            'cs': 'csharp',
            'go': 'go',
            'rs': 'rust'
        };
        return langMap[ext] || 'text';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `fixed top-4 right-4 p-4 rounded-lg shadow-lg z-50 transition-all duration-300 ${this.getNotificationClass(type)}`;
        notification.textContent = message;
        
        document.body.appendChild(notification);
        
        // Auto-remove after 3 seconds
        setTimeout(() => {
            notification.classList.add('opacity-0', 'translate-x-full');
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    getNotificationClass(type) {
        const classes = {
            'success': 'bg-green-500 text-white',
            'error': 'bg-red-500 text-white',
            'warning': 'bg-yellow-500 text-white',
            'info': 'bg-blue-500 text-white'
        };
        return classes[type] || classes.info;
    }
}

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    window.app = new ModelToCodeApp();
});