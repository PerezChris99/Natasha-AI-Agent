import os
import subprocess
import platform

class ApplicationManager:
    def __init__(self):
        self.system = platform.system()
        self.common_paths = self._get_common_paths()

    def _get_common_paths(self):
        if self.system == "Windows":
            return [
                os.path.join(os.environ["ProgramFiles"], ""),
                os.path.join(os.environ["ProgramFiles(x86)"], ""),
                os.path.join(os.environ["APPDATA"], ""),
            ]
        # Add paths for other operating systems as needed
        return []

    def open_application(self, app_name):
        try:
            if self.system == "Windows":
                os.system(f"start {app_name}")
            elif self.system == "Darwin":  # macOS
                os.system(f"open -a '{app_name}'")
            else:  # Linux
                subprocess.Popen(app_name)
            return f"Opening {app_name}"
        except Exception as e:
            return f"Error opening application: {str(e)}"
