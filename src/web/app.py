"""
Flask web application for Model-to-Code generator
Provides a web interface for uploading models and generating code
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import tempfile
import zipfile
from io import StringIO

from ..parsers.text_parser import TextModelParser
from ..generators.python_generator import PythonCodeGenerator
from ..generators.java_generator import JavaCodeGenerator
from ..generators.typescript_generator import TypeScriptCodeGenerator
from ..models.class_model import create_sample_model


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Initialize generators (including Kessel Run generators if available)
generators = {
    'python': PythonCodeGenerator(),
    'java': JavaCodeGenerator(),
    'typescript': TypeScriptCodeGenerator()
}

# Add Kessel Run generators if available
try:
    from ..generators.microservice_generator import MicroserviceGenerator
    from ..generators.openapi_generator import OpenAPIGenerator
    from ..generators.devsecops_generator import DevSecOpsGenerator
    
    generators.update({
        'microservices': MicroserviceGenerator(),
        'openapi': OpenAPIGenerator(),
        'devsecops': DevSecOpsGenerator()
    })
except ImportError:
    pass

parser = TextModelParser()


@app.route('/')
def index():
    """Main page with model input form"""
    return render_template('index.html')


@app.route('/api/generate', methods=['POST'])
def generate_code():
    """Generate code from uploaded model"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        model_text = data.get('model_text', '').strip()
        model_format = data.get('model_format', 'simple')
        target_language = data.get('target_language', 'python')
        
        if not model_text:
            return jsonify({'error': 'No model text provided'}), 400
        
        # Parse the model
        try:
            if model_format == 'plantuml':
                diagram = parser.parse_plantuml(model_text)
            elif model_format == 'yaml':
                diagram = parser.parse_yaml(model_text)
            elif model_format == 'simple':
                diagram = parser.parse_simple_text(model_text)
            else:
                return jsonify({'error': f'Unsupported model format: {model_format}'}), 400
        except Exception as e:
            return jsonify({'error': f'Failed to parse model: {str(e)}'}), 400
        
        # Generate code
        try:
            generator = generators.get(target_language)
            if not generator:
                return jsonify({'error': f'Unsupported target language: {target_language}'}), 400
            
            generated_files = generator.generate(diagram)
        except Exception as e:
            return jsonify({'error': f'Failed to generate code: {str(e)}'}), 400
        
        return jsonify({
            'success': True,
            'files': generated_files,
            'diagram_info': {
                'name': diagram.name,
                'classes': len(diagram.classes),
                'relationships': len(diagram.relationships)
            }
        })
    
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500


@app.route('/api/sample')
def get_sample_model():
    """Get a sample model for demonstration"""
    sample_format = request.args.get('format', 'simple')
    
    if sample_format == 'plantuml':
        from ..parsers.text_parser import SAMPLE_PLANTUML
        return jsonify({
            'model_text': SAMPLE_PLANTUML,
            'format': 'plantuml'
        })
    elif sample_format == 'yaml':
        from ..parsers.text_parser import SAMPLE_YAML
        return jsonify({
            'model_text': SAMPLE_YAML,
            'format': 'yaml'
        })
    else:
        from ..parsers.text_parser import SAMPLE_SIMPLE_TEXT
        return jsonify({
            'model_text': SAMPLE_SIMPLE_TEXT,
            'format': 'simple'
        })


@app.route('/api/download')
def download_generated_code():
    """Download generated code as a ZIP file"""
    try:
        files_data = request.args.get('files')
        if not files_data:
            return jsonify({'error': 'No files data provided'}), 400
        
        import json
        files = json.loads(files_data)
        
        # Create a temporary ZIP file
        temp_dir = tempfile.mkdtemp()
        zip_path = os.path.join(temp_dir, 'generated_code.zip')
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for filename, content in files.items():
                zipf.writestr(filename, content)
        
        return send_from_directory(temp_dir, 'generated_code.zip', as_attachment=True)
    
    except Exception as e:
        return jsonify({'error': f'Failed to create download: {str(e)}'}), 500


@app.route('/api/validate', methods=['POST'])
def validate_model():
    """Validate model syntax without generating code"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        model_text = data.get('model_text', '').strip()
        model_format = data.get('model_format', 'simple')
        
        if not model_text:
            return jsonify({'error': 'No model text provided'}), 400
        
        # Try to parse the model
        try:
            if model_format == 'plantuml':
                diagram = parser.parse_plantuml(model_text)
            elif model_format == 'yaml':
                diagram = parser.parse_yaml(model_text)
            elif model_format == 'simple':
                diagram = parser.parse_simple_text(model_text)
            else:
                return jsonify({'error': f'Unsupported model format: {model_format}'}), 400
        except Exception as e:
            return jsonify({
                'valid': False,
                'error': str(e)
            })
        
        # Extract model information
        class_info = []
        for cls in diagram.classes:
            class_info.append({
                'name': cls.name,
                'attributes': len(cls.attributes),
                'methods': len(cls.methods),
                'is_abstract': cls.is_abstract,
                'is_interface': cls.is_interface
            })
        
        return jsonify({
            'valid': True,
            'diagram': {
                'name': diagram.name,
                'classes': class_info,
                'relationships': len(diagram.relationships)
            }
        })
    
    except Exception as e:
        return jsonify({
            'valid': False,
            'error': f'Unexpected error: {str(e)}'
        })


@app.errorhandler(413)
def too_large(e):
    return jsonify({'error': 'File too large'}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({'error': 'Internal server error'}), 500


@app.route('/health')
def health_check():
    """Health check endpoint for DoD Platform One"""
    return jsonify({
        'status': 'healthy',
        'timestamp': '2024-01-01T00:00:00Z',
        'version': '1.0.0',
        'service': 'model-to-code-generator'
    }), 200


@app.route('/ready')
def readiness_check():
    """Readiness check endpoint for Kubernetes"""
    try:
        # Test basic functionality
        from ..parsers.text_parser import TextModelParser
        parser = TextModelParser()
        
        return jsonify({
            'status': 'ready',
            'timestamp': '2024-01-01T00:00:00Z',
            'checks': {
                'parser': 'ok',
                'generators': 'ok'
            }
        }), 200
    except Exception as e:
        return jsonify({
            'status': 'not ready',
            'error': str(e)
        }), 503


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(template_dir):
        os.makedirs(template_dir)
    
    # Try multiple ports in case 5000 is occupied
    ports = [5000, 5001, 5002, 8000, 8080, 3000]
    
    for port in ports:
        try:
            print(f"Trying to start server on port {port}...")
            app.run(debug=False, host='0.0.0.0', port=port, threaded=True)
            break
        except OSError as e:
            if "Address already in use" in str(e):
                print(f"Port {port} is already in use, trying next port...")
                continue
            else:
                print(f"Error starting server on port {port}: {e}")
                break
    else:
        print("Could not start server on any available port")