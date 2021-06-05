
############################################################### Python Imports ####################################################

from flask import Flask, render_template, request, redirect, url_for
import sys
import mysql.connector
from tabulate import tabulate
from mysql.connector import Error
import os
import csv
import io
import pandas as pd
import numpy as np
from IPython.display import HTML 
from IPython.display import display 
from Decomp import *
import re
import itertools
from functools import reduce
import operator

############################################################### Split Input ##############################################################
def is_valid_input(R, FD_s):
    """
    Check if input is valid
    1) If functional dependency has something that is not in relations
    2) If functional dependency is singleton
    :param R: relation set given by user
    :param FD_s: functional dependency list provided by user
    :return: True if no error else False
    """
    set_FDs = [set(i.lh + i.rh) for i in FD_s]
    reduced_FD_set = reduce(operator.or_, set_FDs)

    # Returns False if functional dependency is not a subset of R
    return reduced_FD_set.issubset(R) or reduced_FD_set == R


def split_input(input_list):
    """
    Split the given input into required format for
    converting input list ['A->B', 'C->E']
    to fd1 = FDependency(['A'], ['B'])
    fd2 = FDependency(['C'], ['E'])
        FD_s = FDependencyList([fd1, fd2])

    :param input_list: input from web app
    :return: FDependencyList object
    """

    # Test examples
    # ['A->B', 'C->E']
    # ['A,B->C', 'C->D', 'C,D->E']

    # Split ['A->B', 'C->E'] to [['A,X', 'B'], ['C', 'E']]
    fd_arrow_split_list = [x.split("->") for x in input_list]

    # Split [['A,X', 'B'], ['C', 'E']] to ['A','X'], ['B'] and ['C'],['E']
    fd_list = [FDependency(fd[0].split(","), [fd[1]])
               for fd in fd_arrow_split_list]

    # Create object
    fd_list_obj = FDependencyList(fd_list)

    return fd_list_obj

############################################################# Second Normal Form ###########################################################

def check_2NF(R, FD_list, proposal=True):
    """
    Check If the Relation and its functional dependencies
    is in 2 normalised form- 2NF
    :param R: relation
    :param FD_s:  list of functional dependencies
    
    """

    N = Normalization()
    D = Decomposition()

    merge=[]
    final_output=[]
    FD_s = split_input(FD_list)
    FD_list_output = str(FD_s)
    FD_list_output = FD_list_output.replace('],', ']<br/><br/>') + '\n'

    if is_valid_input(R,FD_s):
        list_fd = f'<h3><u>Given FD List</u></h3>\n'
        FD_list_output = str(FD_s)
        FD_list_output = FD_list_output.replace('],', ']<br/><br/>') + '\n'

        minFds = FD_s.MinimalCover()
        minFds_output = str(minFds)
        minFds_output = minFds_output.replace('],', ']<br/><br/>')
        minFds_output = f'\n<hr></hr><h3><u>MinCover</u></h3>\n {minFds_output}'

        allKeys = N.findCandKeys(R, minFds, FD_s)
        allKeys_output = f'\n\n<hr></hr><h3><u>Keys</u></h3>\n  {allKeys}'


        for fd in minFds:
            lhs = set(fd.lh)
            rhs = set(fd.rh)
            violation = f"\n\n<hr></hr><h3><u>2NF is in violation for</u></h3>\n"
            if (N.check2NF(fd, lhs, rhs, allKeys)):   
                c2= N.FDList2NF
            violation_output=str(c2)
            violation_output=violation_output.replace('],', ']<br/><br/>')
        if proposal:
            two_NF = N.proposal2NF(fd, lhs, rhs, allKeys)
            # Add the master dependencies that are not handled in 2NF
            missing_dependency = [dependency for dependency in FD_s
                                  if dependency not in two_NF]

            # Print 2NF proposal first
            
            merge_print = ""
            merge_print = merge_print + '\n\n<hr></hr><h3><u>2NF PROPOSAL</u></h3>'  
            merge_print = merge_print + "<br/>Merge the below functional " \
                                        "dependencies to create a new relation"

            for i in two_NF:
                merge_print = merge_print + f"<br/><br/>&#9;{set(i.lh + i.rh)} : {i}"
            
            merge_print = merge_print + "<br/><br/>Create the below relations " \
                                        "along with above 2NF proposals"
            for i in missing_dependency:
                merge_print = merge_print + f"<br/><br/>&#9;{set(i.lh + i.rh)} : {i}"             

    else:

        list_fd = f"<u><h3>Given Attributes</h3></u><br/>{R}<br/><br/>"
        FD_list_output = f"<u><h3>Given FD list</h3></u><br/>{FD_list_output}<br/><br/>"
        minFds_output = "<b style=\"color: #FF8C00\";'>ERROR: Check your input!<br/><br/>"
        allKeys_output = "\tFunctional dependency has attributes that are not in relation set.<br/><br/>"
        violation = "\t OR<br/><br/>"
        violation_output = "\tRight hand side of functional dependency is not singleton.<br/><br/> "
        merge_print = "Split it and provide as two separate relations</b><br/><br/>"
        

    return(list_fd + FD_list_output + minFds_output + allKeys_output + violation + violation_output + merge_print )


