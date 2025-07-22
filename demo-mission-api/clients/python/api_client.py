"""
Simple Text Diagram API Client for Air Force Kessel Run
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


class Simple Text DiagramApiClient:
    """API client for Simple Text Diagram service"""
    
    def __init__(self, config: ApiConfig):
        self.config = config
        self.session = requests.Session()
        
        if config.token:
            self.session.headers.update({"Authorization": f"Bearer {config.token}"})
        
        if config.api_key:
            self.session.headers.update({"X-API-Key": config.api_key})
    
    def _request(self, method: str, path: str, data: Any = None, params: Dict = None) -> Dict:
        """Make HTTP request to API"""
        url = f"{self.config.base_url}{path}"
        
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
            raise Exception(f"API request failed: {str(e)}")
