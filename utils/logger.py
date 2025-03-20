import json
from datetime import datetime
from pathlib import Path

class ChatLogger:
    def __init__(self, log_dir="logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.current_log = self.log_dir / f"chat_{datetime.now().strftime('%Y%m%d')}.json"
        
    def log_interaction(self, user_input, assistant_response):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "user_input": user_input,
            "assistant_response": assistant_response
        }
        
        existing = []
        if self.current_log.exists():
            with open(self.current_log, 'r') as f:
                existing = json.load(f)
                
        existing.append(entry)
        
        with open(self.current_log, 'w') as f:
            json.dump(existing, f, indent=2)