############################################################# Third Normal Form ###########################################################

def check_3NF(R, FD_list, proposal=True):
    """
    Check If the Relation and its functional dependencies
    is in 3 normalised form- 3NF
    :param R: relation
    :param FD_s:  list of functional dependencies

    """

    N = Normalization()
    D = Decomposition()

    FD_s = split_input(FD_list)
    if is_valid_input(R, FD_s):

        list_fd = f'<h3><u>Given FD List</u></h3>\n'
        FD_list_output = str(FD_s)
        FD_list_output = FD_list_output.replace('],', ']<br/><br/>') + '\n'

        minFds = FD_s.MinimalCover()
        minFds_output = str(minFds)
        minFds_output = minFds_output.replace('],', ']<br/><br/>')
        minFds_output = f'\n<hr></hr><h3><u>MinCover</u></h3>\n {minFds_output}'

        allKeys = N.findCandKeys(R, minFds, FD_s)
        allKeys_output = f'\n\n<hr></hr><h3><u>Keys</u></h3>\n  {allKeys}'
        
        for fd in minFds:
            lhs = set(fd.lh)
            rhs = set(fd.rh)
            
            violation = f"\n\n<hr></hr><h3><u>3NF is in violation for</u></h3>\n"
            if (N.check3NF(fd, lhs, rhs, allKeys)):   
                c2= N.FDList3NF
            violation_output=str(c2)
            violation_output=violation_output.replace('],', ']<br/><br/>')

        if proposal:
            three_NF = D.proposal3NF(R, minFds, FD_s)
            merge_print = ""
            merge_print = merge_print + '\n\n<hr></hr><h3><u>3NF PROPOSAL</u></h3>'
            
            for i in three_NF:
                merge_print = merge_print + f"<br/><br/>&#9;{i[0]} {i[1]} <br/>"

    else:

        list_fd = f"<u><h3>Given Attributes</h3></u><br/>{R}<br/><br/>"
        FD_list_output = f"<u><h3>Given FD list</h3></u><br/>{FD_list_output}<br/><br/>"
        minFds_output = "<b style=\"color: #FF8C00\";'>ERROR: Check your input!<br/><br/>"
        allKeys_output = "\tFunctional dependency has attributes that are not in relation set.<br/><br/>"
        violation = "\t OR<br/><br/>"
        violation_output = "\tRight hand side of functional dependency is not singleton.<br/><br/> "
        merge_print = "Split it and provide as two separate relations</b><br/><br/>"
   
    return(list_fd + FD_list_output + minFds_output + allKeys_output + violation + violation_output + merge_print )

################################################################# BCNF ##############################################################

def check_BCNF(R, FD_list, proposal=True):
    """
    Check If the Relation and its functional dependencies
    is in 3 normalised form- 3NF
    :param R: relation
    :param FD_s:  list of functional dependencies

    """

    N = Normalization()
    D = Decomposition()

    FD_s = split_input(FD_list)
    if is_valid_input(R, FD_s):

        list_fd = f'<h3><u>Given FD List</u></h3>\n'
        FD_list_output = str(FD_s)
        FD_list_output = FD_list_output.replace('],', ']<br/><br/>') + '\n'

        minFds = FD_s.MinimalCover()
        minFds_output = str(minFds)
        minFds_output = minFds_output.replace('],', ']<br/><br/>')
        minFds_output = f'\n<hr></hr><h3><u>MinCover</u></h3>\n {minFds_output}'

        allKeys = N.findCandKeys(R, minFds, FD_s)
        allKeys_output = f'\n\n<hr></hr><h3><u>Keys</u></h3>\n  {allKeys}'
        
        for fd in minFds:
            lhs = set(fd.lh)
            rhs = set(fd.rh)
            
            violation = f"\n\n<hr></hr><h3><u>BCNF is in violation for</u></h3>\n"
            if (N.checkBCNF(fd, lhs, rhs, allKeys)):   
                c2= N.FDListBCNF
            violation_output=str(c2)
            violation_output=violation_output.replace('],', ']<br/><br/>')

        if proposal:
            bc_NF = D.proposalBCNF(R, FD_s)
            merge_print = ""
            merge_print = merge_print + '\n\n<hr></hr><h3><u>BCNF PROPOSAL</u></h3>'
            
            for i in bc_NF:
                merge_print = merge_print + f"<br/><br/>&#9;{i[0]} {i[1]} <br/>"

    else:

        list_fd = f"<u><h3>Given Attributes</h3></u><br/>{R}<br/><br/>"
        FD_list_output = f"<u><h3>Given FD list</h3></u><br/>{FD_list_output}<br/><br/>"
        minFds_output = "<b style=\"color: #FF8C00\";'>ERROR: Check your input!<br/><br/>"
        allKeys_output = "\tFunctional dependency has attributes that are not in relation set.<br/><br/>"
        violation = "\t OR<br/><br/>"
        violation_output = "\tRight hand side of functional dependency is not singleton.<br/><br/> "
        merge_print = "Split it and provide as two separate relations</b><br/><br/>"
   
    return(list_fd + FD_list_output + minFds_output + allKeys_output + violation + violation_output + merge_print )

############################################################### Primary Key Candidates ####################################################

def is_subkey(newkey,keys):

    for key in keys:
        if set(key).issubset(newkey):
            return True
    return False

def Possible_PrimaryKeys(data,max_num=4):
    doc = data
    num = 1
    result = []
    table_length = len(doc.values)

    while num <= max_num:
        keys = list(itertools.combinations(doc.columns,num))
        for key in keys:
            if is_subkey(key,result):
                continue          
            bools = np.array(doc.duplicated(subset=list(key)))
            if np.sum(bools) > 0:

                continue
            else:
                result.append(list(key))
        num += 1
    return result

########################################################## MySQL - Database Connection #######################################################

def db_connect(host, database, user, password):
    try:
        connection = mysql.connector.connect(
            host = host,
            database = database,
            user = user,
            password = password,
            auth_plugin = 'mysql_native_password')
        if connection.is_connected():
            # Successful Connection to the Database
            return connection

    except Error as err:
        # Failed DB Connectivity
        sys.exit(f'Failed to connect to database:\n{err}')



################################################## Retreiving Table Names for the given Database - SHOW Tables ###############################

def show_tables(db_connection):
    cursor = db_connection.cursor()
    cursor.execute('SHOW TABLES')

    for row in cursor:
        yield row[0] # Return field name



################################################### Retrieving the Table Details - DESCRIBE TABLE #############################################

def describe_tables(db_connection, table_name):
    cursor = db_connection.cursor(dictionary=True)
    cursor.execute(f'DESCRIBE {table_name}')
    result = cursor.fetchall()
    

    if not result:
        raise Error(f'Table {table_name} doesn\'t exist!!! Please give the correct table name!')

    fields = []
    primary_keys = []

    for row in result:
        field = row['Field']
        fields.append(field)
        
        if row['Key'] == 'PRI': # Primary Key Check
            primary_keys.append(field)
    
    return {'fields': fields, 'primary_keys': primary_keys}

def is_unique(fd_check):
    a = fd_check.to_numpy() 
    return (a[0] == a).all()



######################################################## First Normal Form - Files #######################################################

def FirstNF_file(file):
     
    file_data =[]
    for row in file:
        file_data.append(row)
    header = file_data[0]
    File = '<hr></hr>' + '<h3><u>File Data</u></h3>' + '<hr></hr>' + '\n\n'
    data=pd.DataFrame(file_data[1:len(file_data)], columns=header)
    
    
    keys = Possible_PrimaryKeys(data)
    key = '\n' +  '<hr></hr>' + '<h3><u>' +    'POSSIBLE PRIMARY KEYS CANDIDATES' +  '</u></h3>' +  '<hr></hr>' + '\n'
    if len(keys)>0:   
        key1 = str(keys) 
        key1 = key1.replace('],',']<br><br>')
        key1 = key1.replace('[[','[')
        key1 = key1.replace(']]',']')
    else:
        key1="There is no possible primary keys candidates found for this file!"+ '\n'


    #To check unique column name
   
    a = '\n' +  '<hr></hr>' + '<h3><u>' +    'CHECKING FOR DUPLICATE COLUMNS' +  '</u></h3>' +  '<hr></hr>' + '\n'
    column=list(data.columns)
    check=[]
    for i in column:
        if i in check:
             dup_col = 'Duplicate column names found for this file : ' + '\n<h3>' + i +'</h3>'
           
        else:
            check.append(i)
            dup_col='The Columns are unique for this file!' + '\n'

    #To check Duplicate rows

    b = '\n\n' +  '<hr></hr>' + '<h3><u>' +   'CHECKING FOR DUPLICATE ROWS' +  '</u></h3>' +  '<hr></hr>' + '\n'
    duplicateRowsDF = data[data.duplicated()]
    dt=data.duplicated()
    
    if dt.any() == True:
        duplicate_row='Below are the duplicate rows found for this file :' + '\n\n'
        duplicate_rout=duplicateRowsDF
        duplicate_rout=duplicate_rout.to_html()
       
    else:
        duplicate_row='There are no Duplicate Rows present for this file!' + '\n'
        duplicate_rout=''
  
  
    #Code to check atomic values

    c = '\n\n' +  '<hr></hr>' + '<h3><u>' +   '1NF PROPOSAL' +  '</u></h3>' +  '<hr></hr>' 
    count=0
    for i in column:
        lst=[]
        non_atomic={}
        for j in data[i]:
            k=str(j)
            if ',' in k:
                lst.append(k)
                count+=1
                non_atomic[i]=lst

        if non_atomic:
    	    df = pd.DataFrame(non_atomic)
    	    df = df.head()           
                    
    if count==0:
        d = '\n' +  'File Data is already in First Normal Form' + '\n\n' + data.to_html()
    else:
        d = '\n\n' + 'File Data is not in First Normal Form, since the below column has Multi-Valued Attributes for a given file'  + '\n\n'   + df.to_html()    
        

    return(File + data.to_html()  + a + dup_col + b + duplicate_row + str(duplicate_rout) + c + d + key + str(key1) )

######################################################## First Normal Form - Tables  #######################################################
    
