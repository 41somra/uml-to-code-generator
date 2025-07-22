"""
Java code generator for class models
Generates Java classes from UML class diagrams
"""

from typing import List, Dict, Optional
from ..models.class_model import (
    ClassDiagram, ClassDefinition, Attribute, Method, Parameter, 
    Visibility, Relationship
)


class JavaCodeGenerator:
    """Generates Java code from class models"""
    
    def __init__(self):
        self.type_mapping = {
            'string': 'String',
            'int': 'int',
            'integer': 'int',
            'float': 'float',
            'double': 'double',
            'boolean': 'boolean',
            'bool': 'boolean',
            'date': 'LocalDate',
            'datetime': 'LocalDateTime',
            'list': 'List',
            'dict': 'Map',
            'object': 'Object',
            'void': 'void'
        }
        self.required_imports = set()
    
    def generate(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate Java code for entire diagram"""
        generated_files = {}
        
        # Generate each class
        for class_def in diagram.classes:
            filename = f"{class_def.name}.java"
            code = self.generate_class(class_def, diagram)
            generated_files[filename] = code
        
        return generated_files
    
    def generate_class(self, class_def: ClassDefinition, diagram: ClassDiagram) -> str:
        """Generate Java code for a single class"""
        self.required_imports.clear()
        
        lines = []
        
        # Collect imports
        self._collect_imports(class_def, diagram)
        
        # Add package declaration
        if class_def.package:
            lines.append(f'package {class_def.package};')
            lines.append('')
        
        # Add imports
        if self.required_imports:
            for import_stmt in sorted(self.required_imports):
                lines.append(import_stmt)
            lines.append('')
        
        # Add class javadoc
        lines.append('/**')
        if class_def.description:
            lines.append(f' * {class_def.description}')
        else:
            lines.append(f' * {class_def.name} class')
        lines.append(' * Generated from UML model')
        lines.append(' */')
        
        # Generate class definition
        class_code = self._generate_class_definition(class_def, diagram)
        lines.extend(class_code)
        
        return '\n'.join(lines)
    
    def _generate_class_definition(self, class_def: ClassDefinition, diagram: ClassDiagram) -> List[str]:
        """Generate the main class definition"""
        lines = []
        
        # Class modifiers and declaration
        class_line = 'public '
        
        if class_def.is_abstract:
            class_line += 'abstract '
        
        if class_def.is_interface:
            class_line += f'interface {class_def.name}'
        else:
            class_line += f'class {class_def.name}'
        
        # Add inheritance
        if class_def.parent_classes and not class_def.is_interface:
            class_line += f' extends {class_def.parent_classes[0]}'
        
        # Add interfaces
        if class_def.implemented_interfaces:
            if class_def.is_interface:
                class_line += f' extends {", ".join(class_def.implemented_interfaces)}'
            else:
                class_line += f' implements {", ".join(class_def.implemented_interfaces)}'
        
        class_line += ' {'
        lines.append(class_line)
        lines.append('')
        
        # Generate attributes
        for attr in class_def.attributes:
            lines.append(f'    {self._generate_attribute(attr)}')
        
        if class_def.attributes:
            lines.append('')
        
        # Generate constructors
        if not class_def.is_interface:
            constructor_lines = self._generate_constructors(class_def)
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
    
    def _generate_attribute(self, attr: Attribute) -> str:
        """Generate an attribute definition"""
        line = '    '
        
        # Visibility
        if attr.visibility == Visibility.PUBLIC:
            line += 'public '
        elif attr.visibility == Visibility.PRIVATE:
            line += 'private '
        elif attr.visibility == Visibility.PROTECTED:
            line += 'protected '
        
        # Modifiers
        if attr.is_static:
            line += 'static '
        if attr.is_final:
            line += 'final '
        
        # Type and name
        java_type = self._map_type(attr.data_type)
        line += f'{java_type} {attr.name}'
        
        # Default value
        if attr.default_value:
            line += f' = {attr.default_value}'
        elif attr.is_final:
            # Final fields need initialization
            default_val = self._get_default_value(java_type)
            line += f' = {default_val}'
        
        line += ';'
        
        return line
    
    def _generate_constructors(self, class_def: ClassDefinition) -> List[str]:
        """Generate constructors for the class"""
        lines = []
        
        # Default constructor
        lines.append('    /**')
        lines.append(f'     * Default constructor for {class_def.name}')
        lines.append('     */')
        lines.append(f'    public {class_def.name}() {{')
        
        # Initialize attributes with defaults
        for attr in class_def.attributes:
            if not attr.is_static and attr.default_value:
                lines.append(f'        this.{attr.name} = {attr.default_value};')
        
        lines.append('    }')
        lines.append('')
        
        # Parameterized constructor (if there are non-static attributes)
        non_static_attrs = [attr for attr in class_def.attributes if not attr.is_static]
        if non_static_attrs:
            lines.append('    /**')
            lines.append(f'     * Parameterized constructor for {class_def.name}')
            for attr in non_static_attrs:
                lines.append(f'     * @param {attr.name} the {attr.name} value')
            lines.append('     */')
            
            # Constructor signature
            params = []
            for attr in non_static_attrs:
                java_type = self._map_type(attr.data_type)
                params.append(f'{java_type} {attr.name}')
            
            lines.append(f'    public {class_def.name}({", ".join(params)}) {{')
            
            # Initialize attributes
            for attr in non_static_attrs:
                lines.append(f'        this.{attr.name} = {attr.name};')
            
            lines.append('    }')
        
        return lines
    
    def _generate_method(self, method: Method, class_def: ClassDefinition) -> List[str]:
        """Generate a method definition"""
        lines = []
        
        # Method javadoc
        lines.append('    /**')
        if method.description:
            lines.append(f'     * {method.description}')
        else:
            lines.append(f'     * {method.name.replace("_", " ").title()} method')
        
        for param in method.parameters:
            lines.append(f'     * @param {param.name} the {param.name} parameter')
        
        if method.return_type != 'void':
            lines.append(f'     * @return {self._map_type(method.return_type)}')
        
        lines.append('     */')
        
        # Method signature
        signature = '    '
        
        # Visibility
        if method.visibility == Visibility.PUBLIC:
            signature += 'public '
        elif method.visibility == Visibility.PRIVATE:
            signature += 'private '
        elif method.visibility == Visibility.PROTECTED:
            signature += 'protected '
        
        # Modifiers
        if method.is_static:
            signature += 'static '
        if method.is_abstract:
            signature += 'abstract '
        elif method.is_final:
            signature += 'final '
        
        # Return type
        return_type = self._map_type(method.return_type)
        signature += f'{return_type} '
        
        # Method name and parameters
        params = []
        for param in method.parameters:
            param_type = self._map_type(param.data_type)
            param_str = f'{param_type} {param.name}'
            params.append(param_str)
        
        signature += f'{method.name}({", ".join(params)})'
        
        # Abstract methods or interface methods don't have body
        if method.is_abstract or class_def.is_interface:
            signature += ';'
            lines.append(signature)
        else:
            signature += ' {'
            lines.append(signature)
            
            # Method body
            if method.body:
                for line in method.body.split('\n'):
                    lines.append(f'        {line}')
            else:
                # Generate basic method body based on method name
                if method.name.startswith('get'):
                    attr_name = method.name[3:].lower()
                    # Find matching attribute
                    matching_attr = None
                    for attr in class_def.attributes:
                        if attr.name.lower() == attr_name:
                            matching_attr = attr
                            break
                    
                    if matching_attr:
                        lines.append(f'        return this.{matching_attr.name};')
                    else:
                        default_return = self._get_default_value(return_type)
                        lines.append(f'        return {default_return};')
                
                elif method.name.startswith('set'):
                    attr_name = method.name[3:].lower()
                    param_name = method.parameters[0].name if method.parameters else 'value'
                    # Find matching attribute
                    for attr in class_def.attributes:
                        if attr.name.lower() == attr_name:
                            lines.append(f'        this.{attr.name} = {param_name};')
                            break
                
                elif return_type == 'void':
                    lines.append('        // TODO: Implement method')
                
                else:
                    default_return = self._get_default_value(return_type)
                    lines.append(f'        return {default_return};')
            
            lines.append('    }')
        
        return lines
    
    def _collect_imports(self, class_def: ClassDefinition, diagram: ClassDiagram):
        """Collect required imports for the class"""
        all_types = set()
        
        # Collect types from attributes
        for attr in class_def.attributes:
            all_types.add(attr.data_type)
        
        # Collect types from methods
        for method in class_def.methods:
            all_types.add(method.return_type)
            for param in method.parameters:
                all_types.add(param.data_type)
        
        # Add required imports based on types
        for type_name in all_types:
            java_type = self._map_type(type_name)
            
            if java_type == 'LocalDate':
                self.required_imports.add('import java.time.LocalDate;')
            elif java_type == 'LocalDateTime':
                self.required_imports.add('import java.time.LocalDateTime;')
            elif java_type == 'List':
                self.required_imports.add('import java.util.List;')
                self.required_imports.add('import java.util.ArrayList;')
            elif java_type == 'Map':
                self.required_imports.add('import java.util.Map;')
                self.required_imports.add('import java.util.HashMap;')
    
    def _map_type(self, type_name: str) -> str:
        """Map UML types to Java types"""
        return self.type_mapping.get(type_name.lower(), type_name)
    
    def _get_default_value(self, java_type: str) -> str:
        """Get default value for a Java type"""
        defaults = {
            'int': '0',
            'float': '0.0f',
            'double': '0.0',
            'boolean': 'false',
            'String': '""',
            'List': 'new ArrayList<>()',
            'Map': 'new HashMap<>()',
            'LocalDate': 'LocalDate.now()',
            'LocalDateTime': 'LocalDateTime.now()',
        }
        
        return defaults.get(java_type, 'null')
    
    def _to_camel_case(self, name: str) -> str:
        """Convert snake_case to camelCase"""
        components = name.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    def _to_pascal_case(self, name: str) -> str:
        """Convert snake_case to PascalCase"""
        return ''.join(x.title() for x in name.split('_'))