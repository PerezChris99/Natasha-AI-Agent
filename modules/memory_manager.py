import os
import json
import datetime

class MemoryManager:
    """Manages the assistant's memory including facts and conversation history"""
    
    def __init__(self):
        self.memory_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
        self.facts_file = os.path.join(self.memory_dir, "facts.json")
        self.interactions_file = os.path.join(self.memory_dir, "interactions.json")
        
        # Ensure the data directory exists
        if not os.path.exists(self.memory_dir):
            os.makedirs(self.memory_dir)
            
        # Initialize memory storage
        self.facts = self._load_json(self.facts_file, [])
        self.interactions = self._load_json(self.interactions_file, [])

    def _load_json(self, file_path, default_value):
        """Load data from a JSON file, or return default if file doesn't exist"""
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"Error loading {file_path}, using default value")
                return default_value
        return default_value

    def _save_json(self, file_path, data):
        """Save data to a JSON file"""
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving to {file_path}: {e}")
            return False

    def add_fact(self, fact):
        """Add a new fact to memory"""
        timestamp = datetime.datetime.now().isoformat()
        self.facts.append({
            "fact": fact,
            "timestamp": timestamp
        })
        return self._save_json(self.facts_file, self.facts)

    def add_interaction(self, interaction_type, content):
        """Add a new interaction to memory"""
        timestamp = datetime.datetime.now().isoformat()
        self.interactions.append({
            "type": interaction_type,
            "content": content,
            "timestamp": timestamp
        })
        
        # Keep only the most recent 100 interactions
        if len(self.interactions) > 100:
            self.interactions = self.interactions[-100:]
            
        return self._save_json(self.interactions_file, self.interactions)

    def get_facts(self):
        """Get all stored facts"""
        return self.facts

    def get_recent_interactions(self, count=5):
        """Get recent interactions"""
        return self.interactions[-count:] if self.interactions else []

    def search_facts(self, query):
        """Search for facts containing the query"""
        query = query.lower()
        return [fact for fact in self.facts if query in fact["fact"].lower()]

    def clear_facts(self):
        """Clear all stored facts"""
        self.facts = []
        return self._save_json(self.facts_file, self.facts)

    def clear_interactions(self):
        """Clear all stored interactions"""
        self.interactions = []
        return self._save_json(self.interactions_file, self.interactions)
