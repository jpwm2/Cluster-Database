from __future__  import annotations
from ast import literal_eval
import copy
import os


class Obj():
    def importObj(self):
        with open('14/' + str(self.id) + '.txt','r') as f:
            rawData = f.read()
        rawData = rawData.split('\n')
        self.owners = set()
        for objId in literal_eval(rawData[1]):
            self.owners.add(Obj().releaseObj(objId))
        self.passkey = rawData[2]
        self.data = rawData[3]
        self.brothers = set()
        for objId in literal_eval(rawData[4]):
            self.brothers.add(Obj().releaseObj(objId))
        self.childsPathes = {}
        for path, childs in enumerate(eval(rawData[5])):
            objPath = set()
            for objId in path:
                objPath.add(Obj().releaseObj(objId))
            objChilds = set()
            for objId in childs:
                objChilds.add(Obj().releaseObj(objId))
            self.childsPathes[frozenset(objPath)] = objChilds
        self.pathes = set()
        for path in literal_eval(rawData[5]):
            objPath = set()
            for objId in path:
                objPath.add(Obj().releaseObj(objId))
            self.pathes.add(frozenset(objPath))

    def exportObj(self, owners):
        id = self.getId()
        owners = set()
        for obj in self.getOwners():
            owners.add(obj.getId())
        passkey = self.passkey(owners)
        data = self.getData(owners)
        brothers = set()
        for obj in self.getBrothers():
            brothers.add(obj.getId())
        childsPathes = {}
        for objPath, objChilds in enumerate(self.getChildsPathes()):
            path = set()
            for obj in objPath:
                path.add(obj.getId())
            childs = set()
            for obj in objChilds:
                childs.add(obj.getId())
            childsPathes[frozenset(path)] = childs
        pathes = set()
        for objPath in self.getPathes():
            path = set()
            for obj in objPath:
                path.add(obj.getId())
            pathes.add(frozenset(path))
        strObj = id + '\n' + owners + '\n' + passkey + '\n' + data + '\n' + brothers + '\n' + childsPathes + '\n' + pathes
        with open('14/' + str(id) + '.txt','w') as f:
            f.write(strObj)

    def releaseObj(self, id: int, owner: dict = {}, passkey: str = '', data: str = '', path: frozenset = frozenset()):

        def existObj(id):
            path = '14/' + str(id) + '.txt'
            if os.path.exists(path):
                return True
            else:
                return False

        self.id = id
        status = False
        if existObj(id):
            self.importObj()
            status = True
        else:
            self.addOwner(owner, owner)
            self.setData(data, owner)
            self.setPasskey(passkey, owner)
            self.addPath(path, owner)
            self.exportObj()
        return status

    def getId(self):
        return self.id

    def getData(self, owners: dict):
        if self.makeSureItisYou(self.getId(), owners):
            return self.data

    def setData(self, owners: dict, data: str):
        if self.makeSureItisYou(self.getId(), owners):
            self.data = data
            self.exportObj()

    def getPasskey(self, owners: dict):
        if self.makeSureItisYou(self.getId(), owners):
            return self.passkey

    def setPasskey(self, owners: dict, passkey: str):
        if self.makeSureItisYou(self.getId(), owners):
            self.passkey = passkey
            self.exportObj()

    def getOwners(self):
        return self.owners

    def addOwner(self, owners: dict, addObj: Obj):
        if self.makeSureItisYou(self.getId(), owners):
            self.owners.add(addObj.getId())
            self.exportObj()

    def deleteOwner(self, owners: dict, deleteObj: Obj):
        if self.makeSureItisYou(deleteObj.getId(), owners):
            self.owners.remove(deleteObj.getId())
            self.exportObj()

    def getBrothers(self):
        return self.brothers

    def getChildsPathes(self):
        return self.childsPathes

    def getPathes(self):
        return self.path

    def addPath(self, owners: dict, addPath: frozenset):
        if self.makeSureItisYou(self, owners):
            self.path.add(addPath)
            for obj in addPath:
                obj.brohers |= addPath
                obj.childsPathes[addPath].add(self.getId())
                obj.exportObj()

    def deletePath(self, owners: dict, deletePath: frozenset):
        selfId = self.getId()
        if self.makeSureItisYou(selfId, owners):
            self.path.remove(deletePath)
            for obj in deletePath:
                childsPath = obj.childsPathes.getchildsPathes()
                childs = childsPath[deletePath]
                childs.remove(selfId)
                if childs == set():
                    del childs
                cluster = {}
                for obj2 in childsPath.keys():
                    cluster |= obj2
                obj.brother = cluster
                obj.exportObj()

    def makeSureItisYou(self, obj: Obj, owners : dict):
        
        def operatePasskeyOwner(obj, owners):

            return True if obj.passkey == owners.get(obj) else False

        def allowPasskeyOwner(ownerNumber, ownerCount):
            if ownerNumber == 0:
                return True
            else:
                if ownerCount == 0:
                    ownerCount = 0.1
                return True if ownerNumber / ownerCount < 2 else False
        owners0 = obj.getOwners()
        ownerNumber = 0
        ownerCount = 0
        for o in owners0:
            ownerNumber += 1
            ownerCount += 1 if self.makeSureItisYou(o, owners) else 0
        if allowPasskeyOwner(ownerNumber, ownerCount):
            if operatePasskeyOwner(obj, owners):
                ownerCount += 1
        ownerNumber += 1
        if ownerCount == 0:
            ownerCount = 0.1
        return True if ownerNumber / ownerCount <= 2 else False