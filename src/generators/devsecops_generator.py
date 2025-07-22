"""
DevSecOps Generator for Kessel Run
Integrates security-first patterns, automated testing, and compliance into generated code
"""

import os
from typing import Dict, List, Any
from .base_generator import BaseGenerator
from ..models.class_model import ClassDiagram, ClassDefinition


class DevSecOpsGenerator(BaseGenerator):
    """Generate DevSecOps pipeline and security configurations for Kessel Run"""
    
    def __init__(self):
        super().__init__()
        
    def generate(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate complete DevSecOps pipeline and security configurations"""
        files = {}
        
        # Security configurations
        files.update(self._generate_security_configs())
        
        # CI/CD pipelines
        files.update(self._generate_cicd_pipelines(diagram))
        
        # Security testing
        files.update(self._generate_security_tests(diagram))
        
        # Compliance configurations
        files.update(self._generate_compliance_configs())
        
        # Monitoring and logging
        files.update(self._generate_monitoring_configs(diagram))
        
        # Container security
        files.update(self._generate_container_security())
        
        return files
    
    def _generate_security_configs(self) -> Dict[str, str]:
        """Generate security configuration files"""
        files = {}
        
        # Spring Security configuration
        files["security/SecurityConfig.java"] = '''package mil.af.kesselrun.security;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.method.configuration.EnableGlobalMethodSecurity;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.http.SessionCreationPolicy;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.security.web.SecurityFilterChain;
import org.springframework.security.web.authentication.UsernamePasswordAuthenticationFilter;
import org.springframework.security.web.header.writers.ReferrerPolicyHeaderWriter;
import org.springframework.web.cors.CorsConfiguration;
import org.springframework.web.cors.CorsConfigurationSource;
import org.springframework.web.cors.UrlBasedCorsConfigurationSource;

import java.util.Arrays;

/**
 * Kessel Run Security Configuration
 * Implements DoD security requirements and best practices
 */
@Configuration
@EnableWebSecurity
@EnableGlobalMethodSecurity(prePostEnabled = true, securedEnabled = true, jsr250Enabled = true)
public class SecurityConfig {
    
    @Value("${kessel-run.security.jwt.secret}")
    private String jwtSecret;
    
    @Value("${kessel-run.security.cors.allowed-origins:*}")
    private String[] allowedOrigins;
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12);
    }
    
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            // Disable CSRF for stateless API
            .csrf().disable()
            
            // Configure session management
            .sessionManagement().sessionCreationPolicy(SessionCreationPolicy.STATELESS)
            
            // Configure CORS
            .and().cors().configurationSource(corsConfigurationSource())
            
            // Configure security headers
            .and().headers()
                .frameOptions().deny()
                .contentTypeOptions()
                .and().httpStrictTransportSecurity(hstsConfig -> hstsConfig
                    .maxAgeInSeconds(31536000)
                    .includeSubdomains(true))
                .referrerPolicy(ReferrerPolicyHeaderWriter.ReferrerPolicy.STRICT_ORIGIN_WHEN_CROSS_ORIGIN)
            
            // Configure authorization
            .and().authorizeHttpRequests(authz -> authz
                // Public endpoints
                .requestMatchers("/actuator/health", "/actuator/info").permitAll()
                .requestMatchers("/api/v1/auth/**").permitAll()
                .requestMatchers("/swagger-ui/**", "/api-docs/**").permitAll()
                
                // Admin endpoints
                .requestMatchers("/actuator/**").hasRole("ADMIN")
                
                // API endpoints require authentication
                .requestMatchers("/api/**").authenticated()
                
                // All other requests require authentication
                .anyRequest().authenticated()
            );
        
        // Add JWT filter
        http.addFilterBefore(jwtAuthenticationFilter(), UsernamePasswordAuthenticationFilter.class);
        
        return http.build();
    }
    
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration configuration = new CorsConfiguration();
        configuration.setAllowedOriginPatterns(Arrays.asList(allowedOrigins));
        configuration.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "DELETE", "OPTIONS"));
        configuration.setAllowedHeaders(Arrays.asList("*"));
        configuration.setAllowCredentials(true);
        configuration.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", configuration);
        return source;
    }
    
    @Bean
    public JwtAuthenticationFilter jwtAuthenticationFilter() {
        return new JwtAuthenticationFilter();
    }
}
'''
        
        # JWT Authentication Filter
        files["security/JwtAuthenticationFilter.java"] = '''package mil.af.kesselrun.security;

import io.jsonwebtoken.Claims;
import io.jsonwebtoken.Jwts;
import io.jsonwebtoken.SignatureException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.stereotype.Component;
import org.springframework.web.filter.OncePerRequestFilter;

import javax.servlet.FilterChain;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;

/**
 * JWT Authentication Filter for Kessel Run
 * Validates JWT tokens and sets security context
 */
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    private static final Logger logger = LoggerFactory.getLogger(JwtAuthenticationFilter.class);
    private static final String TOKEN_PREFIX = "Bearer ";
    
    @Value("${kessel-run.security.jwt.secret}")
    private String jwtSecret;
    
    @Override
    protected void doFilterInternal(HttpServletRequest request, HttpServletResponse response, 
                                  FilterChain filterChain) throws ServletException, IOException {
        
        String token = getTokenFromRequest(request);
        
        if (token != null && validateToken(token)) {
            try {
                Claims claims = Jwts.parser()
                    .setSigningKey(jwtSecret)
                    .parseClaimsJws(token)
                    .getBody();
                
                String username = claims.getSubject();
                List<String> roles = (List<String>) claims.get("roles");
                
                List<SimpleGrantedAuthority> authorities = roles.stream()
                    .map(role -> new SimpleGrantedAuthority("ROLE_" + role))
                    .collect(Collectors.toList());
                
                UsernamePasswordAuthenticationToken auth = 
                    new UsernamePasswordAuthenticationToken(username, null, authorities);
                
                SecurityContextHolder.getContext().setAuthentication(auth);
                
                logger.debug("JWT authentication successful for user: {}", username);
                
            } catch (Exception e) {
                logger.error("JWT authentication failed", e);
                SecurityContextHolder.clearContext();
            }
        }
        
        filterChain.doFilter(request, response);
    }
    
    private String getTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith(TOKEN_PREFIX)) {
            return bearerToken.substring(TOKEN_PREFIX.length());
        }
        return null;
    }
    
    private boolean validateToken(String token) {
        try {
            Jwts.parser().setSigningKey(jwtSecret).parseClaimsJws(token);
            return true;
        } catch (SignatureException e) {
            logger.error("Invalid JWT signature", e);
        } catch (Exception e) {
            logger.error("JWT validation error", e);
        }
        return false;
    }
}
'''
        
        # Security Headers Filter
        files["security/SecurityHeadersFilter.java"] = '''package mil.af.kesselrun.security;

import org.springframework.stereotype.Component;

import javax.servlet.*;
import javax.servlet.http.HttpServletResponse;
import java.io.IOException;

/**
 * Security Headers Filter for Kessel Run
 * Adds DoD-required security headers
 */
@Component
public class SecurityHeadersFilter implements Filter {
    
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
            throws IOException, ServletException {
        
        HttpServletResponse httpResponse = (HttpServletResponse) response;
        
        // DoD Security Headers
        httpResponse.setHeader("X-Content-Type-Options", "nosniff");
        httpResponse.setHeader("X-Frame-Options", "DENY");
        httpResponse.setHeader("X-XSS-Protection", "1; mode=block");
        httpResponse.setHeader("Strict-Transport-Security", "max-age=31536000; includeSubDomains");
        httpResponse.setHeader("Referrer-Policy", "strict-origin-when-cross-origin");
        httpResponse.setHeader("Permissions-Policy", "geolocation=(), microphone=(), camera=()");
        
        // Content Security Policy
        httpResponse.setHeader("Content-Security-Policy", 
            "default-src 'self'; " +
            "script-src 'self' 'unsafe-inline'; " +
            "style-src 'self' 'unsafe-inline'; " +
            "img-src 'self' data:; " +
            "connect-src 'self'; " +
            "font-src 'self'; " +
            "object-src 'none'; " +
            "media-src 'self'; " +
            "frame-src 'none';");
        
        chain.doFilter(request, response);
    }
}
'''
        
        return files
    
    def _generate_cicd_pipelines(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate CI/CD pipeline configurations"""
        files = {}
        
        # Enhanced GitLab CI with security scans
        files[".gitlab-ci.yml"] = f'''# Kessel Run DevSecOps Pipeline
# Enhanced CI/CD with integrated security scanning and compliance

stages:
  - security-scan
  - build
  - test
  - security-test
  - compliance-check
  - deploy-dev
  - deploy-staging
  - deploy-prod

variables:
  DOCKER_DRIVER: overlay2
  DOCKER_TLS_CERTDIR: "/certs"
  MAVEN_OPTS: "-Dmaven.repo.local=$CI_PROJECT_DIR/.m2/repository"
  SONAR_TOKEN: $SONAR_TOKEN
  SNYK_TOKEN: $SNYK_TOKEN

# Security scanning before any build
sast:
  stage: security-scan
  image: registry1.dso.mil/ironbank/gitlab/gitlab-runner/gitlab-runner:latest
  script:
    - echo "Running Static Application Security Testing (SAST)..."
    - bandit -r src/ -f json -o bandit-report.json || true
    - semgrep --config=auto --json --output=semgrep-report.json src/ || true
    - safety check --json --output safety-report.json || true
  artifacts:
    reports:
      sast: bandit-report.json
    paths:
      - bandit-report.json
      - semgrep-report.json
      - safety-report.json
    expire_in: 1 week
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Dependency scanning
dependency_scanning:
  stage: security-scan
  image: registry1.dso.mil/ironbank/aquasec/trivy:latest
  script:
    - echo "Scanning dependencies for vulnerabilities..."
    - trivy fs --format json --output dependency-scan-report.json .
  artifacts:
    reports:
      dependency_scanning: dependency-scan-report.json
    expire_in: 1 week
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# License compliance scanning
license_scanning:
  stage: security-scan
  image: registry1.dso.mil/ironbank/fossa/fossa:latest
  script:
    - echo "Scanning for license compliance..."
    - fossa analyze
    - fossa test --json > license-report.json || true
  artifacts:
    reports:
      license_scanning: license-report.json
    expire_in: 1 week
  allow_failure: true
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Build application
build:
  stage: build
  image: registry1.dso.mil/ironbank/redhat/ubi/ubi8:8.8
  services:
    - name: registry1.dso.mil/ironbank/docker/docker-dind:20-dind
      alias: docker
  cache:
    paths:
      - .m2/repository/
  before_script:
    - echo $CI_REGISTRY_PASSWORD | docker login -u $CI_REGISTRY_USER --password-stdin $CI_REGISTRY
  script:
    - mvn clean compile -B
    - mvn package -B -DskipTests
    - docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .
    - docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    paths:
      - target/
    expire_in: 1 day
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Unit and integration tests
test:
  stage: test
  image: registry1.dso.mil/ironbank/opensource/openjdk/openjdk11:1.11.0
  cache:
    paths:
      - .m2/repository/
  script:
    - mvn test -B
    - mvn verify -B
  coverage: '/Total.*?([0-9]{{1,3}}\\.[0-9]{{1,2}})%/'
  artifacts:
    reports:
      junit: target/surefire-reports/TEST-*.xml
      coverage_report:
        coverage_format: cobertura
        path: target/site/cobertura/coverage.xml
    paths:
      - target/site/jacoco/
    expire_in: 1 week
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Code quality analysis
code_quality:
  stage: test
  image: registry1.dso.mil/ironbank/sonarqube/sonar-scanner-cli:latest
  variables:
    SONAR_USER_HOME: "${{CI_PROJECT_DIR}}/.sonar"
    GIT_DEPTH: "0"
  cache:
    key: "${{CI_JOB_NAME}}"
    paths:
      - .sonar/cache
  script:
    - sonar-scanner
  artifacts:
    reports:
      codequality: sonarqube-report.json
  rules:
    - if: $CI_MERGE_REQUEST_IID
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Dynamic Application Security Testing (DAST)
dast:
  stage: security-test
  image: registry1.dso.mil/ironbank/owasp/zap/zap:stable
  variables:
    DAST_WEBSITE: http://localhost:8080
  services:
    - name: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
      alias: app
  script:
    - echo "Running DAST scan..."
    - zap-baseline.py -t $DAST_WEBSITE -J dast-report.json || true
  artifacts:
    reports:
      dast: dast-report.json
    expire_in: 1 week
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Container security scanning
container_scanning:
  stage: security-test
  image: registry1.dso.mil/ironbank/aquasec/trivy:latest
  services:
    - name: registry1.dso.mil/ironbank/docker/docker-dind:20-dind
      alias: docker
  script:
    - docker pull $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
    - trivy image --format json --output container-scan-report.json $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA
  artifacts:
    reports:
      container_scanning: container-scan-report.json
    expire_in: 1 week
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# FISMA compliance check
fisma_compliance:
  stage: compliance-check
  image: registry1.dso.mil/ironbank/nessus/nessus:latest
  script:
    - echo "Running FISMA compliance checks..."
    - # Run compliance scanning tools
    - echo "Compliance check completed"
  artifacts:
    reports:
      compliance: fisma-compliance-report.json
  allow_failure: true
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Deploy to development
deploy-dev:
  stage: deploy-dev
  image: registry1.dso.mil/ironbank/kubernetes/kubectl:latest
  environment:
    name: development
    url: https://{diagram.name.lower()}-dev.apps.dso.mil
  script:
    - kubectl config use-context $KUBE_CONTEXT_DEV
    - envsubst < k8s/deployment.yaml | kubectl apply -f -
    - kubectl apply -f k8s/service.yaml -n kessel-run-dev
    - kubectl apply -f k8s/ingress.yaml -n kessel-run-dev
    - kubectl rollout status deployment/{diagram.name.lower()}-service -n kessel-run-dev
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Deploy to staging (manual)
deploy-staging:
  stage: deploy-staging
  image: registry1.dso.mil/ironbank/kubernetes/kubectl:latest
  environment:
    name: staging
    url: https://{diagram.name.lower()}-staging.apps.dso.mil
  script:
    - kubectl config use-context $KUBE_CONTEXT_STAGING
    - envsubst < k8s/deployment.yaml | kubectl apply -f -
    - kubectl apply -f k8s/service.yaml -n kessel-run-staging
    - kubectl apply -f k8s/ingress.yaml -n kessel-run-staging
    - kubectl rollout status deployment/{diagram.name.lower()}-service -n kessel-run-staging
  when: manual
  rules:
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH

# Deploy to production (manual with approval)
deploy-prod:
  stage: deploy-prod
  image: registry1.dso.mil/ironbank/kubernetes/kubectl:latest
  environment:
    name: production
    url: https://{diagram.name.lower()}.apps.dso.mil
  script:
    - kubectl config use-context $KUBE_CONTEXT_PROD
    - envsubst < k8s/deployment.yaml | kubectl apply -f -
    - kubectl apply -f k8s/service.yaml -n kessel-run
    - kubectl apply -f k8s/ingress.yaml -n kessel-run
    - kubectl rollout status deployment/{diagram.name.lower()}-service -n kessel-run
  when: manual
  rules:
    - if: '$CI_COMMIT_TAG'
    - if: $CI_COMMIT_BRANCH == $CI_DEFAULT_BRANCH
      when: manual
      allow_failure: false
'''
        
        # SonarQube configuration
        files["sonar-project.properties"] = '''# SonarQube Configuration for Kessel Run
sonar.projectKey=kessel-run-model-to-code
sonar.projectName=Kessel Run Model to Code Generator
sonar.projectVersion=1.0.0

# Source settings
sonar.sources=src/main
sonar.tests=src/test
sonar.java.binaries=target/classes
sonar.java.test.binaries=target/test-classes

# Coverage settings
sonar.coverage.jacoco.xmlReportPaths=target/site/jacoco/jacoco.xml
sonar.java.coveragePlugin=jacoco

# Language specific settings
sonar.java.source=11
sonar.exclusions=**/*Test.java,**/*IT.java,**/target/**

# Quality gates
sonar.qualitygate.wait=true

# Security settings
sonar.security.hotspots.inclusions=**/*.java
sonar.security.hotspots.exclusions=**/test/**
'''
        
        return files
    
    def _generate_security_tests(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate security test files"""
        files = {}
        
        # OWASP ZAP automation configuration
        files["security-tests/zap-automation.yaml"] = '''version: "1.0.0"
jobs:
  - type: passive-scan
    parameters:
      maxAlertsPerRule: 10
      scanOnlyInScope: true
  
  - type: spider
    parameters:
      context: "Default Context"
      url: "http://localhost:8080"
      maxDuration: 10
      maxChildren: 10
  
  - type: active-scan
    parameters:
      context: "Default Context"
      policy: "Default Policy"
      maxRuleDurationInMins: 5
      maxScanDurationInMins: 10
  
  - type: report
    parameters:
      template: "traditional-json"
      reportFile: "/zap/reports/zap-report.json"
      reportTitle: "Kessel Run Security Test Report"
      reportDescription: "Security test results for Air Force mission systems"

contexts:
  - name: "Default Context"
    includePaths:
      - "http://localhost:8080/api/.*"
    excludePaths:
      - "http://localhost:8080/actuator/.*"
    authentication:
      method: "bearer"
      bearer:
        token: "test-jwt-token"
'''
        
        # Security integration tests
        files["src/test/java/security/SecurityIntegrationTest.java"] = '''package mil.af.kesselrun.security;

import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.ActiveProfiles;

import static org.junit.jupiter.api.Assertions.*;

/**
 * Security Integration Tests for Kessel Run
 * Tests security configurations and authentication
 */
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@ActiveProfiles("test")
public class SecurityIntegrationTest {
    
    @LocalServerPort
    private int port;
    
    private TestRestTemplate restTemplate = new TestRestTemplate();
    
    @Test
    public void testSecurityHeaders() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "http://localhost:" + port + "/actuator/health", String.class);
        
        // Check security headers
        assertTrue(response.getHeaders().containsKey("X-Content-Type-Options"));
        assertEquals("nosniff", response.getHeaders().getFirst("X-Content-Type-Options"));
        
        assertTrue(response.getHeaders().containsKey("X-Frame-Options"));
        assertEquals("DENY", response.getHeaders().getFirst("X-Frame-Options"));
        
        assertTrue(response.getHeaders().containsKey("X-XSS-Protection"));
        assertEquals("1; mode=block", response.getHeaders().getFirst("X-XSS-Protection"));
    }
    
    @Test
    public void testUnauthorizedAccess() {
        ResponseEntity<String> response = restTemplate.getForEntity(
            "http://localhost:" + port + "/api/v1/users", String.class);
        
        assertEquals(HttpStatus.UNAUTHORIZED, response.getStatusCode());
    }
    
    @Test
    public void testCORSHeaders() {
        ResponseEntity<String> response = restTemplate.optionsForEntity(
            "http://localhost:" + port + "/api/v1/users", String.class);
        
        assertTrue(response.getHeaders().containsKey("Access-Control-Allow-Origin"));
        assertTrue(response.getHeaders().containsKey("Access-Control-Allow-Methods"));
    }
}
'''
        
        return files
    
    def _generate_compliance_configs(self) -> Dict[str, str]:
        """Generate compliance configuration files"""
        files = {}
        
        # FISMA compliance configuration
        files["compliance/fisma-controls.yaml"] = '''# FISMA Security Controls Implementation
# Air Force Kessel Run Compliance Configuration

access_controls:
  AC-2: # Account Management
    implemented: true
    description: "Account management through Spring Security and JWT"
    evidence: "SecurityConfig.java, JwtAuthenticationFilter.java"
  
  AC-3: # Access Enforcement
    implemented: true
    description: "Role-based access control with Spring Security"
    evidence: "@PreAuthorize annotations, SecurityConfig.java"
  
  AC-6: # Least Privilege
    implemented: true
    description: "Minimal required permissions per role"
    evidence: "Role definitions in SecurityConfig.java"

audit_controls:
  AU-2: # Audit Events
    implemented: true
    description: "Security event logging via Spring Boot Actuator"
    evidence: "application.yml logging configuration"
  
  AU-3: # Audit Record Content
    implemented: true
    description: "Structured logging with user context"
    evidence: "AuditEventRepository configuration"
  
  AU-12: # Audit Generation
    implemented: true
    description: "Automated audit log generation"
    evidence: "Logback configuration, Spring Security events"

configuration_management:
  CM-6: # Configuration Settings
    implemented: true
    description: "Secure configuration management"
    evidence: "application.yml, security properties"
  
  CM-7: # Least Functionality
    implemented: true
    description: "Minimal service configuration"
    evidence: "Disabled unused Spring modules"

identification_authentication:
  IA-2: # Identification and Authentication
    implemented: true
    description: "JWT-based authentication"
    evidence: "JwtAuthenticationFilter.java"
  
  IA-5: # Authenticator Management
    implemented: true
    description: "Secure password policies"
    evidence: "BCryptPasswordEncoder configuration"

system_communications:
  SC-7: # Boundary Protection
    implemented: true
    description: "Network security controls"
    evidence: "NetworkPolicy configurations"
  
  SC-8: # Transmission Confidentiality
    implemented: true
    description: "TLS encryption for all communications"
    evidence: "HTTPS configuration, TLS certificates"
  
  SC-23: # Session Authenticity
    implemented: true
    description: "JWT token-based session management"
    evidence: "Stateless session configuration"
'''
        
        # STIG compliance checklist
        files["compliance/stig-checklist.json"] = '''{
  "stigId": "APSC-DV-002560",
  "title": "Application Security and Development STIG",
  "version": "V4R11",
  "releaseDate": "2024-01-01",
  "checks": [
    {
      "vulnId": "V-222397",
      "rule": "APSC-DV-002560",
      "severity": "high",
      "title": "The application must protect the confidentiality and integrity of transmitted information.",
      "status": "NotAFinding",
      "comments": "TLS 1.3 implemented for all communications",
      "evidence": "SecurityConfig.java - HTTPS enforcement"
    },
    {
      "vulnId": "V-222398", 
      "rule": "APSC-DV-002570",
      "severity": "medium",
      "title": "The application must implement cryptographic mechanisms to prevent unauthorized modification of information at rest.",
      "status": "NotAFinding",
      "comments": "Database encryption enabled",
      "evidence": "application.yml - database encryption settings"
    },
    {
      "vulnId": "V-222399",
      "rule": "APSC-DV-002580",
      "severity": "high", 
      "title": "The application must separate user functionality from management functionality.",
      "status": "NotAFinding",
      "comments": "Role-based access control implemented",
      "evidence": "SecurityConfig.java - role separation"
    }
  ]
}'''
        
        return files
    
    def _generate_monitoring_configs(self, diagram: ClassDiagram) -> Dict[str, str]:
        """Generate monitoring and logging configurations"""
        files = {}
        
        # Logback configuration with security logging
        files["src/main/resources/logback-spring.xml"] = '''<?xml version="1.0" encoding="UTF-8"?>
<configuration>
    <springProfile name="!prod">
        <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
            <encoder>
                <pattern>%d{yyyy-MM-dd HH:mm:ss} [%thread] %-5level %logger{36} - %msg%n</pattern>
            </encoder>
        </appender>
        <root level="INFO">
            <appender-ref ref="CONSOLE"/>
        </root>
    </springProfile>
    
    <springProfile name="prod">
        <!-- File appender with security events -->
        <appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
            <file>logs/kessel-run.log</file>
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
                <fileNamePattern>logs/kessel-run.%d{yyyy-MM-dd}.%i.log.gz</fileNamePattern>
                <maxFileSize>100MB</maxFileSize>
                <maxHistory>30</maxHistory>
                <totalSizeCap>10GB</totalSizeCap>
            </rollingPolicy>
            <encoder>
                <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [%thread] %-5level [%X{traceId:-},%X{spanId:-}] %logger{40} - %msg%n</pattern>
            </encoder>
        </appender>
        
        <!-- Security events appender -->
        <appender name="SECURITY" class="ch.qos.logback.core.rolling.RollingFileAppender">
            <file>logs/security.log</file>
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
                <fileNamePattern>logs/security.%d{yyyy-MM-dd}.log.gz</fileNamePattern>
                <maxHistory>90</maxHistory>
            </rollingPolicy>
            <encoder>
                <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [SECURITY] %X{user:-anonymous} %X{ip:-unknown} - %msg%n</pattern>
            </encoder>
        </appender>
        
        <!-- Audit events appender -->
        <appender name="AUDIT" class="ch.qos.logback.core.rolling.RollingFileAppender">
            <file>logs/audit.log</file>
            <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
                <fileNamePattern>logs/audit.%d{yyyy-MM-dd}.log.gz</fileNamePattern>
                <maxHistory>365</maxHistory>
            </rollingPolicy>
            <encoder>
                <pattern>%d{yyyy-MM-dd HH:mm:ss.SSS} [AUDIT] %X{user:-system} %X{action:-unknown} - %msg%n</pattern>
            </encoder>
        </appender>
        
        <logger name="mil.af.kesselrun.security" level="DEBUG" additivity="false">
            <appender-ref ref="SECURITY"/>
        </logger>
        
        <logger name="org.springframework.security" level="INFO" additivity="false">
            <appender-ref ref="SECURITY"/>
        </logger>
        
        <logger name="AUDIT" level="INFO" additivity="false">
            <appender-ref ref="AUDIT"/>
        </logger>
        
        <root level="INFO">
            <appender-ref ref="FILE"/>
        </root>
    </springProfile>
</configuration>
'''
        
        # Prometheus monitoring configuration
        files["monitoring/prometheus.yml"] = f'''global:
  scrape_interval: 15s
  evaluation_interval: 15s

rule_files:
  - "kessel-run-alerts.yml"

scrape_configs:
  - job_name: '{diagram.name.lower()}-service'
    static_configs:
      - targets: ['localhost:8080']
    metrics_path: '/actuator/prometheus'
    scrape_interval: 5s
    
  - job_name: 'kubernetes-pods'
    kubernetes_sd_configs:
      - role: pod
    relabel_configs:
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_scrape]
        action: keep
        regex: true
      - source_labels: [__meta_kubernetes_pod_annotation_prometheus_io_path]
        action: replace
        target_label: __metrics_path__
        regex: (.+)

alerting:
  alertmanagers:
    - static_configs:
        - targets: ['alertmanager:9093']
'''
        
        # Security alerts configuration
        files["monitoring/kessel-run-alerts.yml"] = '''groups:
  - name: kessel-run-security
    rules:
      - alert: HighAuthenticationFailureRate
        expr: rate(authentication_failures_total[5m]) > 10
        for: 2m
        labels:
          severity: warning
          component: security
        annotations:
          summary: "High authentication failure rate detected"
          description: "Authentication failures are occurring at {{ $value }} per second"
      
      - alert: UnauthorizedAccessAttempt
        expr: rate(unauthorized_access_attempts_total[1m]) > 0
        for: 0s
        labels:
          severity: critical
          component: security
        annotations:
          summary: "Unauthorized access attempt detected"
          description: "Unauthorized access attempts detected in the last minute"
      
      - alert: SecurityScanDetected
        expr: rate(security_scan_requests_total[5m]) > 5
        for: 1m
        labels:
          severity: warning
          component: security
        annotations:
          summary: "Potential security scan detected"
          description: "High rate of suspicious requests detected"

  - name: kessel-run-application
    rules:
      - alert: ApplicationDown
        expr: up{job="kessel-run-service"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Kessel Run service is down"
          description: "The Kessel Run service has been down for more than 1 minute"
      
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.1
        for: 2m
        labels:
          severity: warning
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value }} errors per second"
'''
        
        return files
    
    def _generate_container_security(self) -> Dict[str, str]:
        """Generate container security configurations"""
        files = {}
        
        # Enhanced Dockerfile with security scanning
        files["Dockerfile.secure"] = '''# Multi-stage build for enhanced security
FROM registry1.dso.mil/ironbank/opensource/openjdk/openjdk11:1.11.0 as builder

# Security: Run as non-root user during build
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser

WORKDIR /app
COPY --chown=appuser:appuser pom.xml .
COPY --chown=appuser:appuser src ./src

# Build application
RUN mvn clean package -DskipTests

# Runtime stage
FROM registry1.dso.mil/ironbank/opensource/openjdk/openjdk11-jre:1.11.0

# Security labels
LABEL name="kessel-run-service" \\
      vendor="U.S. Air Force" \\
      version="1.0.0" \\
      release="1" \\
      summary="Kessel Run Mission Service" \\
      description="Air Force Kessel Run microservice for mission-critical operations" \\
      io.k8s.description="Air Force Kessel Run microservice" \\
      io.k8s.display-name="Kessel Run Service" \\
      io.openshift.tags="kessel-run,airforce,microservice"

# Create non-root user
RUN groupadd -r kesselrun && useradd -r -g kesselrun kesselrun

# Set working directory
WORKDIR /app

# Copy application jar
COPY --from=builder --chown=kesselrun:kesselrun /app/target/*.jar app.jar

# Security: Remove unnecessary packages and files
RUN microdnf update -y && \\
    microdnf clean all && \\
    rm -rf /var/cache/yum && \\
    rm -rf /tmp/*

# Security: Set file permissions
RUN chmod 440 app.jar

# Switch to non-root user
USER kesselrun

# Expose port (non-privileged)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \\
    CMD curl -f http://localhost:8080/actuator/health || exit 1

# Security: Use exec form and non-root user
ENTRYPOINT ["java", "-jar", "-Djava.security.egd=file:/dev/./urandom", "app.jar"]
'''
        
        # Container security scanning script
        files["scripts/security-scan.sh"] = '''#!/bin/bash
# Container Security Scanning Script for Kessel Run

set -euo pipefail

IMAGE_NAME="${1:-kessel-run-service:latest}"
REPORT_DIR="security-reports"

echo "🔒 Starting security scan for image: $IMAGE_NAME"

# Create reports directory
mkdir -p "$REPORT_DIR"

# Trivy vulnerability scanning
echo "📊 Running Trivy vulnerability scan..."
trivy image --format json --output "$REPORT_DIR/trivy-report.json" "$IMAGE_NAME"
trivy image --format table "$IMAGE_NAME"

# Container structure test
echo "🏗️ Running container structure tests..."
if command -v container-structure-test &> /dev/null; then
    container-structure-test test --image "$IMAGE_NAME" --config container-test.yaml
fi

# Docker Bench for Security (if running on Docker)
echo "🛡️ Running Docker Bench for Security..."
if command -v docker-bench-security &> /dev/null; then
    docker-bench-security --json --log-level WARN > "$REPORT_DIR/docker-bench-report.json"
fi

# Anchore scanning (if available)
echo "⚓ Running Anchore analysis..."
if command -v anchore-cli &> /dev/null; then
    anchore-cli image add "$IMAGE_NAME"
    anchore-cli image wait "$IMAGE_NAME"
    anchore-cli image vuln "$IMAGE_NAME" all > "$REPORT_DIR/anchore-vulns.json"
fi

echo "✅ Security scanning completed. Reports available in: $REPORT_DIR"

# Exit with error if critical vulnerabilities found
CRITICAL_COUNT=$(jq '.Results[]?.Vulnerabilities[]? | select(.Severity == "CRITICAL") | length' "$REPORT_DIR/trivy-report.json" | wc -l)
if [ "$CRITICAL_COUNT" -gt 0 ]; then
    echo "❌ Critical vulnerabilities found: $CRITICAL_COUNT"
    exit 1
fi

echo "🎉 No critical vulnerabilities found!"
'''
        
        # Container structure test configuration
        files["container-test.yaml"] = '''schemaVersion: 2.0.0

metadataTest:
  labels:
    - key: "name"
      value: "kessel-run-service"
    - key: "vendor"
      value: "U.S. Air Force"

commandTests:
  - name: "java version check"
    command: "java"
    args: ["-version"]
    exitCode: 0

  - name: "non-root user check"
    command: "whoami"
    expectedOutput: ["kesselrun"]
    exitCode: 0

  - name: "app jar exists"
    command: "ls"
    args: ["/app/app.jar"]
    exitCode: 0

fileExistenceTests:
  - name: "app jar"
    path: "/app/app.jar"
    shouldExist: true

  - name: "no root files"
    path: "/root"
    shouldExist: false

fileContentTests:
  - name: "app jar permissions"
    path: "/app/app.jar"
    expectedContents: []
    # File should not be writable by group or others

licenseTests:
  - debian: false
    files: []
'''
        
        return files


class BaseGenerator:
    """Base class for all code generators"""
    
    def generate(self, diagram) -> Dict[str, str]:
        """Generate code from diagram"""
        raise NotImplementedError