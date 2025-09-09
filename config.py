# config.py - Configuration settings
import os
from pathlib import Path

class Config:
    def __init__(self):
        # LLM Configuration - CAMBIA SOLO QUESTA RIGA PER SWITCHARE PROVIDER
        self.llm_config = {
            "provider": "claude",  # "claude" o "local" (GPT2 mock)
            "model": "claude-sonnet-4-20250514",
            "api_key": "ADD YOUR API KEY HERE",
            "max_tokens": 1000,
            "temperature": 0.7
        }
        
        # File paths
        self.excel_file = "middleware_memory.xlsx"
        self.log_file = "middleware_log.txt"
        self.debug_file = "debug_log.xlsx"
        
        # System parameters
        self.boredom_threshold = 0.3
        self.topic_change_threshold = 5
        self.engagement_decay_rate = 0.1
        
        # Create data directory if it doesn't exist
        Path("data").mkdir(exist_ok=True)
        self.excel_file = f"data/{self.excel_file}"
        self.debug_file = f"data/{self.debug_file}"
        
        # Debug settings
        self.debug_enabled = True
        self.console_debug = False  # False = solo file Excel, True = anche console