# Simple Text Diagram API Documentation

## Overview
This is the official API documentation for the Simple Text Diagram system, developed for Air Force Kessel Run mission-critical operations.

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
{
  "data": { ... },
  "status": "success",
  "timestamp": "2024-01-01T00:00:00Z"
}
```

### Error Response
```json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human readable error message",
    "details": ["Additional error details"],
    "timestamp": "2024-01-01T00:00:00Z"
  }
}
```

## Entities


### Mission

**Description:** Mission entity for Air Force mission systems

**Attributes:**


**Endpoints:**
- `GET /missions` - List all Missions
- `GET /missions/{id}` - Get Mission by ID  
- `POST /missions` - Create new Mission
- `PUT /missions/{id}` - Update Mission
- `DELETE /missions/{id}` - Delete Mission


### MissionAsset

**Description:** MissionAsset entity for Air Force mission systems

**Attributes:**


**Endpoints:**
- `GET /missionassets` - List all MissionAssets
- `GET /missionassets/{id}` - Get MissionAsset by ID  
- `POST /missionassets` - Create new MissionAsset
- `PUT /missionassets/{id}` - Update MissionAsset
- `DELETE /missionassets/{id}` - Delete MissionAsset


### MissionPersonnel

**Description:** MissionPersonnel entity for Air Force mission systems

**Attributes:**


**Endpoints:**
- `GET /missionpersonnels` - List all MissionPersonnels
- `GET /missionpersonnels/{id}` - Get MissionPersonnel by ID  
- `POST /missionpersonnels` - Create new MissionPersonnel
- `PUT /missionpersonnels/{id}` - Update MissionPersonnel
- `DELETE /missionpersonnels/{id}` - Delete MissionPersonnel


### RiskAssessment

**Description:** RiskAssessment entity for Air Force mission systems

**Attributes:**


**Endpoints:**
- `GET /riskassessments` - List all RiskAssessments
- `GET /riskassessments/{id}` - Get RiskAssessment by ID  
- `POST /riskassessments` - Create new RiskAssessment
- `PUT /riskassessments/{id}` - Update RiskAssessment
- `DELETE /riskassessments/{id}` - Delete RiskAssessment


### Intelligence

**Description:** Intelligence entity for Air Force mission systems

**Attributes:**


**Endpoints:**
- `GET /intelligences` - List all Intelligences
- `GET /intelligences/{id}` - Get Intelligence by ID  
- `POST /intelligences` - Create new Intelligence
- `PUT /intelligences/{id}` - Update Intelligence
- `DELETE /intelligences/{id}` - Delete Intelligence


### MissionStatus

**Description:** MissionStatus entity for Air Force mission systems

**Attributes:**


**Endpoints:**
- `GET /missionstatuss` - List all MissionStatuss
- `GET /missionstatuss/{id}` - Get MissionStatus by ID  
- `POST /missionstatuss` - Create new MissionStatus
- `PUT /missionstatuss/{id}` - Update MissionStatus
- `DELETE /missionstatuss/{id}` - Delete MissionStatus



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
