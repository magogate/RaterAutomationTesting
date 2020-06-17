
def transformXML(inputXML):
    taglist = []    
    lineList = inputXML.split("\n")
    policyEndTag = False
    raterStartTag = False
    returnXML = ""

    # print("Inside Read XML Method....")

    #there is a dynamic logic written below, but commented
    program = "GAST"

    # f = open(ihExpessXML, "r")
    for line in lineList:                
        line = line.replace("\n","")         
        # print(line)
        if "ibdoc" in line:
            line = line.replace("ibdoc","Rater")
        if "<m" in line:            
            vValue = ""
            vIndex = line.index('v="')
            iIndex = line.index('i="')
            nIndex = line.index('n="')
            bIndex = line.index('/>')

            if(vIndex < nIndex and nIndex < iIndex):
                vValue = (line[vIndex:nIndex])
            elif(vIndex < iIndex and iIndex < nIndex):
                vValue = (line[vIndex:iIndex])
            elif(vIndex < iIndex):
                vValue = (line[vIndex:iIndex])
            elif(vIndex < nIndex):
                vValue = (line[vIndex:nIndex])
            else:
                vValue = (line[vIndex:bIndex])    

            line = line.replace("<m","<Parameter")
            line = line.replace("n=","code=")            
            line = line.replace(vValue, "")  
            vValue = vValue.replace('"','').replace("v=","").replace(" ","")
            line = line.replace("/>"," >"+ vValue + "</Parameter>")          
            line = line.replace('"</',"</")
        if "desc=" in line:
            line = line.replace('desc=',"code=")
            line = line.replace('<c',"<Parameter")
        if "</c>" in line:
            line = line.replace('</c>',"</Parameter>")
        if "<rate " in line:
            line = "<RateParameter>" + "\n" + '<Parameter code="Policy">'
            # print("Hiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii.................")
            # print(line)
        if "</rate>" in line:
            line = "</Parameter>" + "\n" + "</RateParameter>"

        # if "program_id=" in line:
        #     if('program_id="3"' in line):
        #         program = "GAPA"
        #     elif('program_id="5"' in line):
        #         program = "GAST"
        #     else:
        #         program = "NCPA"

        taglist.append(line)
        # print(line)
        

    signInTag = """<SignIn>
                    <LoginName>admin</LoginName>
                    <Password>admin</Password>
                    <RequestVersion>1.0.0.0</RequestVersion>
                    <RaterVersion>2.0.0.0</RaterVersion>
                    <RulesVersion>2.0.0.0</RulesVersion>
                    <RequesteDateTime>2017-12-17 08:11:30.154</RequesteDateTime>
                    <ReferenceQuoteId>2710</ReferenceQuoteId>
                    <ShowPremium>Y</ShowPremium>
                    <ShowDeductibles>N</ShowDeductibles>
                    <ShowDesc>Y</ShowDesc>
                    <ShowResult>Y</ShowResult>
                    <ShowSteps>N</ShowSteps>
                    <ShowVar>Y</ShowVar>
                    <ShowRateBasis>N</ShowRateBasis>
                    <ShowPremiumSteps>N</ShowPremiumSteps>
                    <ShowDetailLevelTotalPrem>Y</ShowDetailLevelTotalPrem>
                    <RulesState>"""+program+"""</RulesState>
                    <RaterUrl>https://rater.cogitate.us/api/rater</RaterUrl>
                    <ProductCode>PPA</ProductCode>
                    <CoverHolder>IH.AutoRaterMigration</CoverHolder>
                </SignIn>"""    

    
    for i in range(len(taglist)):        
        if('code="EffectiveDt"' in taglist[i]):
            returnXML = returnXML + taglist[i] + "\n" + taglist[i].replace("EffectiveDt","EffectiveDate") + "\n"

        if("<Rater>" in taglist[i]):                        
            returnXML = returnXML + taglist[i]+"\n"            
            returnXML = returnXML + signInTag+"\n"    
            raterStartTag = True      
        elif("</IHRaterRq>" in taglist[i]):
            returnXML = returnXML + "\n"                                
        elif(raterStartTag and 'i="0" code="Policy"' in taglist[i]):
            policyEndTag = True            
            returnXML = returnXML + "\n"
        elif(raterStartTag and policyEndTag and len(taglist[i].strip()) < 13 and "</Parameter>" in taglist[i]):
            policyEndTag = False            
            returnXML = returnXML + "\n"
        elif(raterStartTag and ">" in taglist[i]):            
            returnXML = returnXML + taglist[i].replace("/>","></Parameter>")+"\n"        
        elif(raterStartTag):            
            returnXML = returnXML + taglist[i]+"\n"	        
                  
    # print(returnXML)
    return returnXML
