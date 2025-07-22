"""
Python code generator for class models
Generates Python classes from UML class diagrams
"""

from typing import List, Dict, Optional
from ..models.class_model import (
    ClassDiagram, ClassDefinition, Attribute, Method, Parameter, 
    Visibility, Relationship
)


class PythonCodeGenerator:
    """Generates Python code from class models"""
    
    def __init__(self):
        self.type_mapping = {
            'string': 'str',
            'int': 'int',
            'integer': 'int',
            'float': 'float',
            'double': 'float',
            'boolean': 'bool',
            'bool': 'bool',
            'date': 'datetime.date',
            'datetime': 'datetime.datetime',
            'list': 'List',
            'dict': 'Dict',
            'object': 'Any',
            'void': 'None'
        }
        self.required_imports = set()
    
    def generate(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate Python code for entire diagram"""
        self.required_imports.clear()
        generated_files = {}
        
        # Generate each class
        for class_def in diagram.classes:
            filename = f"{self._to_snake_case(class_def.name)}.py"
            code = self.generate_class(class_def, diagram)
            generated_files[filename] = code
        
        # Generate __init__.py for package
        if diagram.packages:
            init_code = self._generate_package_init(diagram)
            generated_files["__init__.py"] = init_code
        
        return generated_files
    
    def generate_class(self, class_def: ClassDefinition, diagram: ClassDiagram) -> str:
        """Generate Python code for a single class"""
        self.required_imports.clear()
        
        lines = []
        
        # Add file header
        lines.append(f'"""')
        lines.append(f'{class_def.name} class')
        if class_def.description:
            lines.append(f'{class_def.description}')
        lines.append(f'Generated from UML model')
        lines.append(f'"""')
        lines.append('')
        
        # Collect imports
        self._collect_imports(class_def, diagram)
        
        # Add imports
        if self.required_imports:
            for import_stmt in sorted(self.required_imports):
                lines.append(import_stmt)
            lines.append('')
        
        # Generate class definition
        class_code = self._generate_class_definition(class_def, diagram)
        lines.extend(class_code)
        
        return '\n'.join(lines)
    
    def _generate_class_definition(self, class_def: ClassDefinition, diagram: ClassDiagram) -> List[str]:
        """Generate the main class definition"""
        lines = []
        
        # Class declaration
        class_line = f'class {class_def.name}'
        
        # Add inheritance
        parent_classes = []
        if class_def.parent_classes:
            parent_classes.extend(class_def.parent_classes)
        if class_def.implemented_interfaces:
            parent_classes.extend(class_def.implemented_interfaces)
        
        if parent_classes:
            class_line += f'({", ".join(parent_classes)})'
        
        class_line += ':'
        lines.append(class_line)
        
        # Class docstring
        if class_def.description or class_def.is_abstract or class_def.is_interface:
            lines.append('    """')
            if class_def.description:
                lines.append(f'    {class_def.description}')
            if class_def.is_abstract:
                lines.append('    Abstract class')
            if class_def.is_interface:
                lines.append('    Interface definition')
            lines.append('    """')
            lines.append('')
        
        # Add class attributes (class variables)
        static_attributes = [attr for attr in class_def.attributes if attr.is_static]
        if static_attributes:
            for attr in static_attributes:
                lines.append(f'    {self._generate_attribute(attr, is_static=True)}')
            lines.append('')
        
        # Generate constructor
        constructor = self._find_constructor(class_def)
        if constructor or class_def.attributes:
            lines.extend(self._generate_constructor(class_def, constructor))
            lines.append('')
        
        # Generate methods
        regular_methods = [m for m in class_def.methods if m.name != '__init__']
        for method in regular_methods:
            lines.extend(self._generate_method(method, class_def))
            lines.append('')
        
        # Generate properties for private attributes
        private_attributes = [attr for attr in class_def.attributes if not attr.is_static]
        if private_attributes:
            lines.extend(self._generate_properties(private_attributes))
        
        # If class is empty, add pass
        if len(lines) == 1:
            lines.append('    pass')
        
        return lines
    
    def _generate_constructor(self, class_def: ClassDefinition, constructor: Optional[Method]) -> List[str]:
        """Generate constructor method"""
        lines = []
        
        # Build parameter list
        params = ['self']
        
        if constructor and constructor.parameters:
            for param in constructor.parameters:
                param_type = self._map_type(param.data_type)
                param_str = f'{param.name}: {param_type}'
                if param.default_value:
                    param_str += f' = {param.default_value}'
                elif param.is_optional:
                    param_str += ' = None'
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
        if len(params) == 1:
            lines.append('    def __init__(self):')
        else:
            lines.append(f'    def __init__({", ".join(params)}):')
        
        # Constructor docstring
        lines.append('        """Initialize the class instance"""')
        
        # Initialize attributes
        for attr in class_def.attributes:
            if not attr.is_static:
                if constructor and any(p.name == attr.name for p in constructor.parameters):
                    lines.append(f'        self._{attr.name} = {attr.name}')
                elif attr.default_value:
                    lines.append(f'        self._{attr.name} = {attr.default_value}')
                else:
                    default_val = self._get_default_value(attr.data_type)
                    lines.append(f'        self._{attr.name} = {default_val}')
        
        # If no attributes, add pass
        if not any(not attr.is_static for attr in class_def.attributes):
            lines.append('        pass')
        
        return lines
    
    def _generate_method(self, method: Method, class_def: ClassDefinition) -> List[str]:
        """Generate a method definition"""
        lines = []
        
        # Method signature
        params = ['self'] if not method.is_static else []
        
        for param in method.parameters:
            param_type = self._map_type(param.data_type)
            param_str = f'{param.name}: {param_type}'
            if param.default_value:
                param_str += f' = {param.default_value}'
            elif param.is_optional:
                param_str += ' = None'
            params.append(param_str)
        
        # Return type annotation
        return_type = self._map_type(method.return_type)
        
        # Method decorator
        if method.is_static:
            lines.append('    @staticmethod')
        elif method.is_abstract:
            lines.append('    @abstractmethod')
        
        # Method signature
        signature = f'    def {method.name}({", ".join(params)})'
        if return_type != 'None':
            signature += f' -> {return_type}'
        signature += ':'
        lines.append(signature)
        
        # Method docstring
        lines.append('        """')
        if method.description:
            lines.append(f'        {method.description}')
        else:
            lines.append(f'        {method.name.replace("_", " ").title()} method')
        lines.append('        """')
        
        # Method body
        if method.body:
            for line in method.body.split('\n'):
                lines.append(f'        {line}')
        elif method.is_abstract:
            lines.append('        pass')
        elif class_def.is_interface:
            lines.append('        raise NotImplementedError')
        else:
            # Generate basic method body based on method name
            if method.name.startswith('get_'):
                attr_name = method.name[4:]
                lines.append(f'        return self._{attr_name}')
            elif method.name.startswith('set_'):
                attr_name = method.name[4:]
                param_name = method.parameters[0].name if method.parameters else 'value'
                lines.append(f'        self._{attr_name} = {param_name}')
            elif method.return_type == 'void' or method.return_type == 'None':
                lines.append('        pass')
            else:
                default_return = self._get_default_value(method.return_type)
                lines.append(f'        return {default_return}')
        
        return lines
    
    def _generate_properties(self, attributes: List[Attribute]) -> List[str]:
        """Generate property decorators for private attributes"""
        lines = []
        
        for attr in attributes:
            if attr.visibility == Visibility.PRIVATE:
                # Getter property
                lines.append('')
                lines.append('    @property')
                lines.append(f'    def {attr.name}(self) -> {self._map_type(attr.data_type)}:')
                lines.append(f'        """Get {attr.name}"""')
                lines.append(f'        return self._{attr.name}')
                
                # Setter property
                lines.append('')
                lines.append(f'    @{attr.name}.setter')
                lines.append(f'    def {attr.name}(self, value: {self._map_type(attr.data_type)}):')
                lines.append(f'        """Set {attr.name}"""')
                lines.append(f'        self._{attr.name} = value')
        
        return lines
    
    def _generate_attribute(self, attr: Attribute, is_static: bool = False) -> str:
        """Generate an attribute definition"""
        if attr.default_value:
            return f'{attr.name}: {self._map_type(attr.data_type)} = {attr.default_value}'
        else:
            default_val = self._get_default_value(attr.data_type)
            return f'{attr.name}: {self._map_type(attr.data_type)} = {default_val}'
    
    def _find_constructor(self, class_def: ClassDefinition) -> Optional[Method]:
        """Find the constructor method"""
        for method in class_def.methods:
            if method.name == '__init__':
                return method
        return None
    
    def _collect_imports(self, class_def: ClassDefinition, diagram: ClassDiagram):
        """Collect required imports for the class"""
        # Check for typing imports
        all_types = set()
        
        # Collect types from attributes
        for attr in class_def.attributes:
            all_types.add(attr.data_type)
        
        # Collect types from methods
        for method in class_def.methods:
            all_types.add(method.return_type)
            for param in method.parameters:
                all_types.add(param.data_type)
        
        # Add required imports
        if any('List' in t or 'Dict' in t or 'Any' in t or 'Optional' in t for t in all_types):
            self.required_imports.add('from typing import List, Dict, Any, Optional')
        
        if any('datetime' in t for t in all_types):
            self.required_imports.add('import datetime')
        
        if any(method.is_abstract for method in class_def.methods):
            self.required_imports.add('from abc import ABC, abstractmethod')
        
        # Add imports for related classes
        for rel in diagram.get_relationships_for_class(class_def.name):
            if rel.target_class != class_def.name:
                # Add import for related class
                related_class = diagram.get_class_by_name(rel.target_class)
                if related_class and related_class.package:
                    self.required_imports.add(f'from .{self._to_snake_case(rel.target_class)} import {rel.target_class}')
    
    def _generate_package_init(self, diagram: ClassDiagram) -> str:
        """Generate __init__.py for the package"""
        lines = [
            f'"""',
            f'{diagram.name}',
            f'',
            f'{diagram.description or "Generated from UML model"}',
            f'"""',
            f'',
        ]
        
        # Import all classes
        for class_def in diagram.classes:
            module_name = self._to_snake_case(class_def.name)
            lines.append(f'from .{module_name} import {class_def.name}')
        
        lines.append('')
        lines.append('__all__ = [')
        for class_def in diagram.classes:
            lines.append(f'    "{class_def.name}",')
        lines.append(']')
        
        return '\n'.join(lines)
    
    def _map_type(self, type_name: str) -> str:
        """Map UML types to Python types"""
        return self.type_mapping.get(type_name.lower(), type_name)
    
    def _get_default_value(self, type_name: str) -> str:
        """Get default value for a type"""
        python_type = self._map_type(type_name)
        
        defaults = {
            'str': '""',
            'int': '0',
            'float': '0.0',
            'bool': 'False',
            'List': '[]',
            'Dict': '{}',
            'datetime.date': 'datetime.date.today()',
            'datetime.datetime': 'datetime.datetime.now()',
        }
        
        return defaults.get(python_type, 'None')
    
    def _to_snake_case(self, name: str) -> str:
        """Convert PascalCase to snake_case"""
        result = []
        for i, char in enumerate(name):
            if char.isupper() and i > 0:
                result.append('_')
            result.append(char.lower())
        return ''.join(result)