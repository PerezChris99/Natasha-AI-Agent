import webbrowser

class CommandProcessor:
    def __init__(self):
        self.commands = {
            'search': self.web_search,
            'play': self.handle_play,
            'open': self.handle_open,
            'volume': self.handle_volume,
            'mute': lambda x: ('volume', 'mute'),
            'unmute': lambda x: ('volume', 'unmute'),
            'weather': self.handle_weather,
            'news': self.handle_news,
            'timer': self.handle_timer,
            'remind': self.handle_reminder,
            'turn': self.handle_smart_home,
            'schedule': self.handle_calendar,
            'joke': lambda x: ('joke', None),
            'calculate': self.handle_math,
            'flip': lambda x: ('coin', None),
            'roll': self.handle_dice,
            'identify': lambda x: ('identify', None),
            'add face': self.handle_face_add,
            'system': self.handle_system_command,
            'schedule': self.handle_schedule,
            'monitor': self.handle_monitor,
            'analyze': self.handle_analysis,
            'learn': self.handle_learning,
            'summarize': self.handle_summarize,
            'context': lambda x: ('context', None),
            'understand': self.handle_understanding
        }

    def process(self, command):
        for key in self.commands:
            if command.startswith(key):
                return self.commands[key](command)
        return "Command not recognized"

    def web_search(self, command):
        query = command.replace('search', '').strip()
        search_url = f"https://www.google.com/search?q={query}"
        webbrowser.open(search_url)
        return f"Searching for {query}"

    def handle_play(self, command):
        if 'spotify' in command:
            return 'spotify', command.replace('play', '').replace('on spotify', '').strip()
        elif 'youtube' in command:
            return 'youtube', command.replace('play', '').replace('on youtube', '').strip()
        return None

    def handle_open(self, command):
        app_name = command.replace('open', '').strip()
        return 'app', app_name

    def handle_volume(self, command):
        try:
            level = int(''.join(filter(str.isdigit, command)))
            return 'volume', level
        except ValueError:
            return None

    def handle_weather(self, command):
        city = command.replace('weather', '').replace('in', '').strip()
        return ('weather', city)

    def handle_news(self, command):
        category = 'general'
        if 'tech' in command: category = 'technology'
        elif 'sports' in command: category = 'sports'
        elif 'business' in command: category = 'business'
        return ('news', category)

    def handle_timer(self, command):
        try:
            minutes = int(''.join(filter(str.isdigit, command)))
            return ('timer', minutes)
        except ValueError:
            return None

    def handle_reminder(self, command):
        try:
            parts = command.replace('remind me to', '').split('in')
            message = parts[0].strip()
            hours = int(''.join(filter(str.isdigit, parts[1])))
            return ('reminder', (message, hours))
        except:
            return None

    def handle_smart_home(self, command):
        words = command.split()
        if len(words) >= 4:
            action = words[1]  # on/off
            device_name = ' '.join(words[2:])
            return ('smart_home', (device_name, action))
        return None

    def handle_calendar(self, command):
        days = 1
        if 'week' in command:
            days = 7
        elif 'month' in command:
            days = 30
        return ('calendar', days)

    def handle_math(self, command):
        query = command.replace('calculate', '').strip()
        return ('math', query)

    def handle_dice(self, command):
        try:
            sides = int(''.join(filter(str.isdigit, command))) if any(c.isdigit() for c in command) else 6
            return ('dice', sides)
        except:
            return ('dice', 6)

    def handle_face_add(self, command):
        name = command.replace('add face', '').strip()
        return ('add_face', name)

    def handle_system_command(self, command):
        if 'status' in command:
            return ('system_status', None)
        elif 'network' in command:
            return ('network_status', None)
        elif 'processes' in command:
            return ('processes', None)
        return None

    def handle_schedule(self, command):
        try:
            parts = command.split(' at ')
            task_parts = parts[0].replace('schedule', '').strip().split(' ')
            return ('schedule', {
                'name': f"task_{len(self.tasks)}",
                'command': ' '.join(task_parts[:-1]),
                'schedule_type': task_parts[-1],
                'time_value': parts[1].strip()
            })
        except:
            return None

    def handle_monitor(self, command):
        if 'cpu' in command:
            return ('monitor', 'cpu')
        elif 'memory' in command:
            return ('monitor', 'memory')
        elif 'gpu' in command:
            return ('monitor', 'gpu')
        return ('monitor', 'all')

    def handle_analysis(self, command):
        if 'data' in command:
            parts = command.split('data')
            if len(parts) > 1:
                return ('analyze_data', parts[1].strip())
        return ('analyze_text', command.replace('analyze', '').strip())

    def handle_learning(self, command):
        if 'pattern' in command:
            # Format: learn pattern "input" -> "response"
            parts = command.split('"')
            if len(parts) >= 4:
                return ('learn_pattern', (parts[1], parts[3]))
        elif 'fact' in command:
            fact = command.replace('learn fact', '').strip()
            return ('learn_fact', fact)
        return None

    def handle_summarize(self, command):
        text = command.replace('summarize', '').strip()
        return ('summarize', text)

    def handle_understanding(self, command):
        text = command.replace('understand', '').strip()
        return ('understand', text)
