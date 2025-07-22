"""
OpenAPI/Swagger Generator for Kessel Run API-First Development
Generates complete OpenAPI specifications, client SDKs, and server stubs
"""

import json
import yaml
from typing import Dict, List, Any
from .base_generator import BaseGenerator
from ..models.class_model import ClassDiagram, ClassDefinition


class OpenAPIGenerator(BaseGenerator):
    """Generate OpenAPI specifications and client/server code for Kessel Run"""
    
    def __init__(self):
        super().__init__()
        self.api_version = "v1"
        
    def generate(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate OpenAPI specifications and related files"""
        files = {}
        
        # Generate OpenAPI specification
        openapi_spec = self._generate_openapi_spec(diagram)
        files["api/openapi.yaml"] = yaml.dump(openapi_spec, default_flow_style=False, sort_keys=False)
        files["api/openapi.json"] = json.dumps(openapi_spec, indent=2)
        
        # Generate client SDKs
        files.update(self._generate_client_sdks(diagram, openapi_spec))
        
        # Generate server stubs
        files.update(self._generate_server_stubs(diagram, openapi_spec))
        
        # Generate API documentation
        files.update(self._generate_api_docs(diagram, openapi_spec))
        
        # Generate testing files
        files.update(self._generate_api_tests(diagram, openapi_spec))
        
        return files
    
    def _generate_openapi_spec(self, diagram: ClassDiagram) -> Dict[str, Any]:
        """Generate complete OpenAPI 3.0 specification"""
        
        spec = {
            "openapi": "3.0.3",
            "info": {
                "title": f"{diagram.name} API",
                "description": "Air Force Kessel Run Mission System API",
                "version": "1.0.0",
                "contact": {
                    "name": "Kessel Run Team",
                    "email": "kessel.run@us.af.mil",
                    "url": "https://kesselrun.af.mil"
                },
                "license": {
                    "name": "U.S. Government Work",
                    "url": "https://www.usa.gov/government-works"
                }
            },
            "servers": [
                {
                    "url": "https://api.kesselrun.af.mil/v1",
                    "description": "Production server"
                },
                {
                    "url": "https://api-staging.kesselrun.af.mil/v1", 
                    "description": "Staging server"
                },
                {
                    "url": "http://localhost:8080/v1",
                    "description": "Development server"
                }
            ],
            "security": [
                {"bearerAuth": []},
                {"apiKeyAuth": []}
            ],
            "paths": {},
            "components": {
                "schemas": {},
                "securitySchemes": {
                    "bearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT"
                    },
                    "apiKeyAuth": {
                        "type": "apiKey",
                        "in": "header",
                        "name": "X-API-Key"
                    }
                },
                "parameters": {
                    "pageParam": {
                        "name": "page",
                        "in": "query",
                        "description": "Page number for pagination",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "minimum": 0,
                            "default": 0
                        }
                    },
                    "sizeParam": {
                        "name": "size", 
                        "in": "query",
                        "description": "Number of items per page",
                        "required": False,
                        "schema": {
                            "type": "integer",
                            "minimum": 1,
                            "maximum": 100,
                            "default": 20
                        }
                    }
                },
                "responses": {
                    "ErrorResponse": {
                        "description": "Error response",
                        "content": {
                            "application/json": {
                                "schema": {
                                    "type": "object",
                                    "properties": {
                                        "error": {
                                            "type": "object",
                                            "properties": {
                                                "code": {"type": "string"},
                                                "message": {"type": "string"},
                                                "details": {"type": "array", "items": {"type": "string"}},
                                                "timestamp": {"type": "string", "format": "date-time"}
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
        
        # Generate schemas for each class
        for cls in diagram.classes:
            spec["components"]["schemas"].update(self._generate_schemas_for_class(cls))
        
        # Generate paths for each class
        for cls in diagram.classes:
            spec["paths"].update(self._generate_paths_for_class(cls))
        
        return spec
    
    def _generate_schemas_for_class(self, cls: ClassDefinition) -> Dict[str, Any]:
        """Generate OpenAPI schemas for a class"""
        schemas = {}
        
        # Main entity schema
        properties = {}
        required = []
        
        # Add ID field
        properties["id"] = {
            "type": "integer",
            "format": "int64",
            "description": f"Unique identifier for {cls.name}",
            "example": 1
        }
        
        # Add attributes
        for attr in cls.attributes:
            property_schema = self._map_to_openapi_type(attr.type)
            property_schema["description"] = f"{cls.name} {attr.name}"
            properties[attr.name] = property_schema
            
            if not attr.name.endswith("_optional"):
                required.append(attr.name)
        
        # Add audit fields
        properties.update({
            "createdAt": {
                "type": "string",
                "format": "date-time",
                "description": "Creation timestamp",
                "readOnly": True
            },
            "updatedAt": {
                "type": "string", 
                "format": "date-time",
                "description": "Last update timestamp",
                "readOnly": True
            }
        })
        
        schemas[cls.name] = {
            "type": "object",
            "description": f"{cls.name} entity for Air Force mission systems",
            "properties": properties,
            "required": required
        }
        
        # Create DTO variants
        schemas[f"{cls.name}CreateRequest"] = {
            "type": "object",
            "description": f"Request payload for creating {cls.name}",
            "properties": {k: v for k, v in properties.items() 
                          if k not in ["id", "createdAt", "updatedAt"]},
            "required": [r for r in required if r != "id"]
        }
        
        schemas[f"{cls.name}UpdateRequest"] = {
            "type": "object",
            "description": f"Request payload for updating {cls.name}",
            "properties": {k: v for k, v in properties.items() 
                          if k not in ["id", "createdAt", "updatedAt"]},
            "required": []
        }
        
        schemas[f"{cls.name}Response"] = {
            "allOf": [
                {"$ref": f"#/components/schemas/{cls.name}"},
                {
                    "type": "object",
                    "properties": {
                        "_links": {
                            "type": "object",
                            "description": "HATEOAS links",
                            "properties": {
                                "self": {"type": "string", "format": "uri"},
                                "edit": {"type": "string", "format": "uri"},
                                "delete": {"type": "string", "format": "uri"}
                            }
                        }
                    }
                }
            ]
        }
        
        # Paginated response
        schemas[f"{cls.name}PageResponse"] = {
            "type": "object",
            "properties": {
                "content": {
                    "type": "array",
                    "items": {"$ref": f"#/components/schemas/{cls.name}Response"}
                },
                "pageable": {
                    "type": "object",
                    "properties": {
                        "page": {"type": "integer"},
                        "size": {"type": "integer"},
                        "sort": {"type": "string"}
                    }
                },
                "totalElements": {"type": "integer"},
                "totalPages": {"type": "integer"},
                "first": {"type": "boolean"},
                "last": {"type": "boolean"}
            }
        }
        
        return schemas
    
    def _generate_paths_for_class(self, cls: ClassDefinition) -> Dict[str, Any]:
        """Generate API paths for a class"""
        paths = {}
        resource_name = cls.name.lower()
        resource_path = f"/{resource_name}s"
        
        # Collection endpoints
        paths[resource_path] = {
            "get": {
                "tags": [cls.name],
                "summary": f"List all {cls.name}s",
                "description": f"Retrieve a paginated list of {cls.name} entities",
                "operationId": f"list{cls.name}s",
                "parameters": [
                    {"$ref": "#/components/parameters/pageParam"},
                    {"$ref": "#/components/parameters/sizeParam"},
                    {
                        "name": "sort",
                        "in": "query",
                        "description": "Sort criteria",
                        "required": False,
                        "schema": {
                            "type": "string",
                            "example": "createdAt,desc"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{cls.name}PageResponse"}
                            }
                        }
                    },
                    "400": {"$ref": "#/components/responses/ErrorResponse"},
                    "401": {"$ref": "#/components/responses/ErrorResponse"},
                    "500": {"$ref": "#/components/responses/ErrorResponse"}
                },
                "security": [{"bearerAuth": []}]
            },
            "post": {
                "tags": [cls.name],
                "summary": f"Create a new {cls.name}",
                "description": f"Create a new {cls.name} entity",
                "operationId": f"create{cls.name}",
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{cls.name}CreateRequest"}
                        }
                    }
                },
                "responses": {
                    "201": {
                        "description": f"{cls.name} created successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{cls.name}Response"}
                            }
                        }
                    },
                    "400": {"$ref": "#/components/responses/ErrorResponse"},
                    "401": {"$ref": "#/components/responses/ErrorResponse"},
                    "409": {"$ref": "#/components/responses/ErrorResponse"},
                    "500": {"$ref": "#/components/responses/ErrorResponse"}
                },
                "security": [{"bearerAuth": []}]
            }
        }
        
        # Individual resource endpoints
        paths[f"{resource_path}/{{id}}"] = {
            "get": {
                "tags": [cls.name],
                "summary": f"Get {cls.name} by ID",
                "description": f"Retrieve a specific {cls.name} by its ID",
                "operationId": f"get{cls.name}ById",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": f"{cls.name} ID",
                        "schema": {
                            "type": "integer",
                            "format": "int64"
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Successful response",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{cls.name}Response"}
                            }
                        }
                    },
                    "404": {"$ref": "#/components/responses/ErrorResponse"},
                    "401": {"$ref": "#/components/responses/ErrorResponse"},
                    "500": {"$ref": "#/components/responses/ErrorResponse"}
                },
                "security": [{"bearerAuth": []}]
            },
            "put": {
                "tags": [cls.name],
                "summary": f"Update {cls.name}",
                "description": f"Update an existing {cls.name}",
                "operationId": f"update{cls.name}",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path", 
                        "required": True,
                        "description": f"{cls.name} ID",
                        "schema": {
                            "type": "integer",
                            "format": "int64"
                        }
                    }
                ],
                "requestBody": {
                    "required": True,
                    "content": {
                        "application/json": {
                            "schema": {"$ref": f"#/components/schemas/{cls.name}UpdateRequest"}
                        }
                    }
                },
                "responses": {
                    "200": {
                        "description": f"{cls.name} updated successfully",
                        "content": {
                            "application/json": {
                                "schema": {"$ref": f"#/components/schemas/{cls.name}Response"}
                            }
                        }
                    },
                    "400": {"$ref": "#/components/responses/ErrorResponse"},
                    "404": {"$ref": "#/components/responses/ErrorResponse"},
                    "401": {"$ref": "#/components/responses/ErrorResponse"},
                    "500": {"$ref": "#/components/responses/ErrorResponse"}
                },
                "security": [{"bearerAuth": []}]
            },
            "delete": {
                "tags": [cls.name],
                "summary": f"Delete {cls.name}",
                "description": f"Delete a {cls.name} by ID",
                "operationId": f"delete{cls.name}",
                "parameters": [
                    {
                        "name": "id",
                        "in": "path",
                        "required": True,
                        "description": f"{cls.name} ID", 
                        "schema": {
                            "type": "integer",
                            "format": "int64"
                        }
                    }
                ],
                "responses": {
                    "204": {
                        "description": f"{cls.name} deleted successfully"
                    },
                    "404": {"$ref": "#/components/responses/ErrorResponse"},
                    "401": {"$ref": "#/components/responses/ErrorResponse"},
                    "500": {"$ref": "#/components/responses/ErrorResponse"}
                },
                "security": [{"bearerAuth": []}]
            }
        }
        
        return paths
    
    def _generate_client_sdks(self, diagram: ClassDiagram, spec: Dict) -> Dict[str, str]:
        """Generate client SDKs"""
        files = {}
        
        # JavaScript/TypeScript client
        files["clients/typescript/api-client.ts"] = self._generate_typescript_client(diagram, spec)
        
        # Java client
        files["clients/java/ApiClient.java"] = self._generate_java_client(diagram, spec)
        
        # Python client
        files["clients/python/api_client.py"] = self._generate_python_client(diagram, spec)
        
        return files
    
    def _generate_typescript_client(self, diagram: ClassDiagram, spec: Dict) -> str:
        """Generate TypeScript API client"""
        
        client_code = f'''/**
 * {diagram.name} API Client
 * Generated TypeScript client for Air Force Kessel Run
 */

export interface ApiConfig {{
  baseUrl: string;
  apiKey?: string;
  token?: string;
  timeout?: number;
}}

export interface ApiResponse<T> {{
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}}

export interface ErrorResponse {{
  error: {{
    code: string;
    message: string;
    details?: string[];
    timestamp: string;
  }};
}}

export interface PageResponse<T> {{
  content: T[];
  pageable: {{
    page: number;
    size: number;
    sort: string;
  }};
  totalElements: number;
  totalPages: number;
  first: boolean;
  last: boolean;
}}

// Entity interfaces
'''
        
        # Generate interfaces for each entity
        for cls in diagram.classes:
            client_code += f'''
export interface {cls.name} {{
  id: number;
'''
            for attr in cls.attributes:
                ts_type = self._map_to_typescript_type(attr.type)
                client_code += f'  {attr.name}: {ts_type};\n'
            
            client_code += f'''  createdAt: string;
  updatedAt: string;
}}

export interface {cls.name}CreateRequest {{
'''
            for attr in cls.attributes:
                ts_type = self._map_to_typescript_type(attr.type)
                client_code += f'  {attr.name}: {ts_type};\n'
            
            client_code += f'''}}

export interface {cls.name}UpdateRequest {{
'''
            for attr in cls.attributes:
                ts_type = self._map_to_typescript_type(attr.type)
                client_code += f'  {attr.name}?: {ts_type};\n'
            
            client_code += '}\n'
        
        # Generate API client class
        client_code += f'''
export class {diagram.name}ApiClient {{
  private config: ApiConfig;
  
  constructor(config: ApiConfig) {{
    this.config = config;
  }}
  
  private async request<T>(
    method: string, 
    path: string, 
    data?: any, 
    params?: Record<string, any>
  ): Promise<ApiResponse<T>> {{
    const url = new URL(path, this.config.baseUrl);
    
    if (params) {{
      Object.entries(params).forEach(([key, value]) => {{
        if (value !== undefined && value !== null) {{
          url.searchParams.append(key, String(value));
        }}
      }});
    }}
    
    const headers: Record<string, string> = {{
      'Content-Type': 'application/json',
    }};
    
    if (this.config.token) {{
      headers['Authorization'] = `Bearer ${{this.config.token}}`;
    }}
    
    if (this.config.apiKey) {{
      headers['X-API-Key'] = this.config.apiKey;
    }}
    
    const response = await fetch(url.toString(), {{
      method,
      headers,
      body: data ? JSON.stringify(data) : undefined,
      signal: AbortSignal.timeout(this.config.timeout || 30000)
    }});
    
    const responseData = await response.json();
    
    if (!response.ok) {{
      throw new Error(`API Error: ${{response.status}} - ${{responseData.error?.message || response.statusText}}`);
    }}
    
    return {{
      data: responseData,
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries())
    }};
  }}
'''
        
        # Generate methods for each entity
        for cls in diagram.classes:
            resource_name = cls.name.lower()
            client_code += f'''
  // {cls.name} API methods
  async list{cls.name}s(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<{cls.name}>>> {{
    return this.request('GET', '/{resource_name}s', undefined, {{ page, size, sort }});
  }}
  
  async get{cls.name}(id: number): Promise<ApiResponse<{cls.name}>> {{
    return this.request('GET', `/{resource_name}s/${{id}}`);
  }}
  
  async create{cls.name}(data: {cls.name}CreateRequest): Promise<ApiResponse<{cls.name}>> {{
    return this.request('POST', '/{resource_name}s', data);
  }}
  
  async update{cls.name}(id: number, data: {cls.name}UpdateRequest): Promise<ApiResponse<{cls.name}>> {{
    return this.request('PUT', `/{resource_name}s/${{id}}`, data);
  }}
  
  async delete{cls.name}(id: number): Promise<ApiResponse<void>> {{
    return this.request('DELETE', `/{resource_name}s/${{id}}`);
  }}
'''
        
        client_code += '}\n'
        return client_code
    
    def _generate_java_client(self, diagram: ClassDiagram, spec: Dict) -> str:
        """Generate Java API client"""
        
        return f'''package mil.af.kesselrun.client;

import java.util.List;
import java.util.concurrent.CompletableFuture;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.net.URI;
import java.time.Duration;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;

/**
 * {diagram.name} API Client for Air Force Kessel Run
 * Generated Java client for mission-critical systems
 */
public class {diagram.name}ApiClient {{
    
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    private final String baseUrl;
    private final String apiKey;
    private final String token;
    
    public {diagram.name}ApiClient(String baseUrl, String token) {{
        this.baseUrl = baseUrl;
        this.token = token;
        this.apiKey = null;
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
        this.objectMapper = new ObjectMapper();
        this.objectMapper.registerModule(new JavaTimeModule());
    }}
    
    public {diagram.name}ApiClient(String baseUrl, String apiKey, String token) {{
        this.baseUrl = baseUrl;
        this.token = token;
        this.apiKey = apiKey;
        this.httpClient = HttpClient.newBuilder()
            .connectTimeout(Duration.ofSeconds(30))
            .build();
        this.objectMapper = new ObjectMapper();
        this.objectMapper.registerModule(new JavaTimeModule());
    }}
    
    // Implementation methods would be generated here for each entity
    // This is a simplified example showing the structure
    
}}
'''
    
    def _generate_python_client(self, diagram: ClassDiagram, spec: Dict) -> str:
        """Generate Python API client"""
        
        return f'''"""
{diagram.name} API Client for Air Force Kessel Run
Generated Python client for mission-critical systems
"""

import requests
import json
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass


@dataclass
class ApiConfig:
    base_url: str
    api_key: Optional[str] = None
    token: Optional[str] = None
    timeout: int = 30


class {diagram.name}ApiClient:
    """API client for {diagram.name} service"""
    
    def __init__(self, config: ApiConfig):
        self.config = config
        self.session = requests.Session()
        
        if config.token:
            self.session.headers.update({{"Authorization": f"Bearer {{config.token}}"}})
        
        if config.api_key:
            self.session.headers.update({{"X-API-Key": config.api_key}})
    
    def _request(self, method: str, path: str, data: Any = None, params: Dict = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{{self.config.base_url}}{{path}}"
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=self.config.timeout
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {{str(e)}}")
'''
        
        # Add methods for each entity
        for cls in diagram.classes:
            resource_name = cls.name.lower()
        
        return '''
    # Entity-specific methods would be generated here
    # This is a simplified example showing the structure
    
    def health_check(self) -> Dict:
        """Check API health status"""
        return self._request('GET', '/health')
'''
    
    def _generate_server_stubs(self, diagram: ClassDiagram, spec: Dict) -> Dict[str, str]:
        """Generate server implementation stubs"""
        files = {}
        
        # Spring Boot controller interfaces
        for cls in diagram.classes:
            files[f"server-stubs/java/interfaces/{cls.name}Controller.java"] = self._generate_controller_interface(cls)
        
        return files
    
    def _generate_controller_interface(self, cls: ClassDefinition) -> str:
        """Generate Spring Boot controller interface"""
        
        return f'''package mil.af.kesselrun.api;

import mil.af.kesselrun.model.{cls.name};
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;

/**
 * {cls.name} Controller Interface
 * Generated for Air Force Kessel Run API specification compliance
 */
public interface {cls.name}Controller {{
    
    @GetMapping("/{cls.name.lower()}s")
    ResponseEntity<Page<{cls.name}>> list{cls.name}s(Pageable pageable);
    
    @GetMapping("/{cls.name.lower()}s/{{id}}")
    ResponseEntity<{cls.name}> get{cls.name}(@PathVariable Long id);
    
    @PostMapping("/{cls.name.lower()}s")
    ResponseEntity<{cls.name}> create{cls.name}(@Valid @RequestBody {cls.name} entity);
    
    @PutMapping("/{cls.name.lower()}s/{{id}}")
    ResponseEntity<{cls.name}> update{cls.name}(@PathVariable Long id, @Valid @RequestBody {cls.name} entity);
    
    @DeleteMapping("/{cls.name.lower()}s/{{id}}")
    ResponseEntity<Void> delete{cls.name}(@PathVariable Long id);
}}
'''
    
    def _generate_api_docs(self, diagram: ClassDiagram, spec: Dict) -> Dict[str, str]:
        """Generate API documentation"""
        files = {}
        
        # Generate Markdown documentation
        files["docs/api-documentation.md"] = self._generate_markdown_docs(diagram, spec)
        
        # Generate HTML documentation template
        files["docs/api-docs.html"] = self._generate_html_docs(diagram)
        
        return files
    
    def _generate_markdown_docs(self, diagram: ClassDiagram, spec: Dict) -> str:
        """Generate Markdown API documentation"""
        
        return f'''# {diagram.name} API Documentation

## Overview
This is the official API documentation for the {diagram.name} system, developed for Air Force Kessel Run mission-critical operations.

## Authentication
The API uses JWT Bearer tokens for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your-jwt-token>
```

## Base URL
- Production: `https://api.kesselrun.af.mil/v1`
- Staging: `https://api-staging.kesselrun.af.mil/v1`
- Development: `http://localhost:8080/v1`

## Rate Limiting
- 100 requests per minute per API key
- 1000 requests per hour per API key

## Response Format
All API responses follow a consistent format:

### Success Response
```json
{{
  "data": {{ ... }},
  "status": "success",
  "timestamp": "2024-01-01T00:00:00Z"
}}
```

### Error Response
```json
{{
  "error": {{
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": ["Additional error details"],
    "timestamp": "2024-01-01T00:00:00Z"
  }}
}}
```

## Entities

{"".join([f'''
### {cls.name}

**Description:** {cls.name} entity for Air Force mission systems

**Attributes:**
{"".join([f"- `{attr.name}` ({attr.type}): {cls.name} {attr.name}" for attr in cls.attributes])}

**Endpoints:**
- `GET /{cls.name.lower()}s` - List all {cls.name}s
- `GET /{cls.name.lower()}s/{{id}}` - Get {cls.name} by ID  
- `POST /{cls.name.lower()}s` - Create new {cls.name}
- `PUT /{cls.name.lower()}s/{{id}}` - Update {cls.name}
- `DELETE /{cls.name.lower()}s/{{id}}` - Delete {cls.name}

''' for cls in diagram.classes])}

## Error Codes

| Code | Description |
|------|-------------|
| `INVALID_REQUEST` | Request validation failed |
| `UNAUTHORIZED` | Authentication required |
| `FORBIDDEN` | Insufficient permissions |
| `NOT_FOUND` | Resource not found |
| `CONFLICT` | Resource already exists |
| `INTERNAL_ERROR` | Server error |

## Contact
For API support, contact the Kessel Run team at kessel.run@us.af.mil
'''
    
    def _generate_html_docs(self, diagram: ClassDiagram) -> str:
        """Generate HTML documentation template"""
        
        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{diagram.name} API Documentation</title>
    <script src="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui-bundle.js"></script>
    <link rel="stylesheet" href="https://unpkg.com/swagger-ui-dist@3.52.5/swagger-ui.css">
</head>
<body>
    <div id="swagger-ui"></div>
    <script>
        SwaggerUIBundle({{
            url: './openapi.yaml',
            dom_id: '#swagger-ui',
            presets: [
                SwaggerUIBundle.presets.apis,
                SwaggerUIBundle.presets.standalone
            ],
            layout: "StandaloneLayout"
        }});
    </script>
</body>
</html>
'''
    
    def _generate_api_tests(self, diagram: ClassDiagram, spec: Dict) -> Dict[str, str]:
        """Generate API test files"""
        files = {}
        
        # Postman collection
        collection = {
            "info": {
                "name": f"{diagram.name} API Tests",
                "description": "Kessel Run API test collection",
                "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
            },
            "auth": {
                "type": "bearer",
                "bearer": [
                    {"key": "token", "value": "{{jwt_token}}", "type": "string"}
                ]
            },
            "variable": [
                {"key": "base_url", "value": "{{base_url}}"},
                {"key": "jwt_token", "value": "{{jwt_token}}"}
            ],
            "item": []
        }
        
        # Generate test items for each entity
        for cls in diagram.classes:
            resource_name = cls.name.lower()
            
            collection["item"].extend([
                {
                    "name": f"List {cls.name}s",
                    "request": {
                        "method": "GET",
                        "header": [],
                        "url": {
                            "raw": "{{{{base_url}}}}/{resource_name}s",
                            "host": ["{{{{base_url}}}}"],
                            "path": [f"{resource_name}s"]
                        }
                    }
                },
                {
                    "name": f"Create {cls.name}",
                    "request": {
                        "method": "POST",
                        "header": [
                            {"key": "Content-Type", "value": "application/json"}
                        ],
                        "body": {
                            "mode": "raw",
                            "raw": json.dumps({attr.name: f"sample_{attr.name}" for attr in cls.attributes[:3]}, indent=2)
                        },
                        "url": {
                            "raw": "{{{{base_url}}}}/{resource_name}s",
                            "host": ["{{{{base_url}}}}"],
                            "path": [f"{resource_name}s"]
                        }
                    }
                }
            ])
        
        files["tests/postman_collection.json"] = json.dumps(collection, indent=2)
        
        # Generate environment file
        files["tests/postman_environment.json"] = json.dumps({
            "name": f"{diagram.name} Environment",
            "values": [
                {"key": "base_url", "value": "http://localhost:8080/v1", "enabled": True},
                {"key": "jwt_token", "value": "your-jwt-token-here", "enabled": True}
            ]
        }, indent=2)
        
        return files
    
    def _map_to_openapi_type(self, type_str: str) -> Dict[str, Any]:
        """Map UML types to OpenAPI schema types"""
        type_mapping = {
            'int': {'type': 'integer', 'format': 'int32', 'example': 123},
            'integer': {'type': 'integer', 'format': 'int32', 'example': 123},
            'long': {'type': 'integer', 'format': 'int64', 'example': 123456789},
            'string': {'type': 'string', 'example': 'sample text'},
            'float': {'type': 'number', 'format': 'float', 'example': 123.45},
            'double': {'type': 'number', 'format': 'double', 'example': 123.456789},
            'boolean': {'type': 'boolean', 'example': True},
            'bool': {'type': 'boolean', 'example': True},
            'datetime': {'type': 'string', 'format': 'date-time', 'example': '2024-01-01T00:00:00Z'},
            'date': {'type': 'string', 'format': 'date', 'example': '2024-01-01'},
            'list': {'type': 'array', 'items': {'type': 'string'}},
            'array': {'type': 'array', 'items': {'type': 'string'}}
        }
        return type_mapping.get(type_str.lower(), {'type': 'string', 'example': 'sample text'})
    
    def _map_to_typescript_type(self, type_str: str) -> str:
        """Map UML types to TypeScript types"""
        type_mapping = {
            'int': 'number',
            'integer': 'number', 
            'long': 'number',
            'string': 'string',
            'float': 'number',
            'double': 'number',
            'boolean': 'boolean',
            'bool': 'boolean',
            'datetime': 'string',
            'date': 'string',
            'list': 'string[]',
            'array': 'string[]'
        }
        return type_mapping.get(type_str.lower(), 'string')


class BaseGenerator:
    """Base class for all code generators"""
    
    def generate(self, diagram) -> Dict[str, str]:
        """Generate code from diagram"""
        raise NotImplementedError