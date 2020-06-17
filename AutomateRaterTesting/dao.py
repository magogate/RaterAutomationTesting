import pyodbc

def getSourceConn():    
    DSN = ""
    uid = ""
    pwd = ""
    db = ""

    connString = 'DRIVER={SQL Server};SERVER='+DSN+';UID='+uid+';PWD='+pwd+';DATABASE='+db
    
    conn = pyodbc.connect(connString)

    return conn
