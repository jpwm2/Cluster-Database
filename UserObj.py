import socket
import copy
from Obj import Obj


class UserObj(Obj):
    def __init__(self, id, owners = {}, passkey = '', title = '', data = ''):
        id, title, data, passkey = str(id, title, data, passkey)
        rootTitleId, rootDataId, way0Id = 18, 20, 14
        way0Obj = Obj().releaseObj(way0Id)
        self.releaseObj(id, owners, path = frozenset({way0Obj}))
        titleId = id + 1
        titleObj = Obj()
        while not titleObj.releaseObj(titleId, self.owner, data = title, path = frozenset({self, Obj().releaseObj(rootTitleId)})):
            titleId = titleId + 1
        titleObj.addPath(owners, frozenset({way0Obj}))
        dataId = titleId + 1
        dataObj = Obj()
        while not dataObj.releaseObj(dataId, self.owner, path = frozenset({self, Obj().releaseObj(rootDataId)})):
            dataId = titleId + 1
        dataObj.addPath(owners, frozenset({way0Obj}))


    def connectionServer(self, add: bool, followedObj: Obj, followPath: frozenset):
        server_address = ('localhost', 6789)
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        client.sendto(str([add, followedObj, set(followPath)]).encode('utf-8'), server_address)

    def addPath(self, owners, addPath):
        addPath.add(self)
        addPath = list(addPath)
        initPath = copy(addPath)
        for i in range(len(initPath)):
            obj = addPath.pop(i)
            if self.makeSureItisYou(obj, owners):
                obj.super().addPath(owners, frozenset(copy(addPath)))
            else:
                self.connectionServer(True, obj, frozenset(copy(addPath)))
            addPath = copy(initPath)

    def deletePath(self, owners, deletePath):
        deletePath.add(self)
        deletePath = list(deletePath)
        initPath = copy(deletePath)
        for i in range(len(initPath)):
            obj = deletePath.pop(i)
            if self.makeSureItisYou(obj, owners):
                obj.super().addPath(owners, set(copy(deletePath)))
            else:
                self.connectionServer(False, obj, frozenset(copy(deletePath)))
            deletePath = copy(deletePath)