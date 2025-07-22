"""
Microservices Architecture Generator for Kessel Run
Generates complete microservice scaffolding with Spring Boot, Docker, and Kubernetes
"""

import os
from typing import Dict, List, Any
from .base_generator import BaseGenerator
from ..models.class_model import ClassDiagram, ClassDefinition


class MicroserviceGenerator(BaseGenerator):
    """Generate complete microservice architecture for Kessel Run teams"""
    
    def __init__(self):
        super().__init__()
        self.service_port_start = 8080
        
    def generate(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate complete microservice architecture"""
        files = {}
        
        # Generate a microservice for each major entity
        services = self._identify_services(diagram)
        
        for i, service in enumerate(services):
            service_name = service['name'].lower().replace(' ', '-')
            service_port = self.service_port_start + i
            
            # Spring Boot Application
            files.update(self._generate_spring_boot_service(service, service_name, service_port))
            
            # Docker configuration
            files.update(self._generate_docker_files(service_name))
            
            # Kubernetes manifests
            files.update(self._generate_k8s_manifests(service, service_name, service_port))
            
            # API Gateway configuration
            files.update(self._generate_api_gateway_config(service, service_name, service_port))
            
        # Infrastructure files
        files.update(self._generate_infrastructure_files(services))
        
        return files
    
    def _identify_services(self, diagram: ClassDiagram) -> List[Dict[str, Any]]:
        """Identify microservices based on domain entities"""
        services = []
        
        # Group related classes into services
        service_groups = {
            'user-service': ['User', 'Profile', 'Authentication'],
            'product-service': ['Product', 'Catalog', 'Inventory'],
            'order-service': ['Order', 'OrderItem', 'Cart', 'ShoppingCart'],
            'payment-service': ['Payment', 'Transaction', 'Billing'],
            'notification-service': ['Notification', 'Email', 'SMS'],
        }
        
        for service_name, class_patterns in service_groups.items():
            matching_classes = []
            for cls in diagram.classes:
                if any(pattern.lower() in cls.name.lower() for pattern in class_patterns):
                    matching_classes.append(cls)
            
            if matching_classes:
                services.append({
                    'name': service_name,
                    'classes': matching_classes,
                    'domain': service_name.split('-')[0].title()
                })
        
        # Handle remaining classes
        remaining_classes = [cls for cls in diagram.classes 
                           if not any(cls in service['classes'] for service in services)]
        
        if remaining_classes:
            services.append({
                'name': 'common-service',
                'classes': remaining_classes,
                'domain': 'Common'
            })
        
        return services
    
    def _generate_spring_boot_service(self, service: Dict, service_name: str, port: int) -> Dict[str, str]:
        """Generate Spring Boot microservice"""
        files = {}
        package_name = f"mil.af.kesselrun.{service_name.replace('-', '')}"
        
        # Application class
        files[f"{service_name}/src/main/java/{package_name.replace('.', '/')}/Application.java"] = f'''package {package_name};

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.cloud.client.discovery.EnableDiscoveryClient;
import org.springframework.cloud.openfeign.EnableFeignClients;
import org.springframework.data.jpa.repository.config.EnableJpaRepositories;

/**
 * {service['domain']} Service Application
 * Kessel Run Microservice for Air Force Mission Systems
 */
@SpringBootApplication
@EnableDiscoveryClient
@EnableFeignClients
@EnableJpaRepositories
public class Application {{
    public static void main(String[] args) {{
        SpringApplication.run(Application.class, args);
    }}
}}
'''
        
        # Generate entities
        for cls in service['classes']:
            files.update(self._generate_spring_entity(cls, package_name, service_name))
        
        # Generate repositories
        for cls in service['classes']:
            files.update(self._generate_spring_repository(cls, package_name, service_name))
        
        # Generate services
        for cls in service['classes']:
            files.update(self._generate_spring_service(cls, package_name, service_name))
        
        # Generate controllers
        for cls in service['classes']:
            files.update(self._generate_spring_controller(cls, package_name, service_name))
        
        # Configuration files
        files.update(self._generate_spring_config(service_name, port))
        
        return files
    
    def _generate_spring_entity(self, cls: ClassDefinition, package_name: str, service_name: str) -> Dict[str, str]:
        """Generate JPA Entity"""
        files = {}
        
        entity_code = f'''package {package_name}.entity;

import javax.persistence.*;
import javax.validation.constraints.*;
import java.time.LocalDateTime;
import java.util.Objects;

/**
 * {cls.name} Entity
 * Generated for Kessel Run Air Force Mission Systems
 */
@Entity
@Table(name = "{cls.name.lower()}")
public class {cls.name} {{
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
'''
        
        # Add attributes
        for attr in cls.attributes:
            attr_name = attr.name
            attr_type = self._map_to_java_type(attr.type)
            
            entity_code += f'''    @Column(name = "{attr_name}")
    @NotNull
    private {attr_type} {attr_name};
    
'''
        
        # Add audit fields
        entity_code += '''    @Column(name = "created_at")
    private LocalDateTime createdAt;
    
    @Column(name = "updated_at")
    private LocalDateTime updatedAt;
    
    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }
    
    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
    
'''
        
        # Generate getters and setters
        entity_code += "    // Getters and Setters\n"
        for attr in cls.attributes:
            attr_name = attr.name
            attr_type = self._map_to_java_type(attr.type)
            capitalized = attr_name.capitalize()
            
            entity_code += f'''    public {attr_type} get{capitalized}() {{
        return {attr_name};
    }}
    
    public void set{capitalized}({attr_type} {attr_name}) {{
        this.{attr_name} = {attr_name};
    }}
    
'''
        
        # Add equals, hashCode, toString
        entity_code += f'''    @Override
    public boolean equals(Object o) {{
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        {cls.name} entity = ({cls.name}) o;
        return Objects.equals(id, entity.id);
    }}
    
    @Override
    public int hashCode() {{
        return Objects.hash(id);
    }}
    
    @Override
    public String toString() {{
        return "{cls.name}{{" +
                "id=" + id +
                "}}";
    }}
}}
'''
        
        files[f"{service_name}/src/main/java/{package_name.replace('.', '/')}/entity/{cls.name}.java"] = entity_code
        return files
    
    def _generate_spring_repository(self, cls: ClassDefinition, package_name: str, service_name: str) -> Dict[str, str]:
        """Generate Spring Data JPA Repository"""
        files = {}
        
        repo_code = f'''package {package_name}.repository;

import {package_name}.entity.{cls.name};
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

/**
 * {cls.name} Repository
 * Air Force Kessel Run Data Access Layer
 */
@Repository
public interface {cls.name}Repository extends JpaRepository<{cls.name}, Long> {{
    
    /**
     * Find active records
     */
    @Query("SELECT e FROM {cls.name} e WHERE e.deletedAt IS NULL")
    List<{cls.name}> findAllActive();
    
    /**
     * Find by custom criteria
     */
'''
        
        # Add finder methods based on attributes
        for attr in cls.attributes[:3]:  # Limit to first 3 attributes
            attr_name = attr.name
            attr_type = self._map_to_java_type(attr.type)
            capitalized = attr_name.capitalize()
            
            repo_code += f'''    Optional<{cls.name}> findBy{capitalized}({attr_type} {attr_name});
    List<{cls.name}> findBy{capitalized}Containing({attr_type} {attr_name});
    
'''
        
        repo_code += "}\n"
        
        files[f"{service_name}/src/main/java/{package_name.replace('.', '/')}/repository/{cls.name}Repository.java"] = repo_code
        return files
    
    def _generate_spring_service(self, cls: ClassDefinition, package_name: str, service_name: str) -> Dict[str, str]:
        """Generate Spring Service Layer"""
        files = {}
        
        service_code = f'''package {package_name}.service;

import {package_name}.entity.{cls.name};
import {package_name}.repository.{cls.name}Repository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import java.util.List;
import java.util.Optional;

/**
 * {cls.name} Service
 * Business Logic Layer for Air Force Kessel Run
 */
@Service
@Transactional
public class {cls.name}Service {{
    
    @Autowired
    private {cls.name}Repository repository;
    
    /**
     * Get all active records
     */
    @Transactional(readOnly = true)
    public List<{cls.name}> findAll() {{
        return repository.findAllActive();
    }}
    
    /**
     * Get by ID
     */
    @Transactional(readOnly = true)
    public Optional<{cls.name}> findById(Long id) {{
        return repository.findById(id);
    }}
    
    /**
     * Create new record
     */
    public {cls.name} create({cls.name} entity) {{
        return repository.save(entity);
    }}
    
    /**
     * Update existing record
     */
    public {cls.name} update(Long id, {cls.name} entity) {{
        Optional<{cls.name}> existing = repository.findById(id);
        if (existing.isPresent()) {{
            entity.setId(id);
            return repository.save(entity);
        }}
        throw new RuntimeException("{cls.name} not found with id: " + id);
    }}
    
    /**
     * Delete record
     */
    public void delete(Long id) {{
        repository.deleteById(id);
    }}
}}
'''
        
        files[f"{service_name}/src/main/java/{package_name.replace('.', '/')}/service/{cls.name}Service.java"] = service_code
        return files
    
    def _generate_spring_controller(self, cls: ClassDefinition, package_name: str, service_name: str) -> Dict[str, str]:
        """Generate Spring REST Controller"""
        files = {}
        
        controller_code = f'''package {package_name}.controller;

import {package_name}.entity.{cls.name};
import {package_name}.service.{cls.name}Service;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import javax.validation.Valid;
import java.util.List;
import java.util.Optional;

/**
 * {cls.name} REST Controller
 * Air Force Kessel Run API Endpoints
 */
@RestController
@RequestMapping("/api/v1/{cls.name.lower()}")
@CrossOrigin(origins = "*")
public class {cls.name}Controller {{
    
    @Autowired
    private {cls.name}Service service;
    
    /**
     * Get all records
     */
    @GetMapping
    public ResponseEntity<List<{cls.name}>> getAll() {{
        List<{cls.name}> entities = service.findAll();
        return ResponseEntity.ok(entities);
    }}
    
    /**
     * Get by ID
     */
    @GetMapping("/{{id}}")
    public ResponseEntity<{cls.name}> getById(@PathVariable Long id) {{
        Optional<{cls.name}> entity = service.findById(id);
        return entity.map(ResponseEntity::ok)
                     .orElse(ResponseEntity.notFound().build());
    }}
    
    /**
     * Create new record
     */
    @PostMapping
    public ResponseEntity<{cls.name}> create(@Valid @RequestBody {cls.name} entity) {{
        {cls.name} created = service.create(entity);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }}
    
    /**
     * Update existing record
     */
    @PutMapping("/{{id}}")
    public ResponseEntity<{cls.name}> update(@PathVariable Long id, 
                                            @Valid @RequestBody {cls.name} entity) {{
        try {{
            {cls.name} updated = service.update(id, entity);
            return ResponseEntity.ok(updated);
        }} catch (RuntimeException e) {{
            return ResponseEntity.notFound().build();
        }}
    }}
    
    /**
     * Delete record
     */
    @DeleteMapping("/{{id}}")
    public ResponseEntity<Void> delete(@PathVariable Long id) {{
        service.delete(id);
        return ResponseEntity.noContent().build();
    }}
}}
'''
        
        files[f"{service_name}/src/main/java/{package_name.replace('.', '/')}/controller/{cls.name}Controller.java"] = controller_code
        return files
    
    def _generate_spring_config(self, service_name: str, port: int) -> Dict[str, str]:
        """Generate Spring Boot configuration files"""
        files = {}
        
        # application.yml
        files[f"{service_name}/src/main/resources/application.yml"] = f'''spring:
  application:
    name: {service_name}
  profiles:
    active: dev
  datasource:
    url: jdbc:postgresql://localhost:5432/{service_name.replace('-', '_')}
    username: kessel_user
    password: kessel_pass
    driver-class-name: org.postgresql.Driver
  jpa:
    hibernate:
      ddl-auto: update
    show-sql: true
    properties:
      hibernate:
        dialect: org.hibernate.dialect.PostgreSQLDialect
        format_sql: true
  cloud:
    consul:
      host: localhost
      port: 8500
      discovery:
        service-name: {service_name}
        health-check-path: /actuator/health

server:
  port: {port}
  servlet:
    context-path: /{service_name}

management:
  endpoints:
    web:
      exposure:
        include: health,info,metrics,prometheus
  endpoint:
    health:
      show-details: always

logging:
  level:
    mil.af.kesselrun: DEBUG
    org.springframework.web: INFO
  pattern:
    console: "%d{{yyyy-MM-dd HH:mm:ss}} - %msg%n"
    file: "%d{{yyyy-MM-dd HH:mm:ss}} [%thread] %-5level %logger{{36}} - %msg%n"
  file:
    name: logs/{service_name}.log

# Kessel Run specific configuration
kessel-run:
  security:
    enabled: true
    jwt-secret: kessel-run-secret-key
  monitoring:
    enabled: true
    metrics-path: /metrics
'''
        
        # pom.xml
        files[f"{service_name}/pom.xml"] = f'''<?xml version="1.0" encoding="UTF-8"?>
<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 
         http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <modelVersion>4.0.0</modelVersion>
    
    <groupId>mil.af.kesselrun</groupId>
    <artifactId>{service_name}</artifactId>
    <version>1.0.0</version>
    <packaging>jar</packaging>
    
    <name>{service_name}</name>
    <description>Kessel Run Air Force Microservice</description>
    
    <parent>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-parent</artifactId>
        <version>2.7.0</version>
        <relativePath/>
    </parent>
    
    <properties>
        <java.version>11</java.version>
        <spring-cloud.version>2021.0.3</spring-cloud.version>
    </properties>
    
    <dependencies>
        <!-- Spring Boot Starters -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-data-jpa</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-validation</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-actuator</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-security</artifactId>
        </dependency>
        
        <!-- Spring Cloud -->
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-consul-discovery</artifactId>
        </dependency>
        <dependency>
            <groupId>org.springframework.cloud</groupId>
            <artifactId>spring-cloud-starter-openfeign</artifactId>
        </dependency>
        
        <!-- Database -->
        <dependency>
            <groupId>org.postgresql</groupId>
            <artifactId>postgresql</artifactId>
            <scope>runtime</scope>
        </dependency>
        
        <!-- Testing -->
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-test</artifactId>
            <scope>test</scope>
        </dependency>
        
        <!-- Metrics -->
        <dependency>
            <groupId>io.micrometer</groupId>
            <artifactId>micrometer-registry-prometheus</artifactId>
        </dependency>
    </dependencies>
    
    <dependencyManagement>
        <dependencies>
            <dependency>
                <groupId>org.springframework.cloud</groupId>
                <artifactId>spring-cloud-dependencies</artifactId>
                <version>${{spring-cloud.version}}</version>
                <type>pom</type>
                <scope>import</scope>
            </dependency>
        </dependencies>
    </dependencyManagement>
    
    <build>
        <plugins>
            <plugin>
                <groupId>org.springframework.boot</groupId>
                <artifactId>spring-boot-maven-plugin</artifactId>
            </plugin>
        </plugins>
    </build>
</project>
'''
        
        return files
    
    def _generate_docker_files(self, service_name: str) -> Dict[str, str]:
        """Generate Docker configuration"""
        files = {}
        
        # Dockerfile
        files[f"{service_name}/Dockerfile"] = f'''FROM openjdk:11-jre-slim

# Kessel Run Air Force microservice
LABEL maintainer="Kessel Run <kessel.run@us.af.mil>"
LABEL service="{service_name}"
LABEL version="1.0.0"

# Create non-root user
RUN groupadd -r kesselrun && useradd -r -g kesselrun kesselrun

# Set working directory
WORKDIR /app

# Copy jar file
COPY target/{service_name}-1.0.0.jar app.jar

# Change ownership
RUN chown -R kesselrun:kesselrun /app

# Switch to non-root user
USER kesselrun

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Run application
ENTRYPOINT ["java", "-jar", "app.jar"]
'''
        
        # docker-compose.yml for local development
        files[f"{service_name}/docker-compose.yml"] = f'''version: '3.8'

services:
  {service_name}:
    build: .
    ports:
      - "8080:8080"
    environment:
      - SPRING_PROFILES_ACTIVE=docker
      - SPRING_DATASOURCE_URL=jdbc:postgresql://postgres:5432/{service_name.replace('-', '_')}
    depends_on:
      - postgres
      - consul
    networks:
      - kessel-run-network
  
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_DB={service_name.replace('-', '_')}
      - POSTGRES_USER=kessel_user
      - POSTGRES_PASSWORD=kessel_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - kessel-run-network
  
  consul:
    image: consul:1.12
    command: agent -server -bootstrap -ui -node=server-1 -bind=0.0.0.0 -client=0.0.0.0
    ports:
      - "8500:8500"
    networks:
      - kessel-run-network

volumes:
  postgres_data:

networks:
  kessel-run-network:
    driver: bridge
'''
        
        return files
    
    def _generate_k8s_manifests(self, service: Dict, service_name: str, port: int) -> Dict[str, str]:
        """Generate Kubernetes manifests"""
        files = {}
        
        # Deployment
        files[f"{service_name}/k8s/deployment.yaml"] = f'''apiVersion: apps/v1
kind: Deployment
metadata:
  name: {service_name}
  namespace: kessel-run
  labels:
    app: {service_name}
    version: v1.0.0
    component: microservice
  annotations:
    kessel-run.af.mil/service: "{service_name}"
spec:
  replicas: 3
  selector:
    matchLabels:
      app: {service_name}
  template:
    metadata:
      labels:
        app: {service_name}
        version: v1.0.0
      annotations:
        prometheus.io/scrape: "true"
        prometheus.io/port: "{port}"
        prometheus.io/path: "/actuator/prometheus"
    spec:
      serviceAccountName: {service_name}-sa
      securityContext:
        runAsNonRoot: true
        runAsUser: 1000
        fsGroup: 1000
      containers:
      - name: {service_name}
        image: registry.il2.dso.mil/kessel-run/{service_name}:latest
        imagePullPolicy: Always
        ports:
        - containerPort: {port}
          name: http
        env:
        - name: SPRING_PROFILES_ACTIVE
          value: "kubernetes"
        - name: SPRING_DATASOURCE_URL
          valueFrom:
            secretKeyRef:
              name: {service_name}-db-secret
              key: url
        - name: SPRING_DATASOURCE_USERNAME
          valueFrom:
            secretKeyRef:
              name: {service_name}-db-secret
              key: username
        - name: SPRING_DATASOURCE_PASSWORD
          valueFrom:
            secretKeyRef:
              name: {service_name}-db-secret
              key: password
        resources:
          requests:
            memory: "512Mi"
            cpu: "250m"
          limits:
            memory: "1Gi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /actuator/health
            port: {port}
          initialDelaySeconds: 60
          periodSeconds: 30
        readinessProbe:
          httpGet:
            path: /actuator/health/readiness
            port: {port}
          initialDelaySeconds: 30
          periodSeconds: 10
        securityContext:
          allowPrivilegeEscalation: false
          readOnlyRootFilesystem: true
          runAsNonRoot: true
          capabilities:
            drop:
            - ALL
'''
        
        # Service
        files[f"{service_name}/k8s/service.yaml"] = f'''apiVersion: v1
kind: Service
metadata:
  name: {service_name}
  namespace: kessel-run
  labels:
    app: {service_name}
  annotations:
    kessel-run.af.mil/service: "{service_name}"
spec:
  type: ClusterIP
  ports:
  - port: 80
    targetPort: {port}
    protocol: TCP
    name: http
  selector:
    app: {service_name}
'''
        
        return files
    
    def _generate_api_gateway_config(self, service: Dict, service_name: str, port: int) -> Dict[str, str]:
        """Generate API Gateway configuration"""
        files = {}
        
        # Kong configuration
        files[f"{service_name}/api-gateway/kong.yaml"] = f'''_format_version: "2.1"
_transform: true

services:
- name: {service_name}
  url: http://{service_name}.kessel-run.svc.cluster.local
  plugins:
  - name: rate-limiting
    config:
      minute: 100
      hour: 1000
  - name: cors
    config:
      origins:
      - "*"
      methods:
      - GET
      - POST
      - PUT
      - DELETE
      - OPTIONS
      headers:
      - Accept
      - Authorization
      - Content-Type
      - X-Requested-With
  - name: jwt
    config:
      key_claim_name: iss
      secret_is_base64: false

routes:
- name: {service_name}-api
  service: {service_name}
  paths:
  - /api/v1/{service['domain'].lower()}
  methods:
  - GET
  - POST
  - PUT
  - DELETE
  strip_path: false
'''
        
        return files
    
    def _generate_infrastructure_files(self, services: List[Dict]) -> Dict[str, str]:
        """Generate infrastructure and deployment files"""
        files = {}
        
        # Docker Compose for all services
        compose_services = {}
        for i, service in enumerate(services):
            service_name = service['name']
            port = self.service_port_start + i
            
            compose_services[service_name] = {
                'build': f"./{service_name}",
                'ports': [f"{port}:{port}"],
                'environment': [
                    'SPRING_PROFILES_ACTIVE=docker',
                    f'SERVER_PORT={port}'
                ],
                'depends_on': ['postgres', 'consul'],
                'networks': ['kessel-run-network']
            }
        
        # Infrastructure docker-compose
        files["infrastructure/docker-compose.yml"] = f'''version: '3.8'

services:
  # Generated Microservices
{self._format_compose_services(compose_services)}
  
  # Infrastructure Services
  postgres:
    image: postgres:13
    environment:
      - POSTGRES_MULTIPLE_DATABASES={"_".join([s['name'].replace('-', '_') for s in services])}
      - POSTGRES_USER=kessel_user
      - POSTGRES_PASSWORD=kessel_pass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init-db.sh:/docker-entrypoint-initdb.d/init-db.sh
    networks:
      - kessel-run-network
  
  consul:
    image: consul:1.12
    command: agent -server -bootstrap -ui -node=server-1 -bind=0.0.0.0 -client=0.0.0.0
    ports:
      - "8500:8500"
    networks:
      - kessel-run-network
  
  kong:
    image: kong:latest
    environment:
      - KONG_DATABASE=off
      - KONG_DECLARATIVE_CONFIG=/kong/declarative/kong.yml
      - KONG_PROXY_ACCESS_LOG=/dev/stdout
      - KONG_ADMIN_ACCESS_LOG=/dev/stdout
      - KONG_PROXY_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_ERROR_LOG=/dev/stderr
      - KONG_ADMIN_LISTEN=0.0.0.0:8001
    ports:
      - "8000:8000"
      - "8443:8443"
      - "8001:8001"
      - "8444:8444"
    volumes:
      - ./api-gateway:/kong/declarative
    networks:
      - kessel-run-network

volumes:
  postgres_data:

networks:
  kessel-run-network:
    driver: bridge
'''
        
        # Kubernetes namespace
        files["k8s/namespace.yaml"] = '''apiVersion: v1
kind: Namespace
metadata:
  name: kessel-run
  labels:
    name: kessel-run
    istio-injection: enabled
  annotations:
    kessel-run.af.mil/environment: "production"
'''
        
        # Database initialization script
        files["infrastructure/init-db.sh"] = f'''#!/bin/bash
set -e

# Create databases for each service
{"".join([f'psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL\n    CREATE DATABASE {service["name"].replace("-", "_")};\n    GRANT ALL PRIVILEGES ON DATABASE {service["name"].replace("-", "_")} TO $POSTGRES_USER;\nEOSQL\n\n' for service in services])}

echo "All databases created successfully!"
'''
        
        return files
    
    def _format_compose_services(self, services: Dict) -> str:
        """Format docker-compose services section"""
        formatted = ""
        for name, config in services.items():
            formatted += f"  {name}:\n"
            formatted += f"    build: {config['build']}\n"
            formatted += f"    ports:\n"
            for port in config['ports']:
                formatted += f"      - \"{port}\"\n"
            formatted += f"    environment:\n"
            for env in config['environment']:
                formatted += f"      - {env}\n"
            formatted += f"    depends_on:\n"
            for dep in config['depends_on']:
                formatted += f"      - {dep}\n"
            formatted += f"    networks:\n"
            for network in config['networks']:
                formatted += f"      - {network}\n"
            formatted += "\n"
        return formatted
    
    def _map_to_java_type(self, type_str: str) -> str:
        """Map UML types to Java types"""
        type_mapping = {
            'int': 'Integer',
            'integer': 'Integer',
            'string': 'String',
            'float': 'Double',
            'boolean': 'Boolean',
            'bool': 'Boolean',
            'datetime': 'LocalDateTime',
            'date': 'LocalDate',
            'list': 'List<String>',
            'array': 'List<String>'
        }
        return type_mapping.get(type_str.lower(), 'String')


class BaseGenerator:
    """Base class for all code generators"""
    
    def generate(self, diagram) -> Dict[str, str]:
        """Generate code from diagram"""
        raise NotImplementedError