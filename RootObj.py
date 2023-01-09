from ast import literal_eval
import socket
from Obj import Obj

class RootObj(Obj):
    passkey = 'rootpasskey1234'
    owner = {Obj().releaseObj(12): passkey}
    def __init__(self, id, title = '', data = ''):
        id, title, data = str(id, title, data)
        rootTitleId, rootDataId, way0Id = 18, 20, 14
        way0Obj = Obj().releaseObj(way0Id)
        self.releaseObj(id, self.owner, path = frozenset({way0Obj}))
        titleId = id + 1
        titleObj = Obj()
        while not titleObj.releaseObj(titleId, self.owner, data = title, path = frozenset({self, Obj().releaseObj(rootTitleId)})):
            titleId = titleId + 1
        titleObj.addPath(self.owner, frozenset({way0Obj}))
        rootTitleObj = Obj().releaseObj(rootTitleId)
        rootTitleObj.addPath(self.owner, {self, titleObj})
        dataId = titleId + 1
        dataObj = Obj()
        while not dataObj.releaseObj(dataId, self.owner, path = frozenset({self, Obj().releaseObj(rootDataId)})):
            dataId = titleId + 1
        dataObj.addPath(self.owner, frozenset({way0Obj}))
        rootDataObj = Obj().releaseObj(rootDataId)
        rootDataObj.addPath(self.owner, {self, titleObj})

    def activation():
        server_address = ('localhost', 6789)
        max_size = 4096

        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(server_address)
        while True:
            rawData, client = server.recvfrom(max_size)
            data = literal_eval(rawData)
            obj = Obj().releaseObj(data[1])
            path = set()
            for objId in data[2]:
                path.add(Obj().releaseObj(objId))
            if data[0]:
                obj.super().addPath(frozenset(path))
            else:
                obj.super().deletePath(frozenset(path))