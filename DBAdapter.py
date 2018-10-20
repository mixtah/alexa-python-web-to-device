'''
Created on 18 Jul 2016

@author: Michael

@sumary: MySQL db API for Club Manager Lite
'''
from abc import ABCMeta, abstractmethod
import settings
import bleach

class Adapter(object):
    '''
        Basic Template for a Database Adapter
    '''
    __metaclass__ = ABCMeta

    def __init__(self, config=settings.CONFIG,debug=settings.DEBUG,timezone=settings.TIME_ZONE):
        self.config = config
        self.debug = debug
        self.timezone = timezone
    
    
    def clean(self,text):
        #Dereference some html so that bleach can understand what to strip.
        #Summernote has a really annoying Security Vuln where referenced html 
        #will be dereferenced before displaying in the editor. As we load existing
        #cleaned content into a summernote instance, it will dereference the clean &lt; etc
        #which may then reveal some XSS code. Only safe way now is to strip it all together,
        #still, if someone inserts &lt; it may still get in, so these need to also be catered for.
        while '&amp;' in text:
            text = text.replace('&amp;','&')
        for deref in settings.DEREFERENCE_HTML:
            text = text.replace(deref[0],deref[1])
        #Clean everything and strip anything we don't want.
        return bleach.clean(text,
                       tags=settings.ALLOWED_TAGS, 
                       attributes=settings.ALLOWED_ATTRIBUTES,
                       styles=settings.ALLOWED_STYLES,
                       strip=True,
                       strip_comments=True
                       )
    
    @abstractmethod
    def QUERY(self,statement,params=None,giveId=False):
        '''
            Performs a general SQL statement and returns the number of rows that has changed. 
            When Selecting data, use CUSTOM_SELECT
        '''
        return NotImplemented
    
    @abstractmethod
    def CUSTOM_SELECT(self,statement,params=None):
        '''
            Allows more specific SELECT statement usage beyond what is supported with the SELECT function. 
            It is potentially vulnerable to SQLi attacks to be sure ALL user entered data is screened first.
            Returns a List of Dicts, each Dict a row and keys correspond to selected columns.
        '''
        #execute statement
        return NotImplemented
    
    @abstractmethod
    def SELECT(self,table,filters,select="*",orderby='',ascending=True,limit=-1,offset=-1,set_or=False):
        '''
            A Generic SQL SELECT statement from 'table' with keys matching columns and their desired filter
            returning the columns specified in 'select' (list of strings). 'select' can also be just a string
            that is meant to represent that part of the statement (even '*' is possible and is the default)
        '''    
        return NotImplemented
    
    @abstractmethod
    def DELETE(self,table,filters):
        '''
            A Generic SQL DELETE statement into 'table' with keys matching columns and their desired filters
        '''
        
        return NotImplemented
    
    @abstractmethod
    def INSERT(self,table,values,giveId=True):
        '''
            A Generic SQL INSERT statement into 'table' with keys matching columns and their desired values
        '''
        return NotImplemented
    
    @abstractmethod
    def UPDATE(self,table,filters,values):
        '''
            A Generic SQL UPDATE statement into 'table' with keys matching columns and their desired values
        '''
        return NotImplemented
    
    
    