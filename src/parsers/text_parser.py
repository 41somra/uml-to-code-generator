"""
Text-based parser for UML class diagrams
Supports PlantUML, simple text format, and YAML definitions
"""

import re
import yaml
from typing import Dict, List, Optional
from ..models.class_model import (
    ClassDiagram, ClassDefinition, Attribute, Method, Parameter, 
    Relationship, Visibility, DataType
)


class TextModelParser:
    """Parser for text-based model definitions"""
    
    def __init__(self):
        self.visibility_map = {
            '+': Visibility.PUBLIC,
            '-': Visibility.PRIVATE,
            '#': Visibility.PROTECTED,
            '~': Visibility.PACKAGE
        }
    
    def parse_plantuml(self, plantuml_text: str) -> ClassDiagram:
        """Parse PlantUML class diagram syntax"""
        lines = [line.strip() for line in plantuml_text.split('\n') if line.strip()]
        
        diagram = ClassDiagram(name="Parsed Diagram")
        current_class = None
        
        for line in lines:
            # Skip PlantUML directives
            if line.startswith('@') or line.startswith('!'):
                continue
            
            # Class definition
            if line.startswith('class '):
                class_name = self._extract_class_name(line)
                current_class = ClassDefinition(name=class_name)
                diagram.classes.append(current_class)
            
            # Interface definition
            elif line.startswith('interface '):
                interface_name = self._extract_class_name(line)
                current_class = ClassDefinition(name=interface_name, is_interface=True)
                diagram.classes.append(current_class)
            
            # Abstract class
            elif line.startswith('abstract class '):
                class_name = self._extract_class_name(line)
                current_class = ClassDefinition(name=class_name, is_abstract=True)
                diagram.classes.append(current_class)
            
            # Class members (attributes and methods)
            elif current_class and (line.startswith('+') or line.startswith('-') or 
                                  line.startswith('#') or line.startswith('~')):
                self._parse_class_member(line, current_class)
            
            # Relationships
            elif '-->' in line or '<--' in line or '--|>' in line or '<|--' in line:
                relationship = self._parse_relationship(line)
                if relationship:
                    diagram.relationships.append(relationship)
            
            # End class definition
            elif line == '}' and current_class:
                current_class = None
        
        return diagram
    
    def parse_yaml(self, yaml_text: str) -> ClassDiagram:
        """Parse YAML-based model definition"""
        try:
            data = yaml.safe_load(yaml_text)
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML format: {e}")
        
        diagram = ClassDiagram(
            name=data.get('name', 'YAML Diagram'),
            description=data.get('description')
        )
        
        # Parse classes
        for class_data in data.get('classes', []):
            class_def = self._parse_yaml_class(class_data)
            diagram.classes.append(class_def)
        
        # Parse relationships
        for rel_data in data.get('relationships', []):
            relationship = self._parse_yaml_relationship(rel_data)
            diagram.relationships.append(relationship)
        
        return diagram
    
    def parse_simple_text(self, text: str) -> ClassDiagram:
        """Parse simple text format for quick prototyping"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        diagram = ClassDiagram(name="Simple Text Diagram")
        current_class = None
        
        for line in lines:
            # Class definition
            if line.endswith(':'):
                class_name = line[:-1].strip()
                current_class = ClassDefinition(name=class_name)
                diagram.classes.append(current_class)
            
            # Attributes and methods
            elif current_class and line.startswith('  '):
                member = line.strip()
                if '(' in member and ')' in member:
                    # Method
                    method = self._parse_simple_method(member)
                    current_class.methods.append(method)
                else:
                    # Attribute
                    attr = self._parse_simple_attribute(member)
                    current_class.attributes.append(attr)
        
        return diagram
    
    def _extract_class_name(self, line: str) -> str:
        """Extract class name from PlantUML class definition"""
        match = re.search(r'(?:class|interface|abstract class)\s+(\w+)', line)
        return match.group(1) if match else "Unknown"
    
    def _parse_class_member(self, line: str, class_def: ClassDefinition):
        """Parse a class member (attribute or method) from PlantUML"""
        visibility_char = line[0]
        visibility = self.visibility_map.get(visibility_char, Visibility.PUBLIC)
        member_text = line[1:].strip()
        
        if '(' in member_text and ')' in member_text:
            # Method
            method = self._parse_plantuml_method(member_text, visibility)
            class_def.methods.append(method)
        else:
            # Attribute
            attr = self._parse_plantuml_attribute(member_text, visibility)
            class_def.attributes.append(attr)
    
    def _parse_plantuml_method(self, method_text: str, visibility: Visibility) -> Method:
        """Parse PlantUML method definition"""
        # Extract method name and parameters
        match = re.match(r'(\w+)\s*\(([^)]*)\)\s*:?\s*(\w+)?', method_text)
        
        if not match:
            return Method(name=method_text, visibility=visibility)
        
        method_name = match.group(1)
        params_text = match.group(2) or ""
        return_type = match.group(3) or "void"
        
        # Parse parameters
        parameters = []
        if params_text.strip():
            for param in params_text.split(','):
                param = param.strip()
                if ':' in param:
                    param_name, param_type = param.split(':', 1)
                    parameters.append(Parameter(
                        name=param_name.strip(),
                        data_type=param_type.strip()
                    ))
                else:
                    parameters.append(Parameter(name=param, data_type="object"))
        
        return Method(
            name=method_name,
            return_type=return_type,
            visibility=visibility,
            parameters=parameters
        )
    
    def _parse_plantuml_attribute(self, attr_text: str, visibility: Visibility) -> Attribute:
        """Parse PlantUML attribute definition"""
        if ':' in attr_text:
            attr_name, attr_type = attr_text.split(':', 1)
            return Attribute(
                name=attr_name.strip(),
                data_type=attr_type.strip(),
                visibility=visibility
            )
        else:
            return Attribute(
                name=attr_text.strip(),
                data_type="object",
                visibility=visibility
            )
    
    def _parse_relationship(self, line: str) -> Optional[Relationship]:
        """Parse relationship from PlantUML syntax"""
        # Simple relationship parsing
        if '-->' in line:
            parts = line.split('-->')
            return Relationship(
                source_class=parts[0].strip(),
                target_class=parts[1].strip(),
                relationship_type="association"
            )
        elif '<|--' in line:
            parts = line.split('<|--')
            return Relationship(
                source_class=parts[1].strip(),
                target_class=parts[0].strip(),
                relationship_type="inheritance"
            )
        
        return None
    
    def _parse_yaml_class(self, class_data: Dict) -> ClassDefinition:
        """Parse class definition from YAML"""
        class_def = ClassDefinition(
            name=class_data['name'],
            package=class_data.get('package'),
            is_abstract=class_data.get('abstract', False),
            is_interface=class_data.get('interface', False),
            description=class_data.get('description')
        )
        
        # Parse attributes
        for attr_data in class_data.get('attributes', []):
            attr = Attribute(
                name=attr_data['name'],
                data_type=attr_data['type'],
                visibility=Visibility(attr_data.get('visibility', 'private')),
                default_value=attr_data.get('default')
            )
            class_def.attributes.append(attr)
        
        # Parse methods
        for method_data in class_data.get('methods', []):
            parameters = []
            for param_data in method_data.get('parameters', []):
                param = Parameter(
                    name=param_data['name'],
                    data_type=param_data['type'],
                    default_value=param_data.get('default'),
                    is_optional=param_data.get('optional', False)
                )
                parameters.append(param)
            
            method = Method(
                name=method_data['name'],
                return_type=method_data.get('return_type', 'void'),
                visibility=Visibility(method_data.get('visibility', 'public')),
                is_static=method_data.get('static', False),
                is_abstract=method_data.get('abstract', False),
                parameters=parameters
            )
            class_def.methods.append(method)
        
        return class_def
    
    def _parse_yaml_relationship(self, rel_data: Dict) -> Relationship:
        """Parse relationship from YAML"""
        return Relationship(
            source_class=rel_data['from'],
            target_class=rel_data['to'],
            relationship_type=rel_data['type'],
            multiplicity_source=rel_data.get('multiplicity_from'),
            multiplicity_target=rel_data.get('multiplicity_to'),
            label=rel_data.get('label')
        )
    
    def _parse_simple_method(self, method_text: str) -> Method:
        """Parse method from simple text format"""
        if '(' in method_text:
            method_name = method_text.split('(')[0].strip()
            return Method(name=method_name)
        else:
            return Method(name=method_text.strip())
    
    def _parse_simple_attribute(self, attr_text: str) -> Attribute:
        """Parse attribute from simple text format"""
        if ':' in attr_text:
            attr_name, attr_type = attr_text.split(':', 1)
            return Attribute(
                name=attr_name.strip(),
                data_type=attr_type.strip()
            )
        else:
            return Attribute(name=attr_text.strip(), data_type="object")


# Example usage and test data
SAMPLE_PLANTUML = """
@startuml
class User {
    - id: int
    - username: string
    - email: string
    + getId(): int
    + setUsername(name: string): void
    + validateEmail(): boolean
}

class Order {
    - id: int
    - userId: int
    - total: float
    + calculateTotal(): float
    + getUser(): User
}

interface PaymentProcessor {
    + processPayment(amount: float): boolean
    + refund(transactionId: string): boolean
}

User ||--o{ Order
Order --> PaymentProcessor
@enduml
"""

SAMPLE_YAML = """
name: "E-commerce System"
description: "Basic e-commerce domain model"

classes:
  - name: User
    package: entities
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
          - name: username
            type: string

  - name: Order
    package: entities
    attributes:
      - name: id
        type: int
        visibility: private
      - name: userId
        type: int
        visibility: private
    methods:
      - name: calculateTotal
        return_type: float
        visibility: public

relationships:
  - from: Order
    to: User
    type: association
    multiplicity_from: many
    multiplicity_to: one
"""

SAMPLE_SIMPLE_TEXT = """
User:
  id: int
  username: string
  email: string
  getId()
  setUsername(name)
  validateEmail()

Order:
  id: int
  userId: int
  total: float
  calculateTotal()
  getUser()

PaymentProcessor:
  processPayment(amount)
  refund(transactionId)
"""