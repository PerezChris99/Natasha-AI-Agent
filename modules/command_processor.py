import webbrowser
import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

class CommandProcessor:
    """Processes user input and identifies commands and arguments"""
    
    def __init__(self):
        # Define command patterns and their corresponding command identifiers
        self.commands = {
            r'(?i)tell\s+(?:me\s+)?a\s+joke': ('joke', None),
            r'(?i)set\s+(?:a\s+)?timer\s+for\s+(\d+)': ('timer', lambda m: int(m.group(1))),
            r'(?i)what\s+time\s+is\s+it': ('get_time', None),
            r'(?i)search\s+(?:for\s+)?(.+)': ('web_search', lambda m: m.group(1)),
            r'(?i)remember\s+that\s+(.+)': ('learn_fact', lambda m: m.group(1)),
            r'(?i)roll\s+(?:a\s+)?dice': ('dice', 6),  # Default 6-sided dice
            r'(?i)roll\s+(?:a\s+)?(\d+)(?:\s+sided)?(?:\s+dice)?': ('dice', lambda m: int(m.group(1))),
            r'(?i)remind\s+me\s+to\s+(.+)\s+in\s+(\d+)': ('set_reminder', lambda m: (m.group(1), float(m.group(2)))),
            r'(?i)who\s+are\s+you': ('introduce', None),
            r'(?i)help': ('help', None),
        }

    def process(self, text):
        """
        Process the user input text and extract commands
        
        Returns:
        - String response for direct answers
        - Tuple (command, args) for actions to be executed
        """
        if not text:
            return "I didn't hear anything."
        
        # Check for exit command
        if re.search(r'(?i)exit|quit|goodbye|bye', text):
            return "Goodbye! Have a nice day."
        
        # Check for commands
        for pattern, (command, arg_extractor) in self.commands.items():
            match = re.search(pattern, text)
            if match:
                # Extract arguments if needed
                args = None
                if arg_extractor:
                    if callable(arg_extractor):
                        args = arg_extractor(match)
                    else:
                        args = arg_extractor
                
                return (command, args)
        
        # If no command is recognized, return a fallback message
        return "I'm not sure how to help with that. Try asking for help."
