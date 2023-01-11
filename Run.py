from Obj import Obj
import os


'''

There is a field run Obj class.

'''


def checkField():
    '''
    
    Check the field it hold Objs.
    If nothing, make it.
    
    '''
    if not os.path.exists('26'):
        os.mkdir('26')


checkField()

#Please write up Obj class methods right here.