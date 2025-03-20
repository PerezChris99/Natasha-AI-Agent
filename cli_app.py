from modules.command_processor import CommandProcessor

def main():
    processor = CommandProcessor()
    print("Ready to process commands. Type 'exit' to quit.")
    
    while True:
        command = input("> ").lower().strip()
        
        if command == 'exit':
            print("Goodbye!")
            break
            
        result = processor.process(command)
        print("Result:", result)

if __name__ == "__main__":
    main()
