import passage

class Yamp:
    def __init__(self):
        self.passages = []

    def add_passage(self, text):
        p = passage.Passage()
        p.parse(text)
        self.passages.append(p)