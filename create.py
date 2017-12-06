from header import *

class head:
    def __init__(self):
        self.data = None
        self.head = True
        self.next = None
        self.prev = None
    def add_node(self,obj):
        if obj != None:
            self.next = obj
            obj.prev = self
            self.number = count()
            return self
        else:
            print "Can't add None type object."
    def is_head(self):
        return self.head
    def get_next(self):
        return self.next

class question:
    def __init__(self):
        self.data = None
        self.head = False
        self.next = None
        self.prev = None
    def add_node(self, obj):
        if obj != None:
            self.next = obj
            obj.prev = self
            self.number = count()
            print self.number
            return self.next
        else:
            print "Question object only takes 1 argument."
    def get_next(self):
        return self.next
    def title(self,title):
        self.title = title
    def number(self):
        print self.number
    def is_head(self):
        return self.head
    def has_next(self):
        if self.next == None:
            return False
        else:
            return True
i=0
def count():
    global i
    i+=1
    return i
head = head()
head.add_node(question())
q = head.get_next()
q.title("Hello?")
q.add_node(question()).number()
print i
