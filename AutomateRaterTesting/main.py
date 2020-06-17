import dao as dao
import convertXML
import callCogitateRaterAPI as callApi

def fetchReqXML():
    # change createdOn to updatedOn
    sqlQuery = """select sysid, QuoteRqData
                    from dbo.RaterTestingXML
                    Where CogitateGASTPrem is null
                    and (ProgramId1 = 5 or ProgramId2 = 5 or ProgramId3 = 5 or ProgramId4 = 5)
                    """
    conn = dao.getSourceConn()
    cursor = conn.cursor()    
    cursor.execute(sqlQuery)

    for row in cursor:
        try:
            sysid = (row[0])
            reqXML = (row[1].replace('<?xml version="1.0" encoding="utf-16"?>',''))
            # print(reqXML)
            cogitateXml = convertXML.transformXML(reqXML)
            # print(cogitateXml)
            callApi.callCogitateRaterAPI(sysid, cogitateXml)
        except  Exception:
            print("Inside exception block of main.py")

    cursor.close()
    conn.close()


fetchReqXML()