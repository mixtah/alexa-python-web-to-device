'''
Created on 18 Jul 2016

@author: Michael

@sumary: MySQL db API for Club Manager Lite
'''
import DBAdapter
import MySQLdb
from datetime import datetime
import unicodedata

class MySQLAdapter(DBAdapter.Adapter):
    '''
        Is a generic adapter to connect to my MySQL database.
        
        TODO: 
        -Add generic functions to support installation and uninstallation of modules
        --Add table, remove table
        --Add column in table, remove " " "
        --Modify column maybe? I may want to intentionally not add this since modifying
            columns created by some other module may cause data integrity issues.
        
        This way it should be easier to simply use a different Database given a 
        different database brand. Useful to implement would be SQLite and Postgres.
        These other implementations may cause issues for any 'custom' queries which may 
        currently use MySQL specific commands. 
    '''
    
#Pythonanywhere database servers are shared and use Greenwich Mean Time (+0). 
#As the database itself cannot be changed, and it's a problem that will likely pop 
#up elsewhere, it's a good idea to open mysql in a particular timezone, problem is 
#that there isn't a good config setting for it so the below statement sets the timezone.
#This however didn't work properly as it needs to be set on each connection.
#TODO:
#I'm leaving this function here as a reminder to find a better solution than to 
#before every statement, run the SET time_zone statement. At least for now 
#the timezone issue is solved but probably at a cost of an extra ~1ms per execution.

    
    def QUERY(self,statement,params=None,giveId=False):
        '''
            Performs a general SQL statement and returns the number of rows that has changed. 
            When Selecting data, use CUSTOM_SELECT
        '''
        if self.debug:
            try:
                print(statement % tuple(params))
            except:
                print(statement)
        #execute statement
        try:
            db = MySQLdb.connect(**self.config)
            cur = db.cursor()
            if self.timezone:
                cur.execute('''SET time_zone="%s"'''%self.timezone)
            
            if params==None:
                cur.execute(statement)
            else:
                cur.execute(statement,params)
            
            if giveId:
                cid = cur.lastrowid
            else:
                cid = cur.rowcount
            db.commit()
            db.close()
            return cid 
        except Exception as err:
            print("Exception: ",err)
            return None
    
    def CUSTOM_SELECT(self,statement,params=None):
        '''
            Allows more specific SELECT statement usage beyond what is supported with the SELECT function. 
            It is potentially vulnerable to SQLi attacks to be sure ALL user entered data is screened first.
            Returns a List of Dicts, each Dict a row and keys correspond to selected columns.
        '''
        #execute statement
        if self.debug:
            try:
                print(statement % tuple(params))
            except:
                print(statement)
        try:
            db = MySQLdb.connect(**self.config)
            cur = db.cursor()
            if self.timezone:
                cur.execute('''SET time_zone="%s"'''%self.timezone)
            
            if params==None:
                cur.execute(statement)
            else:
                cur.execute(statement,params)
            
            result = []
            
            for row in cur.fetchall():
                cols = []
                fixedRow = []
                for i in range(len(row)):
                    if isinstance(row[i], datetime):
                        fixedRow.append(row[i].strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        fixedRow.append(row[i])
                for i in cur.description:
                    cols.append(i[0])
                result.append(dict(zip(cols,fixedRow)))
            
            db.close()
            
            return result
        except Exception as err:
            print("Exception: ",err)
            return []
    
    def SELECT(self,table,filters,select="*",orderby='',ascending=True,limit=-1,offset=-1,set_or=False):
        '''
            A Generic SQL SELECT statement from 'table' with keys matching columns and their desired filter
            returning the columns specified in 'select' (list of strings). 'select' can also be just a string
            that is meant to represent that part of the statement (even '*' is possible and is the default)
        '''    
        #create generic statement
        #Create SELECT and FROM components
        if isinstance(select, str):
            statement = 'SELECT '+select+' FROM '+table
        else:
            statement = 'SELECT '
            for sel in select:
                if sel != None:
                    statement = statement+sel+','
            statement = statement[:-1] + ' FROM '+table
        #Create WHERE component
        vals = []
        split = 'AND '
        if set_or:
            split = 'OR '
        if len(filters)>0:
            statement = statement+' WHERE '
            for key,val in filters.items():
                if val != None:
                    if isinstance(val,tuple):
                        #Here any self defined comparisons such as greater than or less than
                        statement = statement+key+' '+val[0]+' %s '+split
                        vals.append(val[1])
                    else:
                        statement = statement+key+'=%s '+split
                        vals.append(val)
            statement = statement[:-(1+len(split))]
        #Create Order By component
        if len(orderby)>0:
            #The 'order by' here requires no quotations, 
            #as MySQLdb stupidly adds them for my convenience
            #I must validate 'orderby' myself
            orderby = self.clean(orderby)
            #Bleach outputs unicode and I don't want that
            orderby = unicodedata.normalize('NFKD', orderby).encode('ascii','xmlcharrefreplace')
            if not ';' in orderby:
                #As it's far enough through the current statement
                #making sure this isn't terminated and another started
                #prevents any actual information from being leaked. 
                statement = statement+" ORDER BY "+orderby
                if ascending:
                    statement = statement+" ASC"
                else:
                    statement = statement+" DESC"
        #Create LIMIT component
        if limit>0:
            statement = statement+" LIMIT "+str(limit)
            
        #Create ORDERBY component
        if offset>0:
            statement = statement+" OFFSET "+str(offset)
        
        if self.debug:
            print(statement % tuple(vals))
        #execute statement
        try:
            db = MySQLdb.connect(**self.config)
            cur = db.cursor()
            if self.timezone:
                cur.execute('''SET time_zone="%s"'''%self.timezone)
            
            cur.execute(statement,tuple(vals))
            
            result = []
            
            for row in cur.fetchall():
                cols = []
                fixedRow = []
                for i in range(len(row)):
                    if isinstance(row[i], datetime):
                        fixedRow.append(row[i].strftime('%Y-%m-%d %H:%M:%S'))
                    else:
                        fixedRow.append(row[i])
                for i in cur.description:
                    cols.append(i[0])
                result.append(dict(zip(cols,fixedRow)))
            
            db.close()
            
            return result
        except Exception as err:
            print("Exception: ",err)
            return []
    
    def DELETE(self,table,filters):
        '''
            A Generic SQL DELETE statement into 'table' with keys matching columns and their desired filters
        '''
        
        statement = 'DELETE FROM '+table
        #clean the dirty dirty data
        for key in filters.keys():
            if isinstance(filters[key],str):
                filters[key] = self.clean(filters[key]).encode('ascii', 'xmlcharrefreplace')
                
        vals = []
        if len(filters)>0:
            statement = statement+' WHERE '
            for key,val in filters.items():
                if val != None:
                    if isinstance(val,tuple):
                        if len(val)==1:
                            statement = statement+key+' '+val[0]+' AND '
                        else:
                            #Here any self defined comparisons such as greater than or less than
                            statement = statement+key+' '+val[0]+' %s AND '
                            vals.append(val[1])
                    else:
                        statement = statement+key+'=%s AND '
                        vals.append(val)
            statement = statement[:-5]
        
        if self.debug:
            print(statement % tuple(vals))
        #execute statement
        try:
            db = MySQLdb.connect(**self.config)
            cur = db.cursor()
            if self.timezone:
                cur.execute('''SET time_zone="%s"'''%self.timezone)
            
            cur.execute(statement,tuple(vals))
            
            
            rowcount = cur.rowcount
            db.commit()
            db.close()
            return rowcount 
        except Exception as err:
            print("Exception: ",err)
            return 0
    
    def INSERT(self,table,values,giveId=True):
        '''
            A Generic SQL INSERT statement into 'table' with keys matching columns and their desired values
        '''
        #clean the dirty dirty data
        for key in values.keys():
            if isinstance(values[key],str):
                values[key] = self.clean(values[key]).encode('ascii', 'xmlcharrefreplace')
        
        #create generic statement
        statement = 'INSERT INTO '+table+' ('
        vals = []
        count = 0
        for key,val in values.items():
            if val != None:
                statement = statement+''+key+','
                vals.append(val)
                count += 1
        statement = statement[:-1]+') VALUES ('
        for i in range(count):
            statement = statement+'%s,'
        statement = statement[:-1]+')'
        
        if self.debug:
            print(statement % tuple(vals))
        #execute statement
        try:
            db = MySQLdb.connect(**self.config)
            cur = db.cursor()
            if self.timezone:
                cur.execute('''SET time_zone="%s"'''%self.timezone)
            
            cur.execute(statement,tuple(vals))
            
            if giveId:
                cid = cur.lastrowid
            else:
                cid = cur.rowcount
            db.commit()
            db.close()
            return cid 
        except Exception as err:
            print("Exception: ",err)
            return None
    
    def UPDATE(self,table,filters,values):
        #clean the dirty dirty data
        for key in values.keys():
            if isinstance(values[key],str):
                values[key] = self.clean(values[key]).encode('ascii', 'xmlcharrefreplace')
        
        #create generic statement
        statement = 'UPDATE %s SET ' % table
        vals = []
        for key,val in values.items():
            if val != None:
                #Only want to handle strings for now
                val = str(val)
                if val.startswith(key):
                    #be careful here, val isn't necessarily sanitized
                    statement = statement+key+'='+val+','
                else:
                    statement = statement+key+'=%s,'
                    #Because mysql hates booleans
                    if val.upper()=="TRUE":
                        vals.append("1")
                    elif val.upper()=="FALSE":
                        vals.append("0")
                    else:
                        vals.append(val)
        statement = statement[:-1]+' WHERE '
        for key,val in filters.items():
            if val != None:
                if isinstance(val,tuple):
                    if len(val)==1:
                        statement = statement+key+' '+val[0]+' AND '
                    else:
                        #Here any self defined comparisons such as greater than or less than
                        statement = statement+key+' '+val[0]+' %s AND '
                        vals.append(val[1])
                else:
                    statement = statement+key+'=%s AND '
                    vals.append(val)
        statement = statement[:-5]
        
        if self.debug:
            print(statement % tuple(vals))
        #execute statement
        try:
            db = MySQLdb.connect(**self.config)
            cur = db.cursor()
            if self.timezone:
                cur.execute('''SET time_zone="%s"'''%self.timezone)
            
            cur.execute(statement,tuple(vals))
            
            rowcount = cur.rowcount
            db.commit()
            db.close()
            return rowcount 
        except Exception as err:
            print("Exception: ",err)
            return 0

    
    