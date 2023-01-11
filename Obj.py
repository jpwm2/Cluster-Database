from __future__ import annotations
from ast import literal_eval
import os

'''

It is possible to explain anything with my difined object and these collections.
And now, The database is here.
森羅万象はこの新しく定義されたオブジェクトとそれの集合で表せられます。
それらによって作られる新しいデータベースです。

'''


class Obj():
    '''
    
    Obj is an Object.
    It is based on security protection (Who likes do bad?)
    And these are 6 elements to make an Object.
    セキュリティ保護をベースに作りました。（人の嫌がることはしてもされたくもないでしょうから。）
    そのうえでオブジェクトとして機能するために6つの要素を分けました。

    self.id (int): an id the one and only.
    self.owners (set): a set of owners who can operate core methods.
    self.passkey (str): a passkey it can be an owner if you know the it.
    self.data (str): a data the obj's
    self.childs (set): a set of child objs
    self.parents (set): a set of parent objs

    '''
    way0Id = 26

    def __init__(self, id: int):
        '''

        Fleshen self with an id.

        Args:
            id (int): an id self is fleshed with.

        '''

        def importObj():
            '''
            
            Import an obj with self.id from your explore.
            
            '''
            with open(str(self.way0Id) + '/' + str(self.id) + '.txt','r') as f:
                ids = f.read()
            ids = ids.split('\n')
            self.owners = literal_eval(ids[1])
            self.passkey = ids[2]
            self.data = ids[3]
            self.childs = literal_eval(ids[4])
            self.parents = literal_eval(ids[5])

        self.id = id
        if self.existObj():
            importObj()
        else:
            self.owners = set()
            self.passkey = None
            self.data = None
            self.childs = set()
            self.parents = set()


    def exportObj(self):
        '''
        
        Export an obj to your explore.
        
        '''
        id = self.id
        owners = self.owners
        passkey = self.passkey
        data = self.data
        rawChilds = self.childs
        rawParents = self.parents
        ids = f"{id}\n{owners}\n{passkey or ''}\n{data or ''}\n{rawChilds}\n{rawParents}"
        with open(str(self.way0Id) + '/' + str(self.id) + '.txt','w') as f:
            f.write(ids)


    def existObj(self):
        '''
        
        Check self is in explore.

        Returns:
            bool: True if self is in explore, else False.
        
        '''
        return True if os.path.exists(str(self.way0Id) + '/' + str(self.id) + '.txt') else False


    def getId(self):
        '''
        
        Get self.id

        return:
            int: self.id
        
        '''
        return self.id


    def getData(self, passkeys: set = {''}):
        '''
        
        Get self.data if you are owners.

        Args:
            passkeys (set): prove myself.

        Return:
            str: self.data if you are owners.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            return self.data


    def setData(self, passkeys: set = {''}, data: str = ''):
        '''
        
        Set a data to self.data if you are owners.

        Args:
            passkeys (set): prove myself.
            data (str): a data you set newly.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            self.data = data
            self.exportObj()


    def getPasskey(self, passkeys: set = {''}):
        '''
        
        Get self.passkey if you are owners.

        Args:
            passkeys (set): prove myself.

        Returns:
            str: self.passkey if you are owners.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            return self.passkey


    def setPasskey(self, passkeys: set = {''}, passkey: str = ''):
        '''
        
        Set a passkey to self.passkey if you are owners.

        Args:
            passkeys (set): prove myself.
            passkey (str): a passkey you set newly.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            self.passkey = passkey
            self.exportObj()


    def getOwners(self):
        '''
        
        Get an owner Obj.

        Returns:
            set: self.owners

        '''
        return self.owners


    def addOwner(self, passkeys: set, addId: int):
        '''
        
        Add an owner Obj to self.owners if you are owners.

        Args:
            passkeys (set): prove myself.
            addId (int): an Id you add.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            self.owners.add(addId)
            self.exportObj()


    def deleteOwner(self, passkeys: set, deleteId: int):
        '''
        
        Delete an owner Obj to self.owners if you are owners.

        Args:
            passkeys (set): prove myself.
            deleteId (int): an Id you delete.
        
        '''
        deleteObj = Obj(deleteId)
        if self.makeSureOwnerIsYou(deleteObj, passkeys):
            self.owners.remove(deleteId)
            self.exportObj()


    def getChilds(self):
        '''
        
        Get Child Objs.

        Returns:
            set: self.childs

        '''
        return self.childs


    def getParents(self):
        '''
        
        Get Parent Objs.

        Returns:
            set: self.parents

        '''
        return self.parents


    def addParent(self, passkeys: set, addId: int):
        '''

        Add an Obj to self.parents if you are owners.
        And add self to the Obj's.childs if you are owners.
        
        Args:
            passkeys (set): prove myself.
            addId (set): an id you add.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            self.parents.add(addId)
            addObj = Obj(addId)
            addObj.childs.add(self.getId())
            self.exportObj()
            addObj.exportObj()


    def deleteParent(self, passkeys: set, deleteId: int):
        '''

        Delete an Obj to self.parents if you are owners.
        And delete self to the Obj's.childs if you are owners.
        
        Args:
            passkeys (set): prove myself.
            deleteId (set): an id you delete.
        
        '''
        if self.makeSureOwnerIsYou(self, passkeys):
            self.parents.remove(deleteId)
            deleteObj = Obj(deleteId)
            deleteObj.childs.remove(self.getId())
            self.exportObj()
            deleteObj.exportObj()


    def makeSureOwnerIsYou(self, obj: Obj, passkeys : set):
        '''
        
        Make sure you are owner.
        
        Args:
            obj (Obj): an Obj judged you are owner.
            passkeys (set): prove Obj's self.
            
        Return:
            bool: Return True if passkeys is majority in self's owners.

        '''

        def helpFromSelfObj():
            '''
            
            Put in a vote by self with self's passkey.

            Return:
                int: Return a vote if the passkeys match, else none vote.

            '''
            return 1 if all({ownerNumber <= (1 if ownerCount == 0 else ownerCount * 2), (obj.passkey or '') in passkeys}) else 0

        owners = obj.getOwners()
        ownerNumber = 1
        ownerCount = 0
        for id in owners:
            ownerNumber += 1
            ownerCount += 1 if self.makeSureOwnerIsYou(Obj(id), passkeys) else 0
        ownerCount += helpFromSelfObj()
        return True if ownerNumber < 2 * ownerCount else False