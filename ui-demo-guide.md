# UI Demo Guide - Kessel Run Model-to-Code Generator

## Starting the Web Interface

```bash
# Start the web UI
python main.py --web
```

The system will automatically find an available port (5000, 5001, 5002, 8000, or 8080) and display:
```
Starting Model-to-Code Generator web interface...
Trying to start server on http://localhost:5000
```

## Live Demo Flow (Web Interface)

### 1. Opening the Web Interface (30 seconds)
```bash
python main.py --web
```
Navigate to `http://localhost:5000` in browser

**Show the interface:**
- Clean, professional UI
- Input text area for model definitions
- Language/architecture selector
- Generate button

### 2. Demo Input (60 seconds)
**Copy and paste mission planning example:**
```
Mission:
  id: int
  missionCode: string
  title: string
  objective: string
  classification: string
  priority: string
  status: string
  plannedStartDate: datetime
  plannedEndDate: datetime
  commanderId: int
  createMission()
  approveMission()
  executeMission()

MissionAsset:
  id: int
  missionId: int
  assetType: string
  assetId: string
  status: string
  deployedDate: datetime
  assignAssetToMission()
  updateAssetStatus()

MissionPersonnel:
  id: int
  missionId: int
  personnelId: int
  role: string
  rank: string
  clearanceLevel: string
  assignedDate: datetime
  assignPersonnelToMission()
  updateRole()
```

### 3. Live Generation Demo (2 minutes)

**Step 1: Microservices Generation**
- Select "microservices" from dropdown
- Click "Generate Code"
- **Show real-time output:**
  - Progress indicator
  - File count increasing (35 files)
  - Generated file tree structure

**Step 2: Show Generated Files**
- Expandable file tree in UI
- Click on different files to preview:
  - `Mission.java` - Spring Boot entity
  - `deployment.yaml` - Kubernetes config
  - `Dockerfile` - Container configuration

**Step 3: API Generation**
- Change selector to "openapi"
- Click "Generate Code" again
- Show OpenAPI specification viewer
- Display generated client SDKs

### 4. Interactive Features Demo (90 seconds)

**File Browser:**
- Click through generated file structure
- Syntax highlighting for different file types
- Download individual files or entire project as ZIP

**Code Preview:**
- Show live code preview with syntax highlighting
- Demonstrate different file types:
  - Java Spring Boot services
  - YAML Kubernetes manifests
  - Shell scripts for security scanning

**Validation:**
- Show input validation (try invalid syntax)
- Error messages and helpful suggestions

## Browser Demo Script

### Opening Statement
"Let me show you the web interface - making Kessel Run code generation accessible to any team member, no command line needed."

### Live Demonstration

1. **Launch Interface:**
   ```bash
   python main.py --web
   ```
   "Web interface launches on localhost:5000"

2. **Input Mission Requirements:**
   - Paste mission planning model
   - "Simple text input - no special syntax required"

3. **Generate Microservices:**
   - Select "microservices"
   - Click generate
   - "Watch as 35 enterprise files are created in real-time"

4. **Explore Generated Code:**
   - Browse file tree
   - Open Mission.java
   - Show Kubernetes deployment
   - "Production-ready Spring Boot microservices"

5. **Generate APIs:**
   - Switch to "openapi"
   - Generate again
   - Show OpenAPI spec
   - "Complete API documentation and client SDKs"

### Key UI Features to Highlight

**User Experience:**
- No technical expertise required
- Instant feedback and validation
- Professional code output with syntax highlighting
- Download capabilities for immediate use

**Enterprise Features:**
- Multiple architecture patterns
- Security-first approach
- DoD compliance built-in
- Kubernetes-ready deployments

## Demo Flow Comparison

| Traditional Development | With Kessel Run UI |
|------------------------|-------------------|
| Weeks of planning      | 30 seconds input  |
| Manual coding          | Automated generation |
| Security afterthought  | Built-in compliance |
| Manual documentation   | Auto-generated APIs |
| Complex deployment     | Kubernetes ready  |

## Audience Interaction

**For Technical Audience:**
- Show generated Spring Boot code quality
- Demonstrate Kubernetes manifests
- Highlight security configurations

**For Management Audience:**
- Focus on time savings (20x faster)
- Emphasize cost reduction
- Show compliance automation

**For End Users:**
- Demonstrate ease of use
- No command line required
- Instant results

## Technical Setup Notes

```bash
# Pre-demo setup
cd /Users/ricksomra/expense-tracker-ai/fitness-pal/model-to-code

# Ensure all dependencies
pip install -r requirements.txt

# Clear any previous output
rm -rf generated/ mission-demo/ demo-mission-*

# Start web interface
python main.py --web
```

## Backup Demo (If Web Interface Issues)

If web interface fails, fall back to CLI demo:
```bash
# Quick CLI demo
python main.py -i examples/mission_planning.txt -l microservices
ls -la mission-demo/
cat mission-demo/common-service/src/main/java/mil/af/kesselrun/commonservice/entity/Mission.java
```

## Demo Success Metrics

**What to measure:**
- Time from input to generated code (< 30 seconds)
- Number of files generated (35+ for microservices)
- Audience engagement (questions about implementation)
- Follow-up interest (requests for trials/POCs)

The web interface makes the powerful Kessel Run features accessible to any Air Force team member, regardless of technical background.