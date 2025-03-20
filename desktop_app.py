import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QSystemTrayIcon, QMenu, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QThread
from pynput import keyboard
from utils.logger import ChatLogger
from utils.settings import Settings
from app import Natasha

class VoiceThread(QThread):
    def __init__(self, assistant):
        super().__init__()
        self.assistant = assistant
        self.running = True

    def run(self):
        while self.running:
            self.assistant.process_voice_command()

    def stop(self):
        self.running = False

class NatashaGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.assistant = Natasha()
        self.settings = Settings()
        self.logger = ChatLogger()
        self.setup_ui()
        self.setup_tray()
        self.setup_status_indicator()
        self.setup_hotkey()
        self.voice_thread = VoiceThread(self.assistant)
        self.voice_thread.start()

    def setup_ui(self):
        self.setWindowTitle('Natasha Assistant')
        self.setGeometry(100, 100, 400, 200)
        
        self.listen_button = QPushButton('Toggle Listening', self)
        self.listen_button.setGeometry(150, 80, 100, 40)
        self.listen_button.clicked.connect(self.toggle_listening)

    def setup_tray(self):
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('icon.png'))
        
        tray_menu = QMenu()
        show_action = tray_menu.addAction('Show')
        quit_action = tray_menu.addAction('Quit')
        
        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.quit_app)
        
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def setup_status_indicator(self):
        self.status_label = QLabel(self)
        self.status_label.setGeometry(10, 10, 20, 20)
        self.update_status_indicator(True)

    def update_status_indicator(self, is_listening):
        color = "green" if is_listening else "red"
        self.status_label.setStyleSheet(
            f"background-color: {color}; border-radius: 10px;"
        )

    def setup_hotkey(self):
        def on_hotkey():
            self.toggle_listening()

        hotkey = self.settings.get("hotkey")
        self.listener = keyboard.GlobalHotKeys({
            hotkey: on_hotkey
        })
        self.listener.start()

    def toggle_listening(self):
        if self.voice_thread.running:
            self.voice_thread.stop()
            self.listen_button.setText('Start Listening')
            self.update_status_indicator(False)
        else:
            self.voice_thread = VoiceThread(self.assistant)
            self.voice_thread.start()
            self.listen_button.setText('Stop Listening')
            self.update_status_indicator(True)

    def quit_app(self):
        self.voice_thread.stop()
        self.voice_thread.wait()
        self.listener.stop()
        QApplication.quit()

    def closeEvent(self, event):
        self.listener.stop()
        event.ignore()
        self.hide()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NatashaGUI()
    window.show()
    sys.exit(app.exec_())