def FirstNF_db(db_connection, table_name):

    table_description = describe_tables(db_connection, table_name)
    
    fields = table_description['fields']
    cursor = db_connection.cursor(buffered=True)

    cursor.execute("SELECT * from %s LIMIT 10 " % table_name)
    with open("static/output/output_1NF.csv","w") as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in cursor.description)
        for row in cursor:
            writer.writerow(row)

   
    Table = f'\n<hr></hr><h3>Table Name : \'{table_name}\'' + ' </h3><hr></hr><br>'
    cursor = db_connection.cursor(buffered=True)

    cursor.execute("SELECT * from %s LIMIT 10 " % table_name)
    myresult = cursor.fetchall()
    field_names = [i[0] for i in cursor.description] 
    

    data = pd.read_csv("static/output/output_1NF.csv") 
    tab_data = data.to_html()

    keys = Possible_PrimaryKeys(data)
    key = '\n' +  '<hr></hr>' + '<h3><u>' +    'POSSIBLE PRIMARY KEYS CANDIDATES' +  '</u></h3>' +  '<hr></hr>' + '\n'
    if len(keys)>0:   
        key1 = str(keys) 
        key1 = key1.replace('],',']<br><br>')
        key1 = key1.replace('[[','[')
        key1 = key1.replace(']]',']')
    else:
        key1="There is no possible primary keys candidates found for this table!"+ '\n'

    #To check unique column name

    star = '*'
    a = '\n' +  '<hr></hr>' + '<h3><u>' +    'CHECKING FOR DUPLICATE COLUMNS' +  '</u></h3>' +  '<hr></hr>' + '\n'
    column=list(data.columns)
    check=[]
    for i in column:
        if i in check:
             dup_col = 'Duplicate column names found for this Table : ' + '\n<h3>' + i +'</h3>'
           
        else:
            check.append(i)
            dup_col='The Columns are unique for this Table since MYSQL doesnt allow duplicate columns while creating a table!' + '\n'

    #To check Duplicate rows

    b = '\n\n' +  '<hr></hr>' + '<h3><u>' +   'CHECKING FOR DUPLICATE ROWS' +  '</u></h3>' +  '<hr></hr>' + '\n'
    duplicateRowsDF = data[data.duplicated()]
    dt=data.duplicated()
    
    if dt.any() == True:
        duplicate_row='Below are the duplicate rows found for this Table :' + '\n\n'
        duplicate_rout=duplicateRowsDF
        duplicate_rout=duplicateRowsDF.to_html()
        
    else:
        duplicate_row='There are no Duplicate Rows present for this Table!' + '\n'
        duplicate_rout=''
        
    #Code to check atomic values

    c = '\n\n' +  '<hr></hr>' + '<h3><u>' +   '1NF PROPOSAL' +  '</u></h3>' +  '<hr></hr>' 
    count=0
    for i in column:
        lst=[]
        non_atomic={}
        for j in data[i]:
            k=str(j)
            if ',' in k:
                lst.append(k)
                count+=1
                non_atomic[i]=lst

        if non_atomic:
    	    df = pd.DataFrame(non_atomic)
    	    df = df.head()           
                    
    if count==0:
        d = '\n\n' +  'Table Data is already in First Normal Form' + '\n\n' + data.to_html()
    else:
        d = '\n\n' + 'Table Data is not in First Normal Form, since the below column has Multi-Valued Attributes for the given table'  + '\n\n'   + df.to_html()    
        

    return(Table + str(tab_data)  + a + dup_col + b + duplicate_row + str(duplicate_rout) + c + d + key + str(key1) )

######################################################## Functional Dependency - Tables  #######################################################

def functional_dependency(db_connection, table_name):
    table_description = describe_tables(db_connection, table_name)
    
    fields = table_description['fields']
    cursor = db_connection.cursor(buffered=True)

    cursor.execute("SELECT * from %s LIMIT 10 " % table_name)
    with open("static/output/output_fd.csv","w") as outfile:
        writer = csv.writer(outfile, quoting=csv.QUOTE_NONNUMERIC)
        writer.writerow(col[0] for col in cursor.description)
        for row in cursor:
            writer.writerow(row)

    
    Table = '<hr></hr>' + '<h3><u>Table Data</u></h3>' + '<hr></hr>' + '\n\n'
    data = pd.read_csv("static/output/output_fd.csv") 
    d = data.to_html()

    keys = Possible_PrimaryKeys(data)
    if len(keys)>0:   
        key1 = str(keys) 
        key1 = key1.replace('],',']<br><br>')
        key1 = key1.replace('[[','[')
        key1 = key1.replace(']]',']')
        b = '\n\nPossible Primary key candidates found for this table: \n\n' + key1
    else:
        b="There is no possible primary keys candidates found for this table!"+ '\n'

    func_depends = []
    result_fd=[]
    cursor.execute("SELECT * from %s LIMIT 10 " % table_name)
    myresult = cursor.fetchall()
    field_names = [i[0] for i in cursor.description] 

    

    for i in range(0, len(fields)):
        for j in range(0, len(fields)):
            if (i == j):
                continue

            field_1 = fields[i]
            field_2 = fields[j]
            
            cursor.execute(f'SELECT {field_1}, COUNT(DISTINCT {field_2}) c FROM {table_name} GROUP BY {field_1} HAVING c > 1')

            if (cursor.rowcount == 0):
                func_depends.append(f'{field_1} -> {field_2}')  
    
    # Print results
    a = f'\n<hr></hr><h3>Table Name : \'{table_name}\'' + ' </h3><hr></hr><br>'
    if func_depends:
        c = '\n\nFollowing are the functional dependencies found for this table : ' + '\n'
        
        for fd in func_depends:
            #print('\n')
            result_fd.append('\n' + fd +'\n')
    else:
        result_fd = '\n\nThere were no functional dependencies found for this table.'
    
    return(a + str(d) + b + c + ' '.join(result_fd))


#######################################################   Functional Dependency - Files   ######################################################  

def file_fd(file):
   
    data =[]
    for row in file:
        data.append(row)
    header = data[0]

    func_depends = []
    result_fd=[]


    File = '<hr></hr>' + '<h3><u>File Data</u></h3>' + '<hr></hr>' + '\n\n'
    df=pd.DataFrame(data[1:len(data)], columns=header) 
    #print(df)

    keys = Possible_PrimaryKeys(df)
    if len(keys)>0:   
        key1 = str(keys) 
        key1 = key1.replace('],',']<br><br>')
        key1 = key1.replace('[[','[')
        key1 = key1.replace(']]',']')
        b = '\n\nPossible Primary key candidates found for this file: \n\n' + key1
    else:
        b="There is no possible primary keys candidates found for this file!"+ '\n'

    for i in range(0, len(header)): 
        for j in range(0, len(header)):
            if (i == j):
                continue

            field_1 = header[i]
            field_2 = header[j]

            #print(field_1,field_2)

            df_1 = df.groupby(field_1)[field_2].nunique()
            dups_df = pd.DataFrame(df_1)
            
            if is_unique(dups_df[field_2]):
                func_depends.append(f'{field_1} -> {field_2}')
    
    # Print results
    
    
    if func_depends:
        c = '\n\n' + 'Following are the functional dependencies found for this file : ' + '\n\n'
        
        for fd in func_depends:
            result_fd.append('\n' + fd +'\n')
    else:
        result_fd = '\n\nThere were no functional dependencies found for this table.'

    return(File + df.to_html() + b + c + ' '.join(result_fd))
  
########################################################   MYSQL Password Check   ######################################################## 

class Password:
    DEFAULT = 'Prompt if password is not specified!!'

    def __init__(self, value):
        if value == self.DEFAULT:
            value = getpass.getpass('Password to the database: ')
        self.value = value

    def __str__(self):
        return self.value

##################################################  Database Connection Function - MYSQL #################################################

def db_fd(Hostname,Databasename,Username,Password,Table_Name):
    
    
     db_connection = db_connect(Hostname, Databasename, Username, Password)
     tables=[Table_Name]

     try:
        tables_to_examine = list(show_tables(db_connection)) if tables == 'all' else tables

        for table in tables_to_examine:
            result = functional_dependency(db_connection, table)
    
     except Error as err:
        sys.exit(f'An error occurred:\n{err}\nExiting...')

     finally:
        db_connection.close()
     return result


def db_1NF(Hostname,Databasename,Username,Password,Table_Name):
    
     
     db_connection = db_connect(Hostname, Databasename, Username, Password)
     tables=[Table_Name]

     try:
        tables_to_examine = list(show_tables(db_connection)) if tables == 'all' else tables

        for table in tables_to_examine:
            result = FirstNF_db(db_connection, table)
    
     except Error as err:
        sys.exit(f'An error occurred:\n{err}\nExiting...')

     finally:
        db_connection.close()
     return result


############################################################# Flask Calling ###########################################################  

app = Flask(__name__)
@app.route('/')
def home():
   return render_template("Normalization.html")

@app.route('/Home')
def homepage():
   return render_template("Home.html")

@app.route('/About')
def about():
   return render_template("About.html")

@app.route('/fdhome')
def fdhome():
   return render_template("Functional_Dependency.html")


@app.route('/1NF')
def First_NF():
   return render_template("First_NormalForm.html")

@app.route('/2NF')
def Second_NF():
   return render_template("Second_NormalForm.html")

@app.route('/3NF')
def Third_NF():
   return render_template("Third_NormalForm.html")

@app.route('/BCNF')
def BCNF():
   return render_template("BCNF.html")

@app.route('/Readme')
def Readme():
   return render_template("Readme.html")

################################################### Functional Dependency - Table ################################################# 

@app.route('/fd', methods=['GET', 'POST'])
def fd_output():
    if request.method == 'POST':
        Username = request.form["user"]
        Password = request.form["password"]
        Database_Name = request.form["database"]
        Host_Name = request.form["host"]
        Table_Name = request.form["table"]
        
        return render_template('Functional_Dependency.html',db_output=db_fd(Host_Name,Database_Name,Username,Password,Table_Name))  
    return redirect(url_for('fd_output'))

################################################## Functional Dependency - File ##################################################

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      if not f:
        return "No file"
      stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
      csv_input = csv.reader(stream)
      

      return render_template('Functional_Dependency.html',file_output=file_fd(csv_input))
   return redirect(url_for('upload_file'))

#########################################################  1NF - Table ##########################################################

@app.route('/1NF', methods=['GET', 'POST'])
def FirstNF_Table():
    if request.method == 'POST':
        Username = request.form["user"]
        Password = request.form["password"]
        Database_Name = request.form["database"]
        Host_Name = request.form["host"]
        Table_Name = request.form["table"]
        
        return render_template('First_NormalForm.html',db_output=db_1NF(Host_Name,Database_Name,Username,Password,Table_Name))  
    return redirect(url_for('FirstNF_Table'))

#########################################################  1NF - File ########################################################## 	

@app.route('/1NF_upload', methods = ['GET', 'POST'])
def FirstNF_uploadfile():
   if request.method == 'POST':
      f = request.files['file']
      if not f:
        return "No file"
      stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
      csv_input = csv.reader(stream)
      

      return render_template('First_NormalForm.html',file_output=FirstNF_file(csv_input))
   return redirect(url_for('FirstNF_uploadfile'))

######################################################  Second Normal Form ####################################################

@app.route('/2NF', methods=['GET', 'POST'])
def SecondNF_Table():
    if request.method == 'POST':
        Attributes = request.form["attr"]
        Attributes_list = Attributes.split(",")

        R = set(Attributes_list)
        Fd_list = request.form["fdlist"]
        FD_list = re.split(r"[~\r\n]+", Fd_list)
        
        return render_template('Second_NormalForm.html',Second_NF_output=check_2NF(R, FD_list,proposal=True))  
    return redirect(url_for('SecondNF_Table'))

###################################################### Thrid Normal Form ####################################################

@app.route('/3NF', methods=['GET', 'POST'])
def ThirdNF_Table():
    if request.method == 'POST':
        Attributes = request.form["attr"]
        Attributes_list = Attributes.split(",")

        R = set(Attributes_list)
        Fd_list = request.form["fdlist"]
        FD_list = re.split(r"[~\r\n]+", Fd_list)
        
        return render_template('Third_NormalForm.html',Third_NF_output=check_3NF(R, FD_list,proposal=True))  
    return redirect(url_for('ThirdNF_Table'))

##########################################################  BCNF ###########################################################

@app.route('/BCNF', methods=['GET', 'POST'])
def BCNF_Table():
    if request.method == 'POST':
        Attributes = request.form["attr"]
        Attributes_list = Attributes.split(",")

        R = set(Attributes_list)
        Fd_list = request.form["fdlist"]
        FD_list = re.split(r"[~\r\n]+", Fd_list)
        
        return render_template('BCNF.html',BCNF_output=check_BCNF(R, FD_list,proposal=True))  
    return redirect(url_for('BCNF_Table'))

if __name__ == '__main__':
   app.run(debug=True)