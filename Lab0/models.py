class Student:
    """
    SRP: Stores only student identity/contact data.
    """
    def __init__(self, name: str, email: str, phone: str):
        self.name = name
        self.email = email
        self.phone = phone

    def __str__(self):
        return f"{self.name} ({self.email}, {self.phone})"


class Post:
    """
    SRP: Holds only post content and its author.
    """
    def __init__(self, student: Student, content: str):
        self.student = student
        self.content = content

    def __str__(self):
        return f"{self.student.name}: {self.content}"
