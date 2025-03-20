import tkinter as tk
from tkinter import scrolledtext
import threading

class AssistantUI:
    """GUI interface for the assistant"""
    
    def __init__(self, assistant):
        self.assistant = assistant
        self.root = None
        self.user_input_box = None
        self.response_display = None
        self.status_label = None

    def start(self):
        """Initialize and display the UI"""
        # Create UI in a separate thread to not block main operations
        threading.Thread(target=self._setup_ui, daemon=True).start()
    
    def _setup_ui(self):
        """Set up the UI components"""
        self.root = tk.Tk()
        self.root.title(f"{self.assistant.name} Assistant")
        self.root.geometry("800x600")
        
        # Assistant response display area
        response_frame = tk.Frame(self.root)
        response_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(response_frame, text="Assistant Responses:").pack(anchor=tk.W)
        
        self.response_display = scrolledtext.ScrolledText(response_frame, wrap=tk.WORD, height=15)
        self.response_display.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.response_display.config(state=tk.DISABLED)
        
        # Status indicator
        self.status_label = tk.Label(self.root, text="Status: Ready", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
        
        # User input area
        input_frame = tk.Frame(self.root)
        input_frame.pack(padx=10, pady=5, fill=tk.X, side=tk.BOTTOM)
        
        tk.Label(input_frame, text="Type your message:").pack(anchor=tk.W)
        
        input_box_frame = tk.Frame(input_frame)
        input_box_frame.pack(fill=tk.X, expand=True)
        
        self.user_input_box = tk.Entry(input_box_frame)
        self.user_input_box.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        self.user_input_box.bind("<Return>", self._on_submit)
        
        submit_button = tk.Button(input_box_frame, text="Send", command=self._on_submit)
        submit_button.pack(side=tk.RIGHT, padx=5)
        
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)
        self.root.mainloop()
    
    def _on_submit(self, event=None):
        """Handle user input submission"""
        text = self.user_input_box.get()
        if text.strip():
            self.update_user_input(text)
            self.user_input_box.delete(0, tk.END)
            # Pass the text to the assistant for processing
            self.assistant.text_input(text)
    
    def update_user_input(self, text):
        """Display user input in the response area"""
        self._update_response_display(f"You: {text}")
    
    def update_assistant_response(self, text):
        """Display assistant response in the response area"""
        self._update_response_display(f"{self.assistant.name}: {text}")
    
    def _update_response_display(self, text):
        """Update the response display with new text"""
        def update():
            self.response_display.config(state=tk.NORMAL)
            self.response_display.insert(tk.END, f"{text}\n\n")
            self.response_display.see(tk.END)  # Scroll to the bottom
            self.response_display.config(state=tk.DISABLED)
        
        if self.root:
            self.root.after(0, update)
    
    def update_status(self, status_text):
        """Update the status bar text"""
        if self.status_label:
            self.status_label.config(text=f"Status: {status_text}")
    
    def _on_close(self):
        """Handle window close event"""
        self.stop()
        self.assistant.stop()
    
    def stop(self):
        """Close the UI"""
        if self.root:
            self.root.quit()
            self.root.destroy()
