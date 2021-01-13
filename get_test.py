import sqlite3
from sqlite3 import Error
from random import randint
from googletrans import Translator

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select_question_count(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("""select count(*) 
                     from question""")
    
    return cur.fetchone()[0]


def select_random_question(conn, number):
    """
    Query question by number
    :param conn: the Connection object
    :param number:
    :return:
    """
    cur = conn.cursor()
    cur.execute(""" with TBL_COR_CNT as
 (
   select t.id
         ,count(t.id) nCACNT
		 ,group_concat('<ANSW val = "'||t.ANSWER_TEXT||'"/>', '') as sCA
     from (select * from answer order by random())t
	 where t.IS_CORRECT = 'true'
	 group by t.id
 ),
 TBL_NCOR_CNT as
 (
   select t.id
         ,count(t.id) nNCACNT
		 ,group_concat('<ANSW val = "'||t.ANSWER_TEXT||'"/>', '') as sNCA
     from (select * from answer order by random())t
	 where t.IS_CORRECT = 'false'
	 group by t.id
 ),
 tbl_src as
 (
 select distinct
	    q.*
       ,count(a.id) OVER ( 
        PARTITION BY q.id
        ) as nACNT
	   ,tc.nCACNT as nCACNT
	   ,'<COR>'||tc.sCA||'</COR>' as sCOR_ANSW
	   ,tnc.nNCACNT as nNCACNT
	   ,'<NCOR>'||tnc.sNCA||'</NCOR>' as sNCOR_ANSW
  from question q left join answer a on q.id = a.id
                  left join TBL_COR_CNT tc on q.id = tc.id
				  left join TBL_NCOR_CNT tnc on q.id = tnc.id
),
TBL_PRE as
(
select row_number() over(order by 1) as nROW
      ,t.*
  from tbl_src t
) 
select t.*
  from TBL_PRE t
  where t.nROW = ?""", (number,))

    rows = cur.fetchall()
    
    return rows
    


def main():
    database = r"i:\Python\1z0071_test\quizframework_test_db.db"

    # create a database connection
    conn = create_connection(database)
    
    rows = set()
    text_to_translate = []
    with conn:
        randnum = randint(1, select_question_count(conn))
        print(f"1. Query random question number {randnum}:")
        
        rows = select_random_question(conn, randnum)
    
    for row in rows:
        print(row)
        print(row[2])
        print(row[4])
        
        """text_to_translate.append(row[2])
        text_to_translate.append(row[4])
    translations = Translator()
    translations = translations.translate(text=text_to_translate, dest='ru')
    for translation in translations:
        print(translation.origin, ' -> ', translation.text)"""

"""
import xml.etree.ElementTree as ET
from itertools import *
from math import * 
from random import randint

corroot = ET.fromstring("<COR><ANSW val = "CREATE TABLE my_table (my_data CHAR, CONSTRAINT my_c CHECK (my_data IS NOT NULL));"/><ANSW val = "CREATE TABLE my_table (my_data CHAR, CONSTRAINT my_c PRIMARY KEY (my_data));"/></COR>")
ncorroot = ET.fromstring("<NCOR><ANSW val = "CREATE TABLE my_table (my_data CHAR, CONSTRAINT my_c NOT NULL (my_data));"/><ANSW val = "CREATE TABLE my_table (my_data CHAR, CONSTRAINT my_c UNIQUE (my_data));"/></NCOR>")

coransvar = []
ncoransvar = []

for child in corroot.findall('.//ANSW'):
    print(child.tag, child.attrib)
    coransvar.append(child.attrib.get('val'))
    
for child in ncorroot.findall('.//ANSW'):
    print(child.tag, child.attrib)   
    ncoransvar.append(child.attrib.get('val'))
    

coransvst = set(coransvar)    
allanswar = coransvar + ncoransvar 
arr = allanswar

answlength = 2
combmas = combinations(arr, answlength)
combarr = []

for i in combmas:
    combarr.append(i)

print(len(combarr))

for j in combarr:
    print(j) # ab ac ad bc bd cd 
    
rndi = randint(0, len(combarr)-1)
print('first ',rndi, ' ',len(combarr),' ', combarr[rndi])
testansvst = set(combarr[rndi])
print(testansvst>=coransvst)
combarr.pop(rndi)
rndi = randint(0, len(combarr)-1)
print('second ',rndi, ' ', len(combarr),' ',combarr[rndi])
testansvst = set(combarr[rndi])
print(testansvst>=coransvst)

testansvar = allanswar
    
ncoransvst = set(ncoransvar)
testansvst = set(testansvar)
print(testansvst>=coransvst)
print(testansvst>=ncoransvst)

"""

if __name__ == '__main__':
    main()