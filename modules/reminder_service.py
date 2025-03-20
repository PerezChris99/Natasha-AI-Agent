from datetime import datetime, timedelta
import threading
import time

class ReminderService:
    def __init__(self, voice_engine):
        self.reminders = []
        self.voice_engine = voice_engine
        self.reminder_thread = threading.Thread(target=self._check_reminders, daemon=True)
        self.reminder_thread.start()

    def set_timer(self, minutes):
        reminder_time = datetime.now() + timedelta(minutes=minutes)
        self.reminders.append({
            'time': reminder_time,
            'message': f"Timer for {minutes} minutes is up!"
        })
        return f"Timer set for {minutes} minutes"

    def set_reminder(self, message, hours):
        reminder_time = datetime.now() + timedelta(hours=hours)
        self.reminders.append({
            'time': reminder_time,
            'message': message
        })
        return f"Reminder set for {hours} hours from now"

    def _check_reminders(self):
        while True:
            current_time = datetime.now()
            for reminder in self.reminders[:]:
                if current_time >= reminder['time']:
                    self.voice_engine.speak(reminder['message'])
                    self.reminders.remove(reminder)
            time.sleep(30)
