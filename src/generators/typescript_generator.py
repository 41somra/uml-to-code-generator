"""
TypeScript code generator for class models
Generates TypeScript classes from UML class diagrams
"""

from typing import List, Dict, Optional
from ..models.class_model import (
    ClassDiagram, ClassDefinition, Attribute, Method, Parameter, 
    Visibility, Relationship
)


class TypeScriptCodeGenerator:
    """Generates TypeScript code from class models"""
    
    def __init__(self):
        self.type_mapping = {
            'string': 'string',
            'int': 'number',
            'integer': 'number',
            'float': 'number',
            'double': 'number',
            'boolean': 'boolean',
            'bool': 'boolean',
            'date': 'Date',
            'datetime': 'Date',
            'list': 'Array',
            'dict': 'Record<string, any>',
            'object': 'any',
            'void': 'void'
        }
        self.required_imports = set()
    
    def generate(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate TypeScript code for entire diagram"""
        generated_files = {}
        
        # Generate each class
        for class_def in diagram.classes:
            filename = f"{self._to_kebab_case(class_def.name)}.ts"
            code = self.generate_class(class_def, diagram)
            generated_files[filename] = code
        
        # Generate index.ts for barrel exports
        index_code = self._generate_index_file(diagram)
        generated_files["index.ts"] = index_code
        
        return generated_files
    
    def generate_class(self, class_def: ClassDefinition, diagram: ClassDiagram) -> str:
        """Generate TypeScript code for a single class"""
        self.required_imports.clear()
        
        lines = []
        
        # Collect imports
        self._collect_imports(class_def, diagram)
        
        # Add imports
        if self.required_imports:
            for import_stmt in sorted(self.required_imports):
                lines.append(import_stmt)
            lines.append('')
        
        # Generate interfaces first if needed
        if class_def.is_interface:
            interface_code = self._generate_interface(class_def)
            lines.extend(interface_code)
        else:
            # Generate class definition
            class_code = self._generate_class_definition(class_def, diagram)
            lines.extend(class_code)
        
        return '\n'.join(lines)
    
    def _generate_interface(self, class_def: ClassDefinition) -> List[str]:
        """Generate TypeScript interface"""
        lines = []
        
        # Interface comment
        lines.append('/**')
        if class_def.description:
            lines.append(f' * {class_def.description}')
        else:
            lines.append(f' * {class_def.name} interface')
        lines.append(' * Generated from UML model')
        lines.append(' */')
        
        # Interface declaration
        interface_line = f'export interface {class_def.name}'
        
        # Add inheritance
        if class_def.parent_classes or class_def.implemented_interfaces:
            extends = []
            extends.extend(class_def.parent_classes)
            extends.extend(class_def.implemented_interfaces)
            interface_line += f' extends {", ".join(extends)}'
        
        interface_line += ' {'
        lines.append(interface_line)
        
        # Add properties
        for attr in class_def.attributes:
            lines.append(f'  {self._generate_interface_property(attr)}')
        
        # Add method signatures
        for method in class_def.methods:
            lines.append(f'  {self._generate_interface_method(method)}')
        
        lines.append('}')
        
        return lines
    
    def _generate_class_definition(self, class_def: ClassDefinition, diagram: ClassDiagram) -> List[str]:
        """Generate the main class definition"""
        lines = []
        
        # Class comment
        lines.append('/**')
        if class_def.description:
            lines.append(f' * {class_def.description}')
        else:
            lines.append(f' * {class_def.name} class')
        lines.append(' * Generated from UML model')
        lines.append(' */')
        
        # Class declaration
        class_line = 'export '
        
        if class_def.is_abstract:
            class_line += 'abstract '
        
        class_line += f'class {class_def.name}'
        
        # Add inheritance
        if class_def.parent_classes:
            class_line += f' extends {class_def.parent_classes[0]}'
        
        # Add interfaces
        if class_def.implemented_interfaces:
            class_line += f' implements {", ".join(class_def.implemented_interfaces)}'
        
        class_line += ' {'
        lines.append(class_line)
        
        # Generate properties
        for attr in class_def.attributes:
            lines.append(f'  {self._generate_property(attr)}')
        
        if class_def.attributes:
            lines.append('')
        
        # Generate constructor
        constructor_lines = self._generate_constructor(class_def)
        if constructor_lines:
            lines.extend(constructor_lines)
            lines.append('')
        
        # Generate methods
        for method in class_def.methods:
            if method.name != '__init__':  # Skip Python-style constructor
                lines.extend(self._generate_method(method, class_def))
                lines.append('')
        
        # Close class
        lines.append('}')
        
        return lines
    
    def _generate_property(self, attr: Attribute) -> str:
        """Generate a property definition"""
        line = ''
        
        # Visibility (TypeScript uses public by default)
        if attr.visibility == Visibility.PRIVATE:
            line += 'private '
        elif attr.visibility == Visibility.PROTECTED:
            line += 'protected '
        elif attr.visibility == Visibility.PUBLIC:
            line += 'public '
        
        # Modifiers
        if attr.is_static:
            line += 'static '
        if attr.is_final:
            line += 'readonly '
        
        # Property name and type
        ts_type = self._map_type(attr.data_type)
        line += f'{attr.name}: {ts_type}'
        
        # Default value
        if attr.default_value:
            line += f' = {attr.default_value}'
        elif not attr.default_value and ts_type != 'any':
            # Add undefined for optional properties
            line = line.replace(f': {ts_type}', f'?: {ts_type}')
        
        line += ';'
        
        return line
    
    def _generate_interface_property(self, attr: Attribute) -> str:
        """Generate an interface property definition"""
        ts_type = self._map_type(attr.data_type)
        line = f'{attr.name}: {ts_type};'
        return line
    
    def _generate_interface_method(self, method: Method) -> str:
        """Generate an interface method signature"""
        # Parameters
        params = []
        for param in method.parameters:
            param_type = self._map_type(param.data_type)
            param_str = f'{param.name}: {param_type}'
            if param.is_optional:
                param_str = f'{param.name}?: {param_type}'
            if param.default_value:
                param_str += f' = {param.default_value}'
            params.append(param_str)
        
        # Return type
        return_type = self._map_type(method.return_type)
        
        return f'{method.name}({", ".join(params)}): {return_type};'
    
    def _generate_constructor(self, class_def: ClassDefinition) -> List[str]:
        """Generate constructor for the class"""
        lines = []
        
        # Find constructor method or generate from attributes
        constructor_method = None
        for method in class_def.methods:
            if method.name == '__init__':
                constructor_method = method
                break
        
        # Build parameter list
        params = []
        
        if constructor_method and constructor_method.parameters:
            for param in constructor_method.parameters:
                param_type = self._map_type(param.data_type)
                param_str = f'{param.name}: {param_type}'
                if param.default_value:
                    param_str += f' = {param.default_value}'
                elif param.is_optional:
                    param_str = f'{param.name}?: {param_type}'
                params.append(param_str)
        else:
            # Generate parameters from attributes
            for attr in class_def.attributes:
                if not attr.is_static:
                    param_type = self._map_type(attr.data_type)
                    param_str = f'{attr.name}: {param_type}'
                    if attr.default_value:
                        param_str += f' = {attr.default_value}'
                    params.append(param_str)
        
        # Constructor signature
        lines.append('  /**')
        lines.append(f'   * Creates an instance of {class_def.name}')
        for param in (constructor_method.parameters if constructor_method else []):
            lines.append(f'   * @param {param.name} - {param.name} parameter')
        lines.append('   */')
        
        if params:
            lines.append(f'  constructor({", ".join(params)}) {{')
        else:
            lines.append('  constructor() {')
        
        # Initialize properties
        for attr in class_def.attributes:
            if not attr.is_static:
                if constructor_method and any(p.name == attr.name for p in constructor_method.parameters):
                    lines.append(f'    this.{attr.name} = {attr.name};')
                elif attr.default_value:
                    lines.append(f'    this.{attr.name} = {attr.default_value};')
                else:
                    default_val = self._get_default_value(attr.data_type)
                    if default_val != 'undefined':
                        lines.append(f'    this.{attr.name} = {default_val};')
        
        lines.append('  }')
        
        return lines
    
    def _generate_method(self, method: Method, class_def: ClassDefinition) -> List[str]:
        """Generate a method definition"""
        lines = []
        
        # Method comment
        lines.append('  /**')
        if method.description:
            lines.append(f'   * {method.description}')
        else:
            lines.append(f'   * {method.name.replace("_", " ").title()} method')
        
        for param in method.parameters:
            lines.append(f'   * @param {param.name} - {param.name} parameter')
        
        if method.return_type != 'void':
            lines.append(f'   * @returns {self._map_type(method.return_type)}')
        
        lines.append('   */')
        
        # Method signature
        signature = '  '
        
        # Visibility
        if method.visibility == Visibility.PRIVATE:
            signature += 'private '
        elif method.visibility == Visibility.PROTECTED:
            signature += 'protected '
        elif method.visibility == Visibility.PUBLIC:
            signature += 'public '
        
        # Modifiers
        if method.is_static:
            signature += 'static '
        if method.is_abstract:
            signature += 'abstract '
        
        # Method name and parameters
        params = []
        for param in method.parameters:
            param_type = self._map_type(param.data_type)
            param_str = f'{param.name}: {param_type}'
            if param.is_optional:
                param_str = f'{param.name}?: {param_type}'
            if param.default_value:
                param_str += f' = {param.default_value}'
            params.append(param_str)
        
        # Return type
        return_type = self._map_type(method.return_type)
        signature += f'{method.name}({", ".join(params)}): {return_type}'
        
        # Abstract methods don't have body
        if method.is_abstract:
            signature += ';'
            lines.append(signature)
        else:
            signature += ' {'
            lines.append(signature)
            
            # Method body
            if method.body:
                for line in method.body.split('\n'):
                    lines.append(f'    {line}')
            else:
                # Generate basic method body
                if method.name.startswith('get'):
                    attr_name = method.name[3:].lower()
                    # Find matching attribute
                    for attr in class_def.attributes:
                        if attr.name.lower() == attr_name:
                            lines.append(f'    return this.{attr.name};')
                            break
                    else:
                        default_return = self._get_default_value(return_type)
                        if default_return != 'undefined':
                            lines.append(f'    return {default_return};')
                
                elif method.name.startswith('set'):
                    attr_name = method.name[3:].lower()
                    param_name = method.parameters[0].name if method.parameters else 'value'
                    # Find matching attribute
                    for attr in class_def.attributes:
                        if attr.name.lower() == attr_name:
                            lines.append(f'    this.{attr.name} = {param_name};')
                            break
                
                elif return_type != 'void':
                    default_return = self._get_default_value(return_type)
                    if default_return != 'undefined':
                        lines.append(f'    return {default_return};')
                else:
                    lines.append('    // TODO: Implement method')
            
            lines.append('  }')
        
        return lines
    
    def _collect_imports(self, class_def: ClassDefinition, diagram: ClassDiagram):
        """Collect required imports for the class"""
        # Add imports for related classes
        for rel in diagram.get_relationships_for_class(class_def.name):
            if rel.target_class != class_def.name:
                related_class = diagram.get_class_by_name(rel.target_class)
                if related_class:
                    filename = self._to_kebab_case(rel.target_class)
                    self.required_imports.add(f'import {{ {rel.target_class} }} from "./{filename}";')
    
    def _generate_index_file(self, diagram: ClassDiagram) -> str:
        """Generate index.ts for barrel exports"""
        lines = [
            '/**',
            f' * {diagram.name}',
            f' * {diagram.description or "Generated from UML model"}',
            ' */',
            '',
        ]
        
        # Export all classes
        for class_def in diagram.classes:
            filename = self._to_kebab_case(class_def.name)
            lines.append(f'export {{ {class_def.name} }} from "./{filename}";')
        
        return '\n'.join(lines)
    
    def _map_type(self, type_name: str) -> str:
        """Map UML types to TypeScript types"""
        return self.type_mapping.get(type_name.lower(), type_name)
    
    def _get_default_value(self, ts_type: str) -> str:
        """Get default value for a TypeScript type"""
        defaults = {
            'number': '0',
            'string': '""',
            'boolean': 'false',
            'Date': 'new Date()',
            'Array': '[]',
            'Record<string, any>': '{}',
        }
        
        return defaults.get(ts_type, 'undefined')
    
    def _to_kebab_case(self, name: str) -> str:
        """Convert PascalCase to kebab-case"""
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('-')
            result.append(char.lower())
        return ''.join(result)
    
    def _to_camel_case(self, name: str) -> str:
        """Convert snake_case to camelCase"""
        components = name.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])