
import requests
import dao as dao

def callCogitateRaterAPI(sysid, inXml):

    # print("Calling Cogitate Rater...")

    localUrl = "http://localhost/NewRater/api/rater/"
    devUrl = "https://dev.cogitate.us/NewRater/api/rater/"
    
    headers = {
        'Content-Type': 'application/xml'
    }

    # print(inXml)
    
    response = requests.request("POST", localUrl, headers=headers, data = inXml)
    
    # print(response.text)

    for line in (response.text.replace("/>","/>\n").split("\n")):
        if "Total Full Term Premium Result" in line:
            preVal = (line.split("v=")[1].replace("/>","").replace('"',''))            
            updateRecord(sysid, preVal, inXml)


def updateRecord(sysid, premVal, cogitateXML):
    
    updateSql = f"""update dbo.RaterTestingXML
                    set CogitateGASTPrem = {premVal}
                    , CogitateXMLGAST = '{cogitateXML}'
                    where sysid = {sysid}
                    """     
    print(f"{sysid}")
    conn = dao.getSourceConn()
    cursor = conn.cursor()    
    cursor.execute(updateSql)
    cursor.close()
    conn.commit()
    conn.close()