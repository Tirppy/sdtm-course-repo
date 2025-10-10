from models import Student, Post
from notifiers import Notifier, EmailNotifier, SMSNotifier, PushNotifier, CompositeNotifier, NullNotifier

class Forum:
    """
    DIP: Depends on the Notifier abstraction, not concrete channels.
    SRP: Manages forum posts and delegates notification.
    OCP: New notifier types can be added without modifying this class.
    """
    def __init__(self, notifier: Notifier):
        self.notifier = notifier
        self.posts = []

    def add_post(self, student: Student, content: str):
        post = Post(student, content)
        self.posts.append(post)
        self.notifier.send_notification(student, f"New post created: {content}")
        print(f"[Forum] {student.name} posted: {content}")

    def list_posts(self):
        print("\n[Forum] Listing all posts:")
        for post in self.posts:
            print(f"{post.student.name}: {post.content}")

def main():
    alice = Student("Alice", "alice@example.com", "+123456789")
    bob = Student("Bob", "bob@example.com", "+987654321")
    # DIP/OCP: Swap or compose notifier implementations without changing Forum
    notifier = CompositeNotifier([EmailNotifier(), SMSNotifier(), PushNotifier()])
    forum = Forum(notifier)
    forum.add_post(alice, "Hello, this is my first post!")
    forum.add_post(bob, "Welcome Alice!")
    forum.list_posts()

if __name__ == "__main__":
    main()
