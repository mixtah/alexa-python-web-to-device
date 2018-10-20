'''
Created on 7 Feb 2017

@author: Michael
'''
from MySQLAdapter import MySQLAdapter
db = MySQLAdapter()

import time
from datetime import datetime,timedelta
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'

def fix_bool(b, toMySQL=True):
    if toMySQL:
        if isinstance(b, str) and b.upper()=="TRUE":
            b = "1"
        elif isinstance(b, str) and b.upper()=="FALSE":
            b = "0"
        elif b==True:
            b = "1"
        elif b==False:
            b = "0"
    else:
        if isinstance(b, str) and b.upper()=="TRUE":
            b = True
        elif isinstance(b, str) and b.upper()=="FALSE":
            b = False
        elif b=="1":
            b = True
        elif b=="0":
            b = False
    return b

class World_State(object):
    '''
    classdocs
    '''

    def __init__(self, **params):
        '''
        Constructor
        '''
        
        self.id = params.get('id',None)
        self.planetname = params.get('planetname',None)
        self.pressure = params.get('pressure',None)
        self.temperature = params.get('temperature',None)
        self.lookingat = params.get('lookingat',None)
        self.isdaytime = params.get('isdaytime',True)
        self.islighton = params.get('islighton',True)
        self.isdrillon = params.get('isdrillon',True)
        self.settings = params.get('settings','{}')
        self.timestamp = params.get('timestamp',None)
        
        self.fix_bools(toMySQL=False)
        
    
    def save(self):
        '''Adds this object to the database if no id exists, otherwise it updates'''
        self.fix_bools()
        if self.id==None:
            #Add
            if self.timestamp == None or len(self.timestamp)==0:
                self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            res = db.INSERT("world_state", self.__dict__)
            if res:
                self.id = res
        else:
            #Update
            res = db.UPDATE("world_state",{"id":self.id},self.__dict__)
        self.fix_bools(toMySQL=False)
        return res > 0
    
    def fix_bools(self,toMySQL=True):
        ''' because booleans must be a 0 or a 1 in mysql here '''
        self.isdaytime = fix_bool(self.isdaytime,toMySQL)
        self.islighton = fix_bool(self.islighton,toMySQL)
        self.isdrillon = fix_bool(self.isdrillon,toMySQL)
        
def getCount():
    res = db.CUSTOM_SELECT("SELECT COUNT(id) AS count FROM world_state")
    return res[0]['count']

def getFiltered(filters={},limit=-1,orderby='',ascending='False',offset=-1):
    ''' Get a list of filtered Logs '''
    res = db.SELECT("world_state", filters,limit=limit,orderby=orderby,offset=offset,ascending=ascending)
    rlist = []
    for values in res:
        rlist.append(World_State(**values))
    return rlist

def getAll(limit=-1,orderby='',ascending='False'):
    ''' Get a list of all Logs '''
    res = db.SELECT("world_state", {},limit=limit,orderby=orderby,ascending=ascending)
    rlist = []
    for values in res:
        rlist.append(World_State(**values))
    return rlist

def get(id=None):
    ''' Get an Activity Log based on given id'''
    if id==None:
        return None
    
    res = db.SELECT("world_state", 
                     {'id':id})
    if len(res)>0:
        if len(res)>1:
            #This shouldn't really happen unless if null value in db
            #this exists but isn't desired and is effectively a
            #useless entry until fixed, return the first anyway
            #but first, report this
            print("""Warning: SELECT statement returned more than one 
                value when only one should exist! id=%s
                """ % (str(id),))
        return World_State(**res[0])
    else:
        return None
        