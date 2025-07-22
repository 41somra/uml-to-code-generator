# DoD Platform One Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the Model-to-Code Generator on DoD Platform One.

## Prerequisites

### Access Requirements
- [ ] DoD Platform One account
- [ ] CAC authentication configured  
- [ ] Access to target Platform One environment
- [ ] Appropriate security clearance
- [ ] RBAC permissions for deployment

### Technical Prerequisites
- [ ] Iron Bank container registry access
- [ ] Kubernetes cluster access
- [ ] GitLab CI/CD runner access
- [ ] Security scanning tools configured

## Deployment Steps

### 1. Prepare Security Documentation
```bash
# Complete security requirements
- Authority to Operate (ATO) documentation
- Risk Management Framework (RMF) assessment
- FISMA compliance documentation
- DISA STIG compliance verification
```

### 2. Container Image Preparation
```bash
# Build Iron Bank compliant image
docker build -f Dockerfile.ironbank -t registry1.dso.mil/yourorg/model-to-code:v1.0.0 .

# Security scan the image
trivy image registry1.dso.mil/yourorg/model-to-code:v1.0.0

# Push to Iron Bank registry
docker push registry1.dso.mil/yourorg/model-to-code:v1.0.0
```

### 3. Kubernetes Deployment
```bash
# Apply namespace and RBAC
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/rbac.yaml

# Apply security policies
kubectl apply -f k8s/security-policies.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml

# Verify deployment
kubectl get pods -n model-to-code
kubectl get services -n model-to-code
```

### 4. Security Validation
```bash
# Run security scans
kubectl run --rm -it security-scan --image=registry1.dso.mil/ironbank/aquasec/trivy:latest -- trivy k8s cluster

# Verify network policies
kubectl get networkpolicies -n model-to-code

# Check pod security
kubectl get pods -n model-to-code -o jsonpath='{.items[*].spec.securityContext}'
```

### 5. Testing and Validation
```bash
# Health check
curl -k https://model-to-code.apps.dso.mil/health

# Functional testing
curl -k https://model-to-code.apps.dso.mil/api/sample

# Security testing
nmap -sS model-to-code.apps.dso.mil
```

## Security Considerations

### Container Security
- Uses Iron Bank hardened base images
- Runs as non-root user
- Read-only root filesystem
- Minimal attack surface

### Network Security
- TLS encryption enforced
- Network policies implemented
- Istio service mesh integration
- Ingress/egress controls

### Application Security
- Input validation implemented
- No persistent data storage
- Secure coding practices
- Regular security scanning

## Monitoring and Maintenance

### Health Monitoring
```bash
# Check application health
kubectl get pods -n model-to-code -w

# View logs
kubectl logs -f deployment/model-to-code-generator -n model-to-code

# Monitor resources
kubectl top pods -n model-to-code
```

### Security Monitoring
```bash
# Security scan alerts
kubectl get events -n model-to-code --field-selector type=Warning

# Network policy violations
kubectl logs -n istio-system -l app=istiod | grep "policy violation"
```

### Updates and Patches
```bash
# Update container image
kubectl set image deployment/model-to-code-generator model-to-code-generator=registry1.dso.mil/yourorg/model-to-code:v1.0.1 -n model-to-code

# Security patch process
kubectl rollout restart deployment/model-to-code-generator -n model-to-code
```

## Troubleshooting

### Common Issues

#### Image Pull Errors
```bash
# Check registry access
kubectl get secrets -n model-to-code
kubectl describe pod <pod-name> -n model-to-code
```

#### Network Connectivity
```bash
# Test service connectivity
kubectl exec -it <pod-name> -n model-to-code -- curl localhost:8080/health

# Check DNS resolution
kubectl exec -it <pod-name> -n model-to-code -- nslookup kubernetes.default
```

#### Security Policy Violations
```bash
# Check security context
kubectl describe pod <pod-name> -n model-to-code

# Review security policies
kubectl describe psp model-to-code-psp
```

## Compliance and Governance

### Required Documentation
- [ ] System Security Plan (SSP)
- [ ] Risk Assessment Report
- [ ] Security Control Assessment
- [ ] Plan of Action and Milestones (POA&M)
- [ ] Continuous Monitoring Strategy

### Audit and Compliance
- Monthly security scans
- Quarterly compliance reviews
- Annual risk assessments
- Continuous monitoring

## Contact Information

### Platform One Support
- **Environment Support**: platform-one-support@dso.mil
- **Security Team**: security@dso.mil
- **Operations**: ops@dso.mil

### Application Support
- **Development Team**: [Your Contact]
- **Security Officer**: [Security Contact]
- **System Administrator**: [Admin Contact]

## References
- [Platform One Documentation](https://repo1.dso.mil/platform-one/big-bang/bigbang)
- [Iron Bank Documentation](https://repo1.dso.mil/dsop/dccscr)
- [DoD DevSecOps Reference Design](https://dodcio.defense.gov/Portals/0/Documents/DoD%20Enterprise%20DevSecOps%20Reference%20Design%20v1.0_Public%20Release.pdf)
- [NIST 800-190 Container Security](https://csrc.nist.gov/publications/detail/sp/800-190/final)