from Obj import Obj


class A:
    def __init__(self):
        self.hi = 'HI'
    
    def rint(self):
        print('why')
        print(self.hi)
        return 'fuck'

a = A()
ops = {}
ops[a] = 'hello'

print(ops[a])
print(a.rint())