import os
import json
from cryptography.fernet import Fernet
import base64
import hashlib

class ApiKeyManager:
    """Manager for API keys used by various services"""
    
    def __init__(self, keys_file=None, master_password=None):
        """Initialize API Key Manager"""
        self.base_dir = os.path.dirname(os.path.dirname(__file__))
        self.keys_file = keys_file or os.path.join(self.base_dir, 'config', 'api_keys.json')
        self.key_file = os.path.join(self.base_dir, 'config', '.keyfile')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(self.keys_file), exist_ok=True)
        
        self.master_password = master_password
        self.keys = None
        self.encryption_key = None
        
        # Initialize encryption
        self._setup_encryption()
        
        # Load API keys
        self.keys = self._load_keys()
        
    def _setup_encryption(self):
        """Set up encryption for API keys"""
        try:
            if os.path.exists(self.key_file):
                with open(self.key_file, 'rb') as file:
                    self.encryption_key = file.read()
            else:
                # Generate a new encryption key
                self.encryption_key = Fernet.generate_key()
                with open(self.key_file, 'wb') as file:
                    file.write(self.encryption_key)
        except Exception as e:
            print(f"Error setting up encryption: {e}")
            # Fallback to a basic key if encryption fails
            self.encryption_key = b'fallback_key_please_replace_in_production_environment=='
    
    def _encrypt(self, data):
        """Encrypt data"""
        if not data:
            return ""
            
        try:
            f = Fernet(self.encryption_key)
            return f.encrypt(data.encode()).decode()
        except Exception as e:
            print(f"Encryption error: {e}")
            # Basic fallback encryption - not secure, just to avoid plaintext
            key = hashlib.sha256(self.encryption_key).digest()
            encoded = base64.b64encode(data.encode()).decode()
            return encoded
    
    def _decrypt(self, encrypted_data):
        """Decrypt data"""
        if not encrypted_data:
            return ""
            
        try:
            f = Fernet(self.encryption_key)
            return f.decrypt(encrypted_data.encode()).decode()
        except Exception as e:
            print(f"Decryption error: {e}")
            # Basic fallback decryption
            try:
                return base64.b64decode(encrypted_data.encode()).decode()
            except:
                return ""
    
    def _load_keys(self):
        """Load API keys from file"""
        if os.path.exists(self.keys_file):
            try:
                with open(self.keys_file, 'r') as file:
                    encrypted_keys = json.load(file)
                
                # Decrypt keys
                decrypted_keys = {}
                for service, encrypted_key in encrypted_keys.items():
                    decrypted_keys[service] = self._decrypt(encrypted_key)
                
                return decrypted_keys
            except Exception as e:
                print(f"Error loading API keys: {e}")
        
        # If file doesn't exist or there's an error, create a new one with empty keys
        self.keys = {}
        self._save_keys()
        return {}
    
    def _save_keys(self):
        """Save API keys to file"""
        try:
            # Encrypt keys
            encrypted_keys = {}
            for service, key in self.keys.items():
                encrypted_keys[service] = self._encrypt(key)
            
            with open(self.keys_file, 'w') as file:
                json.dump(encrypted_keys, file, indent=4)
        except Exception as e:
            print(f"Error saving API keys: {e}")
    
    def get_api_key(self, service):
        """Get API key for a service"""
        return self.keys.get(service, "")
    
    def set_api_key(self, service, key):
        """Set API key for a service"""
        self.keys[service] = key
        self._save_keys()
    
    def remove_api_key(self, service):
        """Remove API key for a service"""
        if service in self.keys:
            del self.keys[service]
            self._save_keys()
    
    def list_services(self):
        """List all services with API keys"""
        return list(self.keys.keys())
