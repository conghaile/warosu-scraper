class Post():
    def __init__(self, number, subject, text, time):
        self.number = number
        self.subject = subject
        self.text = text
        self.time = time
        
    def postDict(self):
        post = {"number": self.number, "subject": self.subject, "text": self.subject, "time": self.time}
        return post