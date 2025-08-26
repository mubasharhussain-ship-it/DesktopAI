"""
LLM Interface Module
Handles communication with Ollama for local LLM inference.
"""

import os
import json
import base64
import logging
import requests
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Any


class LLMInterface:
    """Interface for communicating with local LLM via Ollama."""
    
    def __init__(self, config):
        """Initialize LLM interface."""
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.ollama_url = "http://localhost:11434"
        self.model_name = config.get_llm_model()
        self.rules = self._load_rules()
    
    def _load_rules(self) -> str:
        """Load automation rules from rules.txt file."""
        try:
            rules_path = Path("data/rules.txt")
            if rules_path.exists():
                with open(rules_path, 'r', encoding='utf-8') as f:
                    return f.read().strip()
            else:
                return self._get_default_rules()
        except Exception as e:
            self.logger.error(f"Error loading rules: {str(e)}")
            return self._get_default_rules()
    
    def _get_default_rules(self) -> str:
        """Get default automation rules."""
        return """
AUTOMATION SAFETY RULES:
1. Never perform destructive actions like deleting files or formatting drives
2. Never access sensitive information or passwords
3. Always confirm actions that might affect system settings
4. Prefer safe, reversible actions
5. If unsure about an action, request clarification
6. Never automate actions that could harm the system or user data
7. Focus on productivity and user assistance tasks
8. Avoid clicking on suspicious links or downloads
9. Never perform financial transactions without explicit confirmation
10. Always respect user privacy and security

RESPONSE FORMAT:
Always respond with valid JSON containing:
{
    "action": "click|type|key|scroll|wait",
    "coordinates": [x, y] (for click actions),
    "text": "text to type" (for type actions),
    "key": "key name" (for key actions like 'enter', 'tab', 'ctrl+c'),
    "direction": "up|down|left|right" (for scroll actions),
    "amount": number (for scroll amount),
    "duration": seconds (for wait actions),
    "reasoning": "explanation of why this action was chosen"
}
"""
    
    def initialize(self) -> bool:
        """Initialize Ollama and ensure model is available."""
        try:
            # Check if Ollama is running
            if not self._is_ollama_running():
                self.logger.info("Starting Ollama service...")
                if not self._start_ollama():
                    self.logger.error("Failed to start Ollama service")
                    return False
            
            # Check if model is available
            if not self._is_model_available():
                self.logger.info(f"Downloading model: {self.model_name}")
                if not self._download_model():
                    self.logger.error(f"Failed to download model: {self.model_name}")
                    return False
            
            # Test model inference
            if not self._test_model():
                self.logger.error("Model test failed")
                return False
            
            self.logger.info("LLM interface initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Error initializing LLM interface: {str(e)}")
            return False
    
    def _is_ollama_running(self) -> bool:
        """Check if Ollama service is running."""
        try:
            response = requests.get(f"{self.ollama_url}/api/version", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def _start_ollama(self) -> bool:
        """Start Ollama service."""
        try:
            # Try to start Ollama
            subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            # Wait for service to start
            import time
            for _ in range(30):  # Wait up to 30 seconds
                if self._is_ollama_running():
                    return True
                time.sleep(1)
            
            return False
        except Exception as e:
            self.logger.error(f"Error starting Ollama: {str(e)}")
            return False
    
    def _is_model_available(self) -> bool:
        """Check if the required model is available."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code != 200:
                return False
            
            models = response.json().get("models", [])
            model_names = [model.get("name", "").split(":")[0] for model in models]
            
            return self.model_name in model_names
        except Exception as e:
            self.logger.error(f"Error checking model availability: {str(e)}")
            return False
    
    def _download_model(self) -> bool:
        """Download the required model."""
        try:
            self.logger.info(f"Pulling model: {self.model_name}")
            
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": self.model_name},
                stream=True,
                timeout=300
            )
            
            if response.status_code != 200:
                return False
            
            # Process streaming response
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if data.get("status") == "success":
                            self.logger.info("Model download completed")
                            return True
                    except json.JSONDecodeError:
                        continue
            
            return True
        except Exception as e:
            self.logger.error(f"Error downloading model: {str(e)}")
            return False
    
    def _test_model(self) -> bool:
        """Test model inference."""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": "Hello, respond with 'OK' if you can understand this message.",
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if "response" in result:
                    self.logger.info("Model test successful")
                    return True
            
            return False
        except Exception as e:
            self.logger.error(f"Error testing model: {str(e)}")
            return False
    
    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64 for LLM input."""
        try:
            with open(image_path, "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            self.logger.error(f"Error encoding image: {str(e)}")
            return ""
    
    def analyze_screen_and_command(self, screenshot_path: str, command: str) -> Optional[Dict[str, Any]]:
        """Analyze screen and user command to determine action."""
        try:
            # Encode screenshot
            image_base64 = self._encode_image(screenshot_path)
            if not image_base64:
                self.logger.error("Failed to encode screenshot")
                return None
            
            # Create prompt
            prompt = self._create_analysis_prompt(command)
            
            # Send request to LLM
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "images": [image_base64],
                    "stream": False,
                    "options": {
                        "temperature": 0.1,  # Low temperature for consistent responses
                        "top_p": 0.9
                    }
                },
                timeout=60
            )
            
            if response.status_code != 200:
                self.logger.error(f"LLM request failed: {response.status_code}")
                return None
            
            result = response.json()
            llm_response = result.get("response", "")
            
            # Parse LLM response
            decision = self._parse_llm_response(llm_response)
            
            if decision:
                self.logger.info(f"LLM decision: {decision}")
                return decision
            else:
                self.logger.error("Failed to parse LLM response")
                return None
                
        except Exception as e:
            self.logger.error(f"Error in LLM analysis: {str(e)}")
            return None
    
    def _create_analysis_prompt(self, command: str) -> str:
        """Create analysis prompt for the LLM."""
        # Check if command involves internet-dependent apps
        internet_dependent_keywords = [
            'chrome', 'firefox', 'edge', 'browser', 'outlook', 'email', 
            'teams', 'discord', 'steam', 'spotify', 'youtube', 'google',
            'internet', 'online', 'web', 'gmail', 'facebook', 'twitter'
        ]
        
        needs_internet = any(keyword in command.lower() for keyword in internet_dependent_keywords)
        
        internet_context = ""
        if needs_internet:
            # Check internet connectivity
            try:
                import requests
                response = requests.get("http://www.google.com", timeout=3)
                internet_available = response.status_code == 200
            except:
                internet_available = False
            
            if not internet_available:
                internet_context = """
IMPORTANT: This command requires internet connectivity, but internet is not currently available.
You should respond with a wait action and explain that you're waiting for internet connectivity.
Example response: {"action": "wait", "duration": 5, "reasoning": "Waiting for internet connection to open Chrome"}
"""
            else:
                internet_context = """
INTERNET STATUS: Internet connection is available. You can proceed with internet-dependent actions.
"""
        
        return f"""
You are an AI desktop automation assistant. You can see the current desktop screenshot and need to decide what action to take based on the user's command.

RULES AND GUIDELINES:
{self.rules}

{internet_context}

USER COMMAND: {command}

Analyze the screenshot and determine the appropriate action to fulfill the user's command. Consider:
1. What UI elements are visible on the screen
2. Where should I click or what should I type to accomplish the task
3. What is the most logical next step
4. If the command requires internet and it's not available, wait for connectivity

Respond ONLY with valid JSON in the exact format specified in the rules. Do not include any other text or explanation outside the JSON.
"""
    
    def _parse_llm_response(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse LLM response and extract action decision."""
        try:
            # Clean response - look for JSON content
            response = response.strip()
            
            # Try to find JSON in the response
            start_idx = response.find('{')
            end_idx = response.rfind('}')
            
            if start_idx >= 0 and end_idx >= start_idx:
                json_str = response[start_idx:end_idx + 1]
                decision = json.loads(json_str)
                
                # Validate required fields
                if self._validate_decision(decision):
                    return decision
            
            self.logger.error(f"Invalid LLM response format: {response}")
            return None
            
        except json.JSONDecodeError as e:
            self.logger.error(f"JSON parsing error: {str(e)}")
            return None
        except Exception as e:
            self.logger.error(f"Error parsing LLM response: {str(e)}")
            return None
    
    def _validate_decision(self, decision: Dict[str, Any]) -> bool:
        """Validate LLM decision format."""
        if not isinstance(decision, dict):
            return False
        
        action = decision.get("action", "").lower()
        valid_actions = ["click", "type", "key", "scroll", "wait"]
        
        if action not in valid_actions:
            return False
        
        # Validate action-specific requirements
        if action == "click":
            coords = decision.get("coordinates")
            if not isinstance(coords, list) or len(coords) != 2:
                return False
            if not all(isinstance(c, (int, float)) for c in coords):
                return False
        
        elif action == "type":
            if "text" not in decision or not isinstance(decision["text"], str):
                return False
        
        elif action == "key":
            if "key" not in decision or not isinstance(decision["key"], str):
                return False
        
        elif action == "scroll":
            if "direction" not in decision:
                return False
            if decision["direction"] not in ["up", "down", "left", "right"]:
                return False
        
        elif action == "wait":
            duration = decision.get("duration", 1)
            if not isinstance(duration, (int, float)) or duration <= 0:
                return False
        
        return True
    
    def cleanup(self):
        """Cleanup LLM interface resources."""
        self.logger.info("Cleaning up LLM interface")
        # No specific cleanup needed for HTTP-based interface
