import requests
import os

class SmartHomeController:
    def __init__(self):
        self.base_url = os.getenv('SMART_HOME_HUB_URL', 'http://localhost:8080')
        self.devices = self._discover_devices()

    def _discover_devices(self):
        try:
            response = requests.get(f"{self.base_url}/devices")
            return response.json()
        except:
            return {}

    def control_device(self, device_name, action):
        device = next((d for d in self.devices if device_name.lower() in d['name'].lower()), None)
        if not device:
            return f"Device '{device_name}' not found"
        
        try:
            response = requests.post(f"{self.base_url}/control", json={
                'device_id': device['id'],
                'action': action
            })
            if response.status_code == 200:
                return f"OK, {action} {device_name}"
            return "Failed to control device"
        except Exception as e:
            return f"Error: {str(e)}"
