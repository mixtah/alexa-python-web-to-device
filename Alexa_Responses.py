'''
Created on 7 Feb 2017

@author: Michael
'''
from MySQLAdapter import MySQLAdapter
db = MySQLAdapter()

import time
from datetime import datetime,timedelta
TIME_FORMAT = '%Y-%m-%d %H:%M:%S'



class Alexa_Response(object):
    '''
    classdocs
    '''

    def __init__(self, **params):
        '''
        Constructor
        '''
        
        self.id = params.get('id',None)
        self.link = params.get('link',"")
        self.settings = params.get('settings','{}')
        self.timestamp = params.get('timestamp',None)
        
    
    def save(self):
        '''Adds this object to the database if no id exists, otherwise it updates'''
        
        if self.id==None:
            #Add
            if self.timestamp == None or len(self.timestamp)==0:
                self.timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
            res = db.INSERT("alexa_response", self.__dict__)
            if res:
                self.id = res
        else:
            #Update
            res = db.UPDATE("alexa_response",{"id":self.id},self.__dict__)
        return res > 0
    
        
def getCount():
    res = db.CUSTOM_SELECT("SELECT COUNT(id) AS count FROM alexa_response")
    return res[0]['count']

def getFiltered(filters={},limit=-1,orderby='',ascending='False',offset=-1):
    ''' Get a list of filtered Logs '''
    res = db.SELECT("alexa_response", filters,limit=limit,orderby=orderby,offset=offset,ascending=ascending)
    rlist = []
    for values in res:
        rlist.append(Alexa_Response(**values))
    return rlist

def getAll(limit=-1,orderby='',ascending='False'):
    ''' Get a list of all Logs '''
    res = db.SELECT("alexa_response", {},limit=limit,orderby=orderby,ascending=ascending)
    rlist = []
    for values in res:
        rlist.append(Alexa_Response(**values))
    return rlist

def get(id=None):
    ''' Get an Activity Log based on given id'''
    if id==None:
        return None
    
    res = db.SELECT("alexa_response", 
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
        return Alexa_Response(**res[0])
    else:
        return None
        