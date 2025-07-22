"""
Class model definitions for the Model-to-Code generator
Represents UML class diagrams as Python objects
"""

from typing import List, Dict, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class Visibility(Enum):
    """Visibility levels for class members"""
    PUBLIC = "public"
    PRIVATE = "private"
    PROTECTED = "protected"
    PACKAGE = "package"


class DataType(Enum):
    """Common data types"""
    STRING = "string"
    INTEGER = "int"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"
    LIST = "list"
    DICT = "dict"
    OBJECT = "object"
    VOID = "void"


@dataclass
class Parameter:
    """Represents a method parameter"""
    name: str
    data_type: str
    default_value: Optional[str] = None
    is_optional: bool = False


@dataclass
class Attribute:
    """Represents a class attribute/field"""
    name: str
    data_type: str
    visibility: Visibility = Visibility.PRIVATE
    is_static: bool = False
    is_final: bool = False
    default_value: Optional[str] = None
    description: Optional[str] = None


@dataclass
class Method:
    """Represents a class method"""
    name: str
    return_type: str = "void"
    visibility: Visibility = Visibility.PUBLIC
    is_static: bool = False
    is_abstract: bool = False
    is_final: bool = False
    parameters: List[Parameter] = field(default_factory=list)
    description: Optional[str] = None
    body: Optional[str] = None


@dataclass
class Relationship:
    """Represents relationships between classes"""
    source_class: str
    target_class: str
    relationship_type: str  # inheritance, composition, aggregation, association
    multiplicity_source: Optional[str] = None
    multiplicity_target: Optional[str] = None
    label: Optional[str] = None


@dataclass
class ClassDefinition:
    """Represents a UML class definition"""
    name: str
    package: Optional[str] = None
    is_abstract: bool = False
    is_interface: bool = False
    stereotype: Optional[str] = None
    attributes: List[Attribute] = field(default_factory=list)
    methods: List[Method] = field(default_factory=list)
    parent_classes: List[str] = field(default_factory=list)
    implemented_interfaces: List[str] = field(default_factory=list)
    description: Optional[str] = None


@dataclass
class ClassDiagram:
    """Represents a complete UML class diagram"""
    name: str
    classes: List[ClassDefinition] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    packages: List[str] = field(default_factory=list)
    description: Optional[str] = None
    
    def get_class_by_name(self, class_name: str) -> Optional[ClassDefinition]:
        """Find a class by name"""
        for cls in self.classes:
            if cls.name == class_name:
                return cls
        return None
    
    def get_classes_in_package(self, package_name: str) -> List[ClassDefinition]:
        """Get all classes in a specific package"""
        return [cls for cls in self.classes if cls.package == package_name]
    
    def get_relationships_for_class(self, class_name: str) -> List[Relationship]:
        """Get all relationships involving a specific class"""
        return [rel for rel in self.relationships 
                if rel.source_class == class_name or rel.target_class == class_name]


# Factory methods for common patterns
class ClassModelFactory:
    """Factory for creating common class model patterns"""
    
    @staticmethod
    def create_entity_class(name: str, attributes: Dict[str, str]) -> ClassDefinition:
        """Create a simple entity/data class"""
        class_attrs = []
        for attr_name, attr_type in attributes.items():
            class_attrs.append(Attribute(
                name=attr_name,
                data_type=attr_type,
                visibility=Visibility.PRIVATE
            ))
        
        # Add constructor
        constructor = Method(
            name="__init__",
            parameters=[Parameter(name=attr_name, data_type=attr_type) 
                       for attr_name, attr_type in attributes.items()]
        )
        
        # Add getters and setters
        methods = [constructor]
        for attr_name, attr_type in attributes.items():
            # Getter
            methods.append(Method(
                name=f"get_{attr_name}",
                return_type=attr_type,
                visibility=Visibility.PUBLIC
            ))
            # Setter
            methods.append(Method(
                name=f"set_{attr_name}",
                parameters=[Parameter(name="value", data_type=attr_type)],
                visibility=Visibility.PUBLIC
            ))
        
        return ClassDefinition(
            name=name,
            attributes=class_attrs,
            methods=methods
        )
    
    @staticmethod
    def create_interface(name: str, methods: List[str]) -> ClassDefinition:
        """Create an interface definition"""
        interface_methods = []
        for method_name in methods:
            interface_methods.append(Method(
                name=method_name,
                is_abstract=True,
                visibility=Visibility.PUBLIC
            ))
        
        return ClassDefinition(
            name=name,
            is_interface=True,
            methods=interface_methods
        )
    
    @staticmethod
    def create_service_class(name: str, dependencies: List[str]) -> ClassDefinition:
        """Create a service class with dependency injection"""
        attributes = []
        constructor_params = []
        
        for dep in dependencies:
            attr_name = f"{dep.lower()}_service"
            attributes.append(Attribute(
                name=attr_name,
                data_type=dep,
                visibility=Visibility.PRIVATE
            ))
            constructor_params.append(Parameter(
                name=attr_name,
                data_type=dep
            ))
        
        constructor = Method(
            name="__init__",
            parameters=constructor_params
        )
        
        return ClassDefinition(
            name=name,
            attributes=attributes,
            methods=[constructor]
        )


# Example usage and predefined models
def create_sample_model() -> ClassDiagram:
    """Create a sample class diagram for demonstration"""
    
    # User entity
    user_class = ClassModelFactory.create_entity_class(
        "User",
        {
            "id": "int",
            "username": "string",
            "email": "string",
            "created_at": "datetime"
        }
    )
    
    # Product entity
    product_class = ClassModelFactory.create_entity_class(
        "Product",
        {
            "id": "int",
            "name": "string",
            "price": "float",
            "description": "string"
        }
    )
    
    # Order entity
    order_class = ClassModelFactory.create_entity_class(
        "Order",
        {
            "id": "int",
            "user_id": "int",
            "total_amount": "float",
            "status": "string",
            "created_at": "datetime"
        }
    )
    
    # Repository interface
    repository_interface = ClassModelFactory.create_interface(
        "Repository",
        ["save", "find_by_id", "find_all", "delete"]
    )
    
    # Service classes
    user_service = ClassModelFactory.create_service_class(
        "UserService",
        ["UserRepository"]
    )
    
    order_service = ClassModelFactory.create_service_class(
        "OrderService",
        ["OrderRepository", "UserService"]
    )
    
    # Define relationships
    relationships = [
        Relationship("Order", "User", "association", "many", "one"),
        Relationship("UserService", "UserRepository", "composition"),
        Relationship("OrderService", "OrderRepository", "composition"),
        Relationship("OrderService", "UserService", "association"),
    ]
    
    return ClassDiagram(
        name="E-commerce System",
        classes=[
            user_class,
            product_class,
            order_class,
            repository_interface,
            user_service,
            order_service
        ],
        relationships=relationships,
        packages=["entities", "repositories", "services"],
        description="Sample e-commerce domain model"
    )