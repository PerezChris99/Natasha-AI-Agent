import schedule
import threading
import subprocess
import time
from datetime import datetime

class TaskAutomation:
    def __init__(self):
        self.tasks = {}
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()

    def add_scheduled_task(self, name, command, schedule_type, time_value):
        """
        schedule_type: daily, weekly, interval
        time_value: HH:MM for daily/weekly, minutes for interval
        """
        if schedule_type == 'daily':
            schedule.every().day.at(time_value).do(
                self._execute_task, name, command
            ).tag(name)
        elif schedule_type == 'interval':
            schedule.every(int(time_value)).minutes.do(
                self._execute_task, name, command
            ).tag(name)
        
        self.tasks[name] = {
            'command': command,
            'schedule_type': schedule_type,
            'time_value': time_value
        }
        return f"Task {name} scheduled successfully"

    def remove_task(self, name):
        if name in self.tasks:
            schedule.clear(name)
            del self.tasks[name]
            return f"Task {name} removed"
        return "Task not found"

    def _execute_task(self, name, command):
        try:
            if command.startswith('http'):
                webbrowser.open(command)
            else:
                subprocess.run(command, shell=True)
            return f"Task {name} executed successfully"
        except Exception as e:
            return f"Error executing task {name}: {str(e)}"

    def _run_scheduler(self):
        while self.running:
            schedule.run_pending()
            time.sleep(60)
