from database_utils import get_connection
import pandas as pd

conn = get_connection()
cursor = conn.cursor()

def insert_records(text_info):
    sql="INSERT INTO users(ID,name,father_name,dob,id_type)VALUES(%s,%s,%s,%s,%s)"
    value=(text_info["ID"],
           text_info["Name"],
           text_info["Father's Name"],
           text_info["DOB"],
           text_info["ID Type"],
           )
    cursor.execute(sql,value)
    conn.commit()

def fetch_data(text_info):
    sql="select * from users where id=%s"
    value=(text_info['ID'],)
    cursor.execute(sql,value)
    results=cursor.fetchall()
    if results:
        df=pd.DataFrame(results,columns=[d[0] for d in cursor.description])
        return df
    else:
        return pd.DataFrame()

def duplicacy(text_info):
    is_duplicate=False
    df=fetch_data(text_info)
    if df.shape[0]>0:
        is_duplicate=True
    return is_duplicate


    