import threading
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.toast import toast
import speech_recognition as sr

KV = '''
BoxLayout:
    orientation: 'vertical'

    MDTextField:
        id: command_text
        hint_text: "Voice command result"
        multiline: True

    MDRaisedButton:
        text: "Listen"
        on_press: app.listen_for_command()
'''

class VoiceCommandApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def listen_for_command(self):
        threading.Thread(target=self._listen_for_command_thread).start()

    def _listen_for_command_thread(self):
        recognizer = sr.Recognizer()

        with sr.Microphone() as source:
            print("Say something:")
            self.root.ids.command_text.text = "Listening..."
            toast("Listening...")

            try:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
                command = recognizer.recognize_google(audio, language="en-US").lower()
                print("You said:", command)
                self.root.ids.command_text.text = command
                self.execute_command(command)
            except sr.UnknownValueError:
                print("Could not understand audio")
                toast("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
                toast(f"Could not request results; {e}")

    def execute_command(self, command):
        # Implement your logic to execute commands here
        # For example, you can perform actions based on recognized commands
        toast(f"Executing command: {command}")

if __name__ == "__main__":
    VoiceCommandApp().run()
