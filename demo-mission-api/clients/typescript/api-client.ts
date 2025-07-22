/**
 * Simple Text Diagram API Client
 * Generated TypeScript client for Air Force Kessel Run
 */

export interface ApiConfig {
  baseUrl: string;
  apiKey?: string;
  token?: string;
  timeout?: number;
}

export interface ApiResponse<T> {
  data: T;
  status: number;
  statusText: string;
  headers: Record<string, string>;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: string[];
    timestamp: string;
  };
}

export interface PageResponse<T> {
  content: T[];
  pageable: {
    page: number;
    size: number;
    sort: string;
  };
  totalElements: number;
  totalPages: number;
  first: boolean;
  last: boolean;
}

// Entity interfaces

export interface Mission {
  id: number;
  createdAt: string;
  updatedAt: string;
}

export interface MissionCreateRequest {
}

export interface MissionUpdateRequest {
}

export interface MissionAsset {
  id: number;
  createdAt: string;
  updatedAt: string;
}

export interface MissionAssetCreateRequest {
}

export interface MissionAssetUpdateRequest {
}

export interface MissionPersonnel {
  id: number;
  createdAt: string;
  updatedAt: string;
}

export interface MissionPersonnelCreateRequest {
}

export interface MissionPersonnelUpdateRequest {
}

export interface RiskAssessment {
  id: number;
  createdAt: string;
  updatedAt: string;
}

export interface RiskAssessmentCreateRequest {
}

export interface RiskAssessmentUpdateRequest {
}

export interface Intelligence {
  id: number;
  createdAt: string;
  updatedAt: string;
}

export interface IntelligenceCreateRequest {
}

export interface IntelligenceUpdateRequest {
}

export interface MissionStatus {
  id: number;
  createdAt: string;
  updatedAt: string;
}

export interface MissionStatusCreateRequest {
}

export interface MissionStatusUpdateRequest {
}

export class Simple Text DiagramApiClient {
  private config: ApiConfig;
  
  constructor(config: ApiConfig) {
    this.config = config;
  }
  
  private async request<T>(
    method: string, 
    path: string, 
    data?: any, 
    params?: Record<string, any>
  ): Promise<ApiResponse<T>> {
    const url = new URL(path, this.config.baseUrl);
    
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.append(key, String(value));
        }
      });
    }
    
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
    };
    
    if (this.config.token) {
      headers['Authorization'] = `Bearer ${this.config.token}`;
    }
    
    if (this.config.apiKey) {
      headers['X-API-Key'] = this.config.apiKey;
    }
    
    const response = await fetch(url.toString(), {
      method,
      headers,
      body: data ? JSON.stringify(data) : undefined,
      signal: AbortSignal.timeout(this.config.timeout || 30000)
    });
    
    const responseData = await response.json();
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status} - ${responseData.error?.message || response.statusText}`);
    }
    
    return {
      data: responseData,
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries())
    };
  }

  // Mission API methods
  async listMissions(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<Mission>>> {
    return this.request('GET', '/missions', undefined, { page, size, sort });
  }
  
  async getMission(id: number): Promise<ApiResponse<Mission>> {
    return this.request('GET', `/missions/${id}`);
  }
  
  async createMission(data: MissionCreateRequest): Promise<ApiResponse<Mission>> {
    return this.request('POST', '/missions', data);
  }
  
  async updateMission(id: number, data: MissionUpdateRequest): Promise<ApiResponse<Mission>> {
    return this.request('PUT', `/missions/${id}`, data);
  }
  
  async deleteMission(id: number): Promise<ApiResponse<void>> {
    return this.request('DELETE', `/missions/${id}`);
  }

  // MissionAsset API methods
  async listMissionAssets(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<MissionAsset>>> {
    return this.request('GET', '/missionassets', undefined, { page, size, sort });
  }
  
  async getMissionAsset(id: number): Promise<ApiResponse<MissionAsset>> {
    return this.request('GET', `/missionassets/${id}`);
  }
  
  async createMissionAsset(data: MissionAssetCreateRequest): Promise<ApiResponse<MissionAsset>> {
    return this.request('POST', '/missionassets', data);
  }
  
  async updateMissionAsset(id: number, data: MissionAssetUpdateRequest): Promise<ApiResponse<MissionAsset>> {
    return this.request('PUT', `/missionassets/${id}`, data);
  }
  
  async deleteMissionAsset(id: number): Promise<ApiResponse<void>> {
    return this.request('DELETE', `/missionassets/${id}`);
  }

  // MissionPersonnel API methods
  async listMissionPersonnels(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<MissionPersonnel>>> {
    return this.request('GET', '/missionpersonnels', undefined, { page, size, sort });
  }
  
  async getMissionPersonnel(id: number): Promise<ApiResponse<MissionPersonnel>> {
    return this.request('GET', `/missionpersonnels/${id}`);
  }
  
  async createMissionPersonnel(data: MissionPersonnelCreateRequest): Promise<ApiResponse<MissionPersonnel>> {
    return this.request('POST', '/missionpersonnels', data);
  }
  
  async updateMissionPersonnel(id: number, data: MissionPersonnelUpdateRequest): Promise<ApiResponse<MissionPersonnel>> {
    return this.request('PUT', `/missionpersonnels/${id}`, data);
  }
  
  async deleteMissionPersonnel(id: number): Promise<ApiResponse<void>> {
    return this.request('DELETE', `/missionpersonnels/${id}`);
  }

  // RiskAssessment API methods
  async listRiskAssessments(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<RiskAssessment>>> {
    return this.request('GET', '/riskassessments', undefined, { page, size, sort });
  }
  
  async getRiskAssessment(id: number): Promise<ApiResponse<RiskAssessment>> {
    return this.request('GET', `/riskassessments/${id}`);
  }
  
  async createRiskAssessment(data: RiskAssessmentCreateRequest): Promise<ApiResponse<RiskAssessment>> {
    return this.request('POST', '/riskassessments', data);
  }
  
  async updateRiskAssessment(id: number, data: RiskAssessmentUpdateRequest): Promise<ApiResponse<RiskAssessment>> {
    return this.request('PUT', `/riskassessments/${id}`, data);
  }
  
  async deleteRiskAssessment(id: number): Promise<ApiResponse<void>> {
    return this.request('DELETE', `/riskassessments/${id}`);
  }

  // Intelligence API methods
  async listIntelligences(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<Intelligence>>> {
    return this.request('GET', '/intelligences', undefined, { page, size, sort });
  }
  
  async getIntelligence(id: number): Promise<ApiResponse<Intelligence>> {
    return this.request('GET', `/intelligences/${id}`);
  }
  
  async createIntelligence(data: IntelligenceCreateRequest): Promise<ApiResponse<Intelligence>> {
    return this.request('POST', '/intelligences', data);
  }
  
  async updateIntelligence(id: number, data: IntelligenceUpdateRequest): Promise<ApiResponse<Intelligence>> {
    return this.request('PUT', `/intelligences/${id}`, data);
  }
  
  async deleteIntelligence(id: number): Promise<ApiResponse<void>> {
    return this.request('DELETE', `/intelligences/${id}`);
  }

  // MissionStatus API methods
  async listMissionStatuss(page = 0, size = 20, sort?: string): Promise<ApiResponse<PageResponse<MissionStatus>>> {
    return this.request('GET', '/missionstatuss', undefined, { page, size, sort });
  }
  
  async getMissionStatus(id: number): Promise<ApiResponse<MissionStatus>> {
    return this.request('GET', `/missionstatuss/${id}`);
  }
  
  async createMissionStatus(data: MissionStatusCreateRequest): Promise<ApiResponse<MissionStatus>> {
    return this.request('POST', '/missionstatuss', data);
  }
  
  async updateMissionStatus(id: number, data: MissionStatusUpdateRequest): Promise<ApiResponse<MissionStatus>> {
    return this.request('PUT', `/missionstatuss/${id}`, data);
  }
  
  async deleteMissionStatus(id: number): Promise<ApiResponse<void>> {
    return this.request('DELETE', `/missionstatuss/${id}`);
  }
}
