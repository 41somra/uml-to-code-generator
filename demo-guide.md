# Kessel Run Demo Guide

## Quick Demo Commands

```bash
# 1. Generate complete microservices architecture
python main.py -i examples/mission_planning.txt -l microservices

# 2. Generate API-first development artifacts  
python main.py -i examples/mission_planning.txt -l openapi

# 3. Generate DevSecOps security configurations
python main.py -i examples/mission_planning.txt -l devsecops
```

## Demo Script (5 minutes)

### Opening (30 seconds)
"This is our Model-to-Code Generator with Kessel Run features - transforming Air Force mission requirements into production-ready code in seconds."

### Live Demo (3 minutes)

**Step 1: Show Input** (30 seconds)
```bash
cat examples/mission_planning.txt
```
"Simple text describing mission entities becomes..."

**Step 2: Generate Microservices** (60 seconds)
```bash
python main.py -i examples/mission_planning.txt -l microservices
```
Show generated output:
- 35 enterprise files
- Spring Boot services
- Kubernetes deployments
- Docker security configs

**Step 3: Show Generated Code** (60 seconds)
```bash
# Show Spring Boot entity
cat mission-demo/common-service/src/main/java/mil/af/kesselrun/commonservice/entity/Mission.java

# Show Kubernetes deployment
cat mission-demo/common-service/k8s/deployment.yaml
```

**Step 4: Generate APIs** (30 seconds)
```bash
python main.py -i examples/mission_planning.txt -l openapi
```
Show OpenAPI spec and generated clients.

### Impact Statement (90 seconds)
"Traditional development: 2-3 weeks
With Kessel Run generator: 30 seconds

**Key Benefits:**
- 20x faster development
- Built-in DoD security compliance
- FISMA/STIG ready
- Kubernetes native
- Auto-generated documentation"

## Demo Files to Highlight

### Microservices
- `mission-demo/common-service/src/main/java/mil/af/kesselrun/commonservice/Application.java`
- `mission-demo/common-service/k8s/deployment.yaml`
- `mission-demo/common-service/Dockerfile`

### APIs  
- `demo-mission-api/api/openapi.yaml`
- `demo-mission-api/clients/typescript/src/apis/MissionApi.ts`

### Security
- `demo-mission-secure/scripts/security-scan.sh`
- `demo-mission-secure/container-test.yaml`

## Questions & Answers

**Q: "Is this production ready?"**
A: "Yes - includes Spring Security, JWT auth, container hardening, and DoD compliance patterns."

**Q: "What about existing systems?"**  
A: "Generated APIs integrate with existing systems via REST/OpenAPI standards."

**Q: "How do we customize?"**
A: "Templates are configurable, and generated code is standard Spring Boot - fully customizable."

## Technical Deep Dive (Optional)

If audience wants technical details:

1. **Architecture**: Show service mesh patterns in Kubernetes configs
2. **Security**: Demonstrate RBAC, JWT validation, container scanning
3. **APIs**: Show auto-generated client SDKs in multiple languages
4. **DevOps**: GitLab CI/CD pipelines with security gates

## Demo Setup (Pre-demo)

```bash
# Ensure Python dependencies
pip install -r requirements.txt

# Clear previous demo output
rm -rf mission-demo demo-mission-* 

# Test commands work
python main.py -i examples/mission_planning.txt -l microservices > /dev/null
```