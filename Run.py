import Obj
import os

if not os.path.exists('14'):
    os.mkdir('14')

o = Obj.Obj('0')
o.setData('3',{'0':''})
o.exportObj()