import random
import requests
import wolframalpha

class FunFeatures:
    def __init__(self):
        self.wolfram_client = wolframalpha.Client(os.getenv('WOLFRAM_APP_ID'))
        self.jokes_api = "https://official-joke-api.appspot.com/random_joke"

    def tell_joke(self):
        try:
            response = requests.get(self.jokes_api)
            joke = response.json()
            return f"{joke['setup']}\n... {joke['punchline']}"
        except:
            return random.choice([
                "Why did the scarecrow win an award? Because he was outstanding in his field!",
                "What do you call a bear with no teeth? A gummy bear!",
                "Why don't eggs tell jokes? They'd crack up!"
            ])

    def solve_math(self, query):
        try:
            res = self.wolfram_client.query(query)
            answer = next(res.results).text
            return f"The answer is: {answer}"
        except:
            return "Sorry, I couldn't solve that math problem."

    def flip_coin(self):
        return random.choice(["Heads!", "Tails!"])

    def roll_dice(self, sides=6):
        return f"Rolling a {sides}-sided die: {random.randint(1, sides)}"
