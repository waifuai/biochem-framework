#!/usr/bin/env python3
"""
OpenRouter API Client
Handles communication with OpenRouter API for biochemistry analysis.
"""

import os
import requests

from pathlib import Path
from typing import Optional, Dict, Any


class OpenRouterClient:
    """Client for interacting with the OpenRouter API."""
    
    BASE_URL = "https://openrouter.ai/api/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the OpenRouter client.
        
        Args:
            api_key: OpenRouter API key. If not provided, reads from 
                     ~/.api-openrouter file or OPENROUTER_API_KEY env var.
        """
        self.api_key = api_key
        
        # Try reading from ~/.api-openrouter file
        if not self.api_key:
            api_file = Path.home() / ".api-openrouter"
            if api_file.exists():
                try:
                    self.api_key = api_file.read_text().strip()
                except IOError:
                    pass
        
        # Fallback to environment variable
        if not self.api_key:
            self.api_key = os.environ.get("OPENROUTER_API_KEY")
        
        if not self.api_key:
            raise ValueError(
                "OpenRouter API key required. Create ~/.api-openrouter file "
                "or set OPENROUTER_API_KEY environment variable."
            )
    
    def _get_headers(self) -> Dict[str, str]:
        """Get headers for API requests."""
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
    
    def generate(
        self, 
        model: str, 
        prompt: str,
        max_tokens: int = 4096,
        temperature: float = 0.3
    ) -> Dict[str, Any]:
        """
        Generate a completion from a model.
        
        Args:
            model: Model identifier (e.g., "openai/gpt-4", "anthropic/claude-3-opus")
            prompt: The prompt to send to the model
            max_tokens: Maximum tokens in response
            temperature: Sampling temperature
            
        Returns:
            Dict with 'content' (response text) and 'usage' (token counts)
        """
        url = f"{self.BASE_URL}/chat/completions"
        
        payload = {
            "model": model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": temperature
        }
        
        try:
            response = requests.post(
                url, 
                headers=self._get_headers(),
                json=payload,
                timeout=120
            )
            response.raise_for_status()
            
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 401:
                raise ValueError("Invalid OpenRouter API key")
            elif e.response.status_code == 429:
                raise RuntimeError("Rate limit exceeded")
            elif e.response.status_code == 400:
                error_msg = e.response.json().get("error", {}).get("message", str(e))
                raise ValueError(f"Bad request: {error_msg}")
            elif e.response.status_code >= 500:
                raise RuntimeError(f"Server error {e.response.status_code}")
            else:
                raise RuntimeError(f"API error: {e}")
        
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Request failed: {e}")
        
        data = response.json()
            
        content = data.get("choices", [{}])[0].get("message", {}).get("content", "")
        usage = data.get("usage", {})
        
        return {
            "content": content,
            "usage": {
                "prompt_tokens": usage.get("prompt_tokens", 0),
                "completion_tokens": usage.get("completion_tokens", 0),
                "total_tokens": usage.get("total_tokens", 0)
            },
            "model": data.get("model", model)
        }


if __name__ == "__main__":
    # Quick test
    try:
        client = OpenRouterClient()
        print("[OK] OpenRouter client initialized")
    except ValueError as e:
        print(f"[ERROR] {e}")
