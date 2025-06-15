import mysql.connector
def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Diya@0811",  
        database="ekyc"         
    )
    
