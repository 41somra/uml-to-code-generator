#!/usr/bin/env python3
"""
Model-to-Code Generator - Main CLI Application
Converts UML class diagrams to source code in multiple languages
"""

import argparse
import sys
import os
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.parsers.text_parser import TextModelParser
from src.generators.python_generator import PythonCodeGenerator
from src.generators.java_generator import JavaCodeGenerator  
from src.generators.typescript_generator import TypeScriptCodeGenerator
from src.generators.microservice_generator import MicroserviceGenerator
from src.generators.openapi_generator import OpenAPIGenerator
from src.generators.devsecops_generator import DevSecOpsGenerator
from src.models.class_model import create_sample_model


def main():
    parser = argparse.ArgumentParser(
        description='Model-to-Code Generator - Convert UML to source code',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s -i model.txt -o output/ -l python
  %(prog)s -i model.puml -f plantuml -l java -o generated/
  %(prog)s --sample -l typescript -o examples/
  %(prog)s --web  # Start web interface
        '''
    )
    
    # Input options
    parser.add_argument('-i', '--input', 
                       help='Input model file path')
    parser.add_argument('-f', '--format', 
                       choices=['simple', 'plantuml', 'yaml'],
                       default='simple',
                       help='Input model format (default: simple)')
    
    # Output options
    parser.add_argument('-o', '--output',
                       default='generated/',
                       help='Output directory (default: generated/)')
    parser.add_argument('-l', '--language',
                       choices=['python', 'java', 'typescript', 'microservices', 'openapi', 'devsecops'],
                       default='python',
                       help='Target programming language or architecture (default: python)')
    
    # Special modes
    parser.add_argument('--sample',
                       action='store_true',
                       help='Generate code from sample model')
    parser.add_argument('--web',
                       action='store_true',
                       help='Start web interface')
    parser.add_argument('--validate-only',
                       action='store_true',
                       help='Only validate the model, don\'t generate code')
    
    # Options
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Verbose output')
    parser.add_argument('--force',
                       action='store_true',
                       help='Overwrite existing files')
    
    args = parser.parse_args()
    
    # Handle special modes
    if args.web:
        start_web_interface()
        return
    
    if args.sample:
        generate_sample_code(args)
        return
    
    # Validate input
    if not args.input:
        parser.error('Input file is required (use -i/--input or --sample)')
    
    if not os.path.exists(args.input):
        print(f"Error: Input file '{args.input}' not found", file=sys.stderr)
        sys.exit(1)
    
    try:
        # Read input file
        with open(args.input, 'r', encoding='utf-8') as f:
            model_text = f.read()
        
        if args.verbose:
            print(f"Reading model from: {args.input}")
            print(f"Model format: {args.format}")
            print(f"Target language: {args.language}")
            print(f"Output directory: {args.output}")
        
        # Parse the model
        parser_instance = TextModelParser()
        
        if args.format == 'plantuml':
            diagram = parser_instance.parse_plantuml(model_text)
        elif args.format == 'yaml':
            diagram = parser_instance.parse_yaml(model_text)
        else:
            diagram = parser_instance.parse_simple_text(model_text)
        
        if args.verbose:
            print(f"Parsed diagram: {diagram.name}")
            print(f"Classes: {len(diagram.classes)}")
            print(f"Relationships: {len(diagram.relationships)}")
        
        # Validate only mode
        if args.validate_only:
            print("✅ Model is valid")
            print(f"Diagram: {diagram.name}")
            print(f"Classes: {len(diagram.classes)}")
            for cls in diagram.classes:
                print(f"  - {cls.name} ({len(cls.attributes)} attributes, {len(cls.methods)} methods)")
            print(f"Relationships: {len(diagram.relationships)}")
            return
        
        # Generate code
        generators = {
            'python': PythonCodeGenerator(),
            'java': JavaCodeGenerator(),
            'typescript': TypeScriptCodeGenerator(),
            'microservices': MicroserviceGenerator(),
            'openapi': OpenAPIGenerator(),
            'devsecops': DevSecOpsGenerator()
        }
        
        generator = generators[args.language]
        generated_files = generator.generate(diagram)
        
        # Create output directory
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Write generated files
        files_written = 0
        for filename, content in generated_files.items():
            output_path = output_dir / filename
            
            if output_path.exists() and not args.force:
                print(f"Warning: {output_path} already exists (use --force to overwrite)")
                continue
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            files_written += 1
            if args.verbose:
                print(f"Generated: {output_path}")
        
        print(f"✅ Successfully generated {files_written} files in {output_dir}")
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


def generate_sample_code(args):
    """Generate code from sample model"""
    if args.verbose:
        print("Generating sample model...")
    
    # Create sample diagram
    diagram = create_sample_model()
    
    # Generate code
    generators = {
        'python': PythonCodeGenerator(),
        'java': JavaCodeGenerator(),
        'typescript': TypeScriptCodeGenerator(),
        'microservices': MicroserviceGenerator(),
        'openapi': OpenAPIGenerator(),
        'devsecops': DevSecOpsGenerator()
    }
    
    generator = generators[args.language]
    generated_files = generator.generate(diagram)
    
    # Create output directory
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Write generated files
    files_written = 0
    for filename, content in generated_files.items():
        output_path = output_dir / filename
        
        if output_path.exists() and not args.force:
            print(f"Warning: {output_path} already exists (use --force to overwrite)")
            continue
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        files_written += 1
        if args.verbose:
            print(f"Generated: {output_path}")
    
    print(f"✅ Successfully generated {files_written} sample files in {output_dir}")


def start_web_interface():
    """Start the web interface"""
    print("Starting Air Force Model-to-Code Generator web interface...")
    
    try:
        from src.web.app import app
        
        # Try multiple ports in case 5000 is occupied
        ports = [5000, 5001, 5002, 8000, 8080]
        
        for port in ports:
            try:
                print(f"Trying to start server on http://localhost:{port}")
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
            print("Try disabling AirPlay Receiver in System Preferences > General > AirDrop & Handoff")
            
    except ImportError as e:
        print(f"Error: Failed to start web interface: {e}")
        print("Make sure Flask is installed: pip install flask")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down web interface...")


if __name__ == '__main__':
    main()