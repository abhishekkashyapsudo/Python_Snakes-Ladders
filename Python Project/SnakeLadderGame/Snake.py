class Snake:

    # init method or constructor
    def __init__(self, head, tail):
        self.head = head
        self.tail = tail

    def __str__(self):
        return 'Head: ' + str(self.head) + " Tail: " + str(self.tail)
