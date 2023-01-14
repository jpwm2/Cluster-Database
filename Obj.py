from __future__ import annotations
from ast import literal_eval
import hashlib
import os
from scryp import encrypt, decrypt

'''

It is possible to explain anything with my difined object and these Cluster.
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
            self.passkey = self.hashKey()
            self.data = encrypt('None','')
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
        childs = self.childs
        parents = self.parents
        ids = f"{id}\n{owners}\n{passkey}\n{data}\n{childs}\n{parents}"
        #print(f"id: {id}, owners: {owners}, passkey: {passkey}, data: {data}, childs: {childs}, parents: {parents}")
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


    def getData(self, passkeys: set = {''}, selfPasskey: str = ''):
        '''
        
        Get self.data if you are owners.

        Args:
            passkeys (set): prove myself.
            selfPasskey (str): a key encrypt data with.

        Return:
            str: self.data if you are owners.
        
        '''
        if self.makeSureAPieceIsYou(self, passkeys):
            return decrypt(self.data, selfPasskey)


    def setData(self, passkeys: set = {''}, selfPasskey: str = '', data: str = ''):
        '''
        
        Set a data to self.data if you are owners.

        Args:
            passkeys (set): prove myself.
            data (str): a data you set newly.
            selfPasskey (str): a key data encrypt by.
        
        '''
        if self.makeSureOwnerIsYou(passkeys):
            self.data = encrypt(data, selfPasskey)
            self.exportObj()


    def setPasskey(self, passkeys: set = {''}, oldPasskey: str = '', newPasskey: str = ''):
        '''
        
        Set a passkey to self.passkey if you are owners.

        Args:
            passkeys (set): prove myself.
            oldPasskey (str): a passkey you remove.
            newPasskey (str): a passkey you set.
        
        '''

        if self.makeSureOwnerIsYou(passkeys):
            self.data = encrypt(decrypt(self.data, oldPasskey), newPasskey)
            self.passkey = self.hashKey(newPasskey)
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
        if self.makeSureOwnerIsYou(passkeys):
            self.owners.add(addId)
            self.exportObj()


    def deleteOwner(self, passkeys: set, deleteId: int):
        '''
        
        Delete an owner Obj to self.owners if you are owners.

        Args:
            passkeys (set): prove myself.
            deleteId (int): an Id you delete.
        
        '''
        if Obj(deleteId).makeSureOwnerIsYou(passkeys):
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
        if self.makeSureOwnerIsYou(passkeys):
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
        if self.makeSureOwnerIsYou(passkeys):
            self.parents.remove(deleteId)
            deleteObj = Obj(deleteId)
            deleteObj.childs.remove(self.getId())
            self.exportObj()
            deleteObj.exportObj()

    def makeSureAPieceIsYou(self, passkeys: set):
        '''
        
        Make sure a piece of owner is you.
        
        Args:
            obj (Obj): an Obj judged you are a piece of owner.
            passkeys (set): prove Obj's self.
            
        Returns:
            bool: Return True if passeys is in self's owners.
        
        '''
        if self.passkey in self.hashKey(passkeys):
            return True
        owners = self.getOwners()
        for id in owners:
            if Obj(id).makeSureAPieceIsYou(passkeys):
                return True
        
            
    def makeSureOwnerIsYou(self, passkeys : set):
        '''
        
        Make sure you are owner.
        
        Args:
            obj (Obj): an Obj judged you are owner.
            passkeys (set): prove Obj's self.
            
        Returns:
            bool: Return True if passkeys is majority in self's owners.

        '''
        ownerNumber = len(self.owners)
        if ownerNumber == 0:
                return 1 if self.passkey in self.hashKey(passkeys) else 0
        else:
            ownerCount = 0
            for id in self.owners:
                ownerCount += Obj(id).makeSureOwnerIsYou(passkeys)
            return 1 if ownerNumber < ownerCount * 2 else 0

    def hashKey(self, passkeys: any = ''):
        '''
        
        Create a hash code.
        
        Args:
            passkeys (any): an any of passkeys will be hashed.

        Returns:
            set: a set of hashed code 
            
        '''
        keyType = str(type(passkeys))
        hashedPasskeys = None
        match keyType:
            case "<class 'str'>":
                hashedPasskeys = hashlib.sha256(passkeys.encode("utf-8")).hexdigest()
            case "<class 'set'>":
                hashedPasskeys = set()
                for passkey in passkeys:
                    hashedPasskeys.add(hashlib.sha256(passkey.encode("utf-8")).hexdigest())
        return hashedPasskeys
