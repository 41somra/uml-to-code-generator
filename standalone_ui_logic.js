class StandaloneModelToCode {
    constructor() {
        this.currentFormat = 'simple';
        this.currentLanguage = 'python';
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

        // Language tabs
        document.querySelectorAll('.lang-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchLanguage(e.target.dataset.lang));
        });

        // Action buttons
        document.getElementById('loadSample').addEventListener('click', () => this.loadSampleModel());
        document.getElementById('clearBtn').addEventListener('click', () => this.clearInput());
        document.getElementById('validateBtn').addEventListener('click', () => this.validateModel());
        document.getElementById('generateBtn').addEventListener('click', () => this.generateCode());
        document.getElementById('copyAllBtn').addEventListener('click', () => this.copyAllCode());
        document.getElementById('downloadBtn').addEventListener('click', () => this.downloadCode());

        // Model text input
        document.getElementById('modelText').addEventListener('input', () => this.updateCharacterCount());
    }

    switchFormat(format) {
        this.currentFormat = format;
        
        // Update active tab
        document.querySelectorAll('.format-tab').forEach(tab => {
            tab.classList.remove('active', 'bg-blue-500', 'text-white');
            tab.classList.add('bg-gray-200', 'hover:bg-gray-300');
        });
        document.querySelector(`[data-format="${format}"]`).classList.add('active', 'bg-blue-500', 'text-white');
        document.querySelector(`[data-format="${format}"]`).classList.remove('bg-gray-200', 'hover:bg-gray-300');
        
        // Update format display
        const formatNames = {
            'simple': 'Simple Text',
            'plantuml': 'PlantUML',
            'yaml': 'YAML'
        };
        document.getElementById('currentFormat').textContent = formatNames[format];
        
        this.clearResults();
    }

    switchLanguage(language) {
        this.currentLanguage = language;
        
        // Update active tab
        document.querySelectorAll('.lang-tab').forEach(tab => {
            tab.classList.remove('active', 'bg-green-500', 'text-white');
            tab.classList.add('bg-gray-200', 'hover:bg-gray-300');
        });
        document.querySelector(`[data-lang="${language}"]`).classList.add('active', 'bg-green-500', 'text-white');
        document.querySelector(`[data-lang="${language}"]`).classList.remove('bg-gray-200', 'hover:bg-gray-300');
        
        this.clearResults();
    }

    loadSampleModel() {
        const samples = {
            simple: `User:
  id: int
  username: string
  email: string
  password: string
  getId()
  setUsername(name: string)
  validateEmail()
  changePassword(newPassword: string)

Product:
  id: int
  name: string
  price: float
  description: string
  getName()
  setPrice(price: float)
  updateDescription(desc: string)

Order:
  id: int
  userId: int
  total: float
  status: string
  createOrder()
  addItem(product: Product, quantity: int)
  calculateTotal()
  updateStatus(status: string)`,

            plantuml: `@startuml
class User {
    - id: int
    - username: string
    - email: string
    - password: string
    + getId(): int
    + setUsername(name: string): void
    + validateEmail(): boolean
    + changePassword(newPassword: string): void
}

class Product {
    - id: int
    - name: string
    - price: float
    - description: string
    + getName(): string
    + setPrice(price: float): void
    + updateDescription(desc: string): void
}

class Order {
    - id: int
    - userId: int
    - total: float
    - status: string
    + createOrder(): void
    + addItem(product: Product, quantity: int): void
    + calculateTotal(): float
    + updateStatus(status: string): void
}

User ||--o{ Order : "places"
Order }o--|| Product : "contains"
@enduml`,

            yaml: `name: "E-commerce System"
description: "Basic e-commerce domain model"

classes:
  - name: User
    attributes:
      - name: id
        type: int
        visibility: private
      - name: username
        type: string
        visibility: private
      - name: email
        type: string
        visibility: private
    methods:
      - name: getId
        return_type: int
        visibility: public
      - name: setUsername
        visibility: public
        parameters:
          - name: name
            type: string

  - name: Product
    attributes:
      - name: id
        type: int
        visibility: private
      - name: name
        type: string
        visibility: private
      - name: price
        type: float
        visibility: private
    methods:
      - name: getName
        return_type: string
        visibility: public
      - name: setPrice
        visibility: public
        parameters:
          - name: price
            type: float`
        };

        document.getElementById('modelText').value = samples[this.currentFormat];
        this.updateCharacterCount();
        this.updateStatus('Sample model loaded', 'success');
    }

    clearInput() {
        document.getElementById('modelText').value = '';
        this.updateCharacterCount();
        this.clearResults();
        this.updateStatus('Input cleared', 'info');
    }

    validateModel() {
        const modelText = document.getElementById('modelText').value.trim();
        
        if (!modelText) {
            this.updateStatus('Please enter a model to validate', 'warning');
            return;
        }

        // Simple validation (in a real app, this would use the actual parser)
        const lines = modelText.split('\n').filter(line => line.trim());
        
        if (this.currentFormat === 'simple') {
            const classCount = lines.filter(line => line.endsWith(':')).length;
            const methodCount = lines.filter(line => line.includes('(') && line.includes(')')).length;
            
            if (classCount > 0) {
                this.updateStatus(`✅ Valid model: ${classCount} classes, ${methodCount} methods`, 'success');
            } else {
                this.updateStatus('⚠️ No classes found in model', 'warning');
            }
        } else {
            this.updateStatus('✅ Model syntax appears valid', 'success');
        }
    }

    generateCode() {
        const modelText = document.getElementById('modelText').value.trim();
        
        if (!modelText) {
            this.updateStatus('Please enter a model to generate code', 'warning');
            return;
        }

        this.updateStatus('Generating code...', 'info');

        // Simulate code generation (in a real app, this would call the backend)
        setTimeout(() => {
            const generatedFiles = this.simulateCodeGeneration(modelText);
            this.displayGeneratedCode(generatedFiles);
            this.updateStatus(`✅ Generated ${Object.keys(generatedFiles).length} files`, 'success');
        }, 1000);
    }

    simulateCodeGeneration(modelText) {
        // Simple code generation simulation
        const classes = this.parseSimpleModel(modelText);
        const files = {};

        classes.forEach(cls => {
            const filename = this.generateFilename(cls.name);
            files[filename] = this.generateClassCode(cls);
        });

        return files;
    }

    parseSimpleModel(modelText) {
        const lines = modelText.split('\n');
        const classes = [];
        let currentClass = null;

        lines.forEach(line => {
            const trimmed = line.trim();
            
            if (trimmed.endsWith(':')) {
                if (currentClass) classes.push(currentClass);
                currentClass = {
                    name: trimmed.slice(0, -1),
                    attributes: [],
                    methods: []
                };
            } else if (currentClass && trimmed) {
                if (trimmed.includes('(') && trimmed.includes(')')) {
                    currentClass.methods.push(trimmed);
                } else if (trimmed.includes(':')) {
                    currentClass.attributes.push(trimmed);
                }
            }
        });

        if (currentClass) classes.push(currentClass);
        return classes;
    }

    generateFilename(className) {
        const extensions = {
            python: '.py',
            java: '.java',
            typescript: '.ts'
        };

        if (this.currentLanguage === 'python') {
            return className.toLowerCase().replace(/([A-Z])/g, '_$1').replace(/^_/, '') + extensions[this.currentLanguage];
        } else {
            return className + extensions[this.currentLanguage];
        }
    }

    generateClassCode(cls) {
        const generators = {
            python: () => this.generatePythonCode(cls),
            java: () => this.generateJavaCode(cls),
            typescript: () => this.generateTypeScriptCode(cls)
        };

        return generators[this.currentLanguage]();
    }

    generatePythonCode(cls) {
        let code = `"""${cls.name} class\nGenerated from UML model\n"""\n\n`;
        code += `class ${cls.name}:\n`;
        code += `    """${cls.name} class"""\n\n`;
        
        // Constructor
        code += `    def __init__(self):\n`;
        code += `        """Initialize the class instance"""\n`;
        cls.attributes.forEach(attr => {
            const [name, type] = attr.split(':').map(s => s.trim());
            code += `        self._${name} = None  # ${type}\n`;
        });
        
        if (cls.attributes.length === 0) {
            code += `        pass\n`;
        }
        code += `\n`;

        // Methods
        cls.methods.forEach(method => {
            const methodName = method.split('(')[0];
            code += `    def ${methodName}(self):\n`;
            code += `        """${methodName} method"""\n`;
            code += `        pass\n\n`;
        });

        return code;
    }

    generateJavaCode(cls) {
        let code = `/**\n * ${cls.name} class\n * Generated from UML model\n */\n`;
        code += `public class ${cls.name} {\n\n`;

        // Attributes
        cls.attributes.forEach(attr => {
            const [name, type] = attr.split(':').map(s => s.trim());
            const javaType = this.mapToJavaType(type);
            code += `    private ${javaType} ${name};\n`;
        });

        if (cls.attributes.length > 0) code += `\n`;

        // Constructor
        code += `    /**\n     * Default constructor for ${cls.name}\n     */\n`;
        code += `    public ${cls.name}() {\n`;
        code += `    }\n\n`;

        // Methods
        cls.methods.forEach(method => {
            const methodName = method.split('(')[0];
            code += `    /**\n     * ${methodName} method\n     */\n`;
            code += `    public void ${methodName}() {\n`;
            code += `        // TODO: Implement method\n`;
            code += `    }\n\n`;
        });

        code += `}\n`;
        return code;
    }

    generateTypeScriptCode(cls) {
        let code = `/**\n * ${cls.name} class\n * Generated from UML model\n */\n`;
        code += `export class ${cls.name} {\n`;

        // Attributes
        cls.attributes.forEach(attr => {
            const [name, type] = attr.split(':').map(s => s.trim());
            const tsType = this.mapToTypeScriptType(type);
            code += `  private ${name}: ${tsType};\n`;
        });

        if (cls.attributes.length > 0) code += `\n`;

        // Constructor
        code += `  /**\n   * Creates an instance of ${cls.name}\n   */\n`;
        code += `  constructor() {\n`;
        cls.attributes.forEach(attr => {
            const [name, type] = attr.split(':').map(s => s.trim());
            const defaultValue = this.getTypeScriptDefault(this.mapToTypeScriptType(type));
            code += `    this.${name} = ${defaultValue};\n`;
        });
        code += `  }\n\n`;

        // Methods
        cls.methods.forEach(method => {
            const methodName = method.split('(')[0];
            code += `  /**\n   * ${methodName} method\n   */\n`;
            code += `  public ${methodName}(): void {\n`;
            code += `    // TODO: Implement method\n`;
            code += `  }\n\n`;
        });

        code += `}\n`;
        return code;
    }

    mapToJavaType(type) {
        const mapping = {
            'int': 'int',
            'integer': 'int',
            'string': 'String',
            'float': 'float',
            'boolean': 'boolean',
            'bool': 'boolean'
        };
        return mapping[type.toLowerCase()] || 'Object';
    }

    mapToTypeScriptType(type) {
        const mapping = {
            'int': 'number',
            'integer': 'number',
            'string': 'string',
            'float': 'number',
            'boolean': 'boolean',
            'bool': 'boolean'
        };
        return mapping[type.toLowerCase()] || 'any';
    }

    getTypeScriptDefault(type) {
        const defaults = {
            'number': '0',
            'string': '""',
            'boolean': 'false'
        };
        return defaults[type] || 'undefined';
    }

    displayGeneratedCode(files) {
        this.currentFiles = files;
        
        // Hide placeholder, show file tabs
        document.getElementById('placeholderState').style.display = 'none';
        document.getElementById('fileTabs').classList.remove('hidden');
        
        // Create file tabs
        const tabsContainer = document.getElementById('fileTabsNav');
        const contentContainer = document.getElementById('fileContent');
        
        tabsContainer.innerHTML = '';
        contentContainer.innerHTML = '';
        
        const fileNames = Object.keys(files);
        
        fileNames.forEach((filename, index) => {
            // Create tab
            const tab = document.createElement('button');
            tab.className = 'px-4 py-2 text-sm font-medium border-b-2 border-transparent hover:text-gray-700 hover:border-gray-300 whitespace-nowrap';
            tab.textContent = filename;
            tab.dataset.filename = filename;
            
            if (index === 0) {
                tab.classList.add('text-blue-600', 'border-blue-500');
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
                    <button onclick="app.copyFileContent('${filename}')" class="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600">
                        Copy
                    </button>
                </div>
                <div class="relative">
                    <pre class="bg-gray-50 p-4 rounded-lg overflow-x-auto"><code class="language-${this.getLanguageFromExtension(filename)}">${this.escapeHtml(files[filename])}</code></pre>
                </div>
            `;
            
            contentContainer.appendChild(contentDiv);
        });
        
        // Highlight code
        document.querySelectorAll('pre code').forEach((block) => {
            hljs.highlightElement(block);
        });
        
        // Enable buttons
        document.getElementById('copyAllBtn').disabled = false;
        document.getElementById('downloadBtn').disabled = false;
    }

    switchFileTab(filename) {
        // Update active tab
        document.querySelectorAll('#fileTabsNav button').forEach(tab => {
            tab.classList.remove('text-blue-600', 'border-blue-500');
        });
        document.querySelector(`#fileTabsNav [data-filename="${filename}"]`).classList.add('text-blue-600', 'border-blue-500');
        
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
            this.updateStatus(`Copied ${filename} to clipboard`, 'success');
        }).catch(() => {
            this.updateStatus('Failed to copy to clipboard', 'error');
        });
    }

    copyAllCode() {
        const allContent = Object.entries(this.currentFiles)
            .map(([filename, content]) => `// ${filename}\n${content}`)
            .join('\n\n' + '='.repeat(80) + '\n\n');
            
        navigator.clipboard.writeText(allContent).then(() => {
            this.updateStatus('All files copied to clipboard', 'success');
        }).catch(() => {
            this.updateStatus('Failed to copy to clipboard', 'error');
        });
    }

    downloadCode() {
        // Create downloadable files as individual downloads
        Object.entries(this.currentFiles).forEach(([filename, content]) => {
            const blob = new Blob([content], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
            URL.revokeObjectURL(url);
        });
        
        this.updateStatus('Files downloaded', 'success');
    }

    clearResults() {
        this.currentFiles = {};
        this.activeFileTab = null;
        
        // Hide generated code sections
        document.getElementById('fileTabs').classList.add('hidden');
        
        // Show placeholder
        document.getElementById('placeholderState').style.display = 'block';
        
        // Disable buttons
        document.getElementById('copyAllBtn').disabled = true;
        document.getElementById('downloadBtn').disabled = true;
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
            'js': 'javascript'
        };
        return langMap[ext] || 'text';
    }

    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    updateStatus(message, type = 'info') {
        const statusElement = document.getElementById('statusText');
        statusElement.textContent = message;
        
        // Reset classes
        statusElement.className = '';
        
        // Add type-specific classes
        if (type === 'success') {
            statusElement.className = 'text-green-600 font-medium';
        } else if (type === 'error') {
            statusElement.className = 'text-red-600 font-medium';
        } else if (type === 'warning') {
            statusElement.className = 'text-yellow-600 font-medium';
        } else {
            statusElement.className = 'text-blue-600 font-medium';
        }
    }
}

// Initialize the app
const app = new StandaloneModelToCode();