class Title:
    """
    Simple class that creates a CLI title:
    a dashed line, the title, a dashed line.
    """

    def __init__(self, title):
        self.title = title

    def display(self):
        print('-' * len(self.title))
        print(self.title)
        print('-' * len(self.title))
