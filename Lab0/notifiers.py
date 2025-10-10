from abc import ABC, abstractmethod
from models import Student

class Notifier(ABC):
    """
    DIP: Abstraction for notifications used by high-level modules.
    OCP: New channels extend this without changing clients.
    """
    @abstractmethod
    def send_notification(self, student: Student, message: str):
        pass

class EmailNotifier(Notifier):
    """
    SRP: Handles only email notifications.
    """
    def send_notification(self, student: Student, message: str):
        print(f"[EmailNotifier] Sending email to {student.email}: {message}")

class SMSNotifier(Notifier):
    """
    SRP: Handles only SMS notifications.
    """
    def send_notification(self, student: Student, message: str):
        print(f"[SMSNotifier] Sending SMS to {student.phone}: {message}")

class PushNotifier(Notifier):
    """
    SRP: Handles only push notifications.
    OCP: Adds a new channel without changing clients.
    """
    def send_notification(self, student: Student, message: str):
        print(f"[PushNotifier] Sending push to {student.name}: {message}")

class NullNotifier(Notifier):
    """
    SRP: No-op notifier for tests or silencing.
    DIP: Swappable implementation without changing clients.
    """
    def send_notification(self, student: Student, message: str):
        return

class CompositeNotifier(Notifier):
    """
    OCP: Extends behavior by composition of notifiers.
    DIP: Depends on Notifier abstractions, not concretes.
    """
    def __init__(self, notifiers: list[Notifier]):
        self._notifiers = notifiers

    def send_notification(self, student: Student, message: str):
        for n in self._notifiers:
            n.send_notification(student, message)
