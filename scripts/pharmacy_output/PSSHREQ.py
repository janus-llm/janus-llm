def PSSHREQ():
    #WOIFO/AV,TS - Creates PSSXML to send to PEPS using input global ;09/20/07
    #1.0;PHARMACY DATA MANAGEMENT;**136,163**;9/30/97;Build 8
    #
    # @authors - Alex Vazquez, Tim Sabat, Steve Gordon
    # @date    - September 19, 2007
    # @version - 1.0
    return

def BLDPREQ(PSSBASE):
    # @DRIVER
    #
    # @DESC Builds the PEPSRequest PSSXML element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An xml string representing an entire order check.
    PSS = {}
    PSS["PSSXMLHeader"] = XMLHDR()
    PSS["xmlns"] = ATRIBUTE("xmlns","gov/va/med/pharmacy/peps/external/common/preencapsulation/vo/drug/check/request")
    PSS["xsi"] = ATRIBUTE("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
    
    PSSXML = PSS["PSSXMLHeader"]
    PSSXML += "<PEPSRequest"
    PSSXML += " " + PSS["xmlns"]
    PSSXML += " " + PSS["xsi"]
    PSSXML += " >"
    PSSXML += HEADER(PSSBASE)
    if not PSSBASE["IN"]["PING"]:
        PSSXML += BODY(PSSBASE)
    PSSXML += "</PEPSRequest>"
    
    return PSSXML

def HEADER(PSSBASE):
    # @DESC Builds the Header PSSXML element. A header is the section of the PSSXML
    # that includes time, server, and user.  This item holds no business logic, it
    # only records debugging information.
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS A the PSSXML string representing the header element.
    PSSXML = ""
    PSS = {}
    
    if "PING" in PSSBASE["IN"]:
        PSS["pingOnly"] = ATRIBUTE("pingOnly","true")
    
    PSSXML = "<Header " + PSS.get("pingOnly","") + ">"
    PSSXML += HDRTIME()
    PSSXML += HDRSERVR()
    PSSXML += HDRMUSER()
    PSSXML += "</Header>"
    
    # Return composed header
    return PSSXML

def HDRTIME():
    # @DESC Builds the Time PSSXML element which resides in the header
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An xml string containing the time element.
    PSS = {}
    PSS["value"] = ATRIBUTE("value",DT)
    
    PSSXML = "<Time"
    PSSXML += " " + PSS["value"]
    PSSXML += " />"
    
    return PSSXML

def HDRSERVR():
    # @DESC Builds the MServer PSSXML element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing the server element.
    PSS = {}
    PSS["IP"] = ATRIBUTE("ip",IO["IP"])
    PSS["nameSpace"] = ATRIBUTE("namespace","")
    PSS["serverName"] = ATRIBUTE("serverName",XMV["NETNAME"].split("@")[1])
    PSS["stationNumber"] = ATRIBUTE("stationNumber",SITE("3"))
    PSS["UCI"] = ATRIBUTE("uci","")
    
    PSSXML = "<MServer"
    PSSXML += " " + PSS["IP"]
    PSSXML += " " + PSS["nameSpace"]
    PSSXML += " " + PSS["serverName"]
    PSSXML += " " + PSS["stationNumber"]
    PSSXML += " " + PSS["UCI"]
    PSSXML += " />"
    
    return PSSXML

def HDRMUSER():
    # @DESC Builds the user element of the PSSXML
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing the M user.
    PSS = {}
    PSS["duz"] = ATRIBUTE("duz",DUZ)
    PSS["jobNumber"] = ATRIBUTE("jobNumber",$J)
    PSS["userName"] = ATRIBUTE("userName",GET1("200",DUZ_",",".01"))
    
    PSSXML = "<MUser"
    PSSXML += " " + PSS["duz"]
    PSSXML += " " + PSS["jobNumber"]
    PSSXML += " " + PSS["userName"]
    PSSXML += " />"
    
    return PSSXML

def BODY(PSSBASE):
    # @DESC Builds the Body PSSXML element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing the body element.
    PSSXML = "<Body>"
    PSSXML += DRGCHEK(PSSBASE)
    PSSXML += "</Body>"
    
    return PSSXML

def DRGCHEK(PSSBASE):
    # @DESC Builds the DrugCheck PSSXML element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS an PSSXML string representing the drugCheck element
    PSSXML = "<drugCheck>"
    PSSXML += CHECKS(PSSBASE)
    PSSXML += DRUGPROS(PSSBASE)
    PSSXML += MEDPROF(PSSBASE)
    PSSXML += "</drugCheck>"
    
    # Return the full drugCheck element
    return PSSXML

def CHECKS(PSSBASE):
    # @DESC Builds the checks PSSXML element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing the checks element.
    PSS = {}
    
    # If data in global, set prospective only to false
    if "PROFILEVPROFILE" in PSSBASE["IN"]:
        PSS["prospectiveOnly"] = ATRIBUTE("prospectiveOnly","false")
    # If no data in global, set prospective only to true
    if "PROFILEVPROFILE" not in PSSBASE["IN"]:
        PSS["prospectiveOnly"] = ATRIBUTE("prospectiveOnly","true")
    
    # OPTIONAL. TBA Right now set to false, will be used in future
    PSS["useCustomTables"] = ATRIBUTE("useCustomTables","true")
    
    PSSXML = "<checks"
    PSSXML += " " + PSS.get("prospectiveOnly","")
    PSSXML += " " + PSS.get("useCustomTables","")
    PSSXML += " >"
    PSSXML += CHEKDOSE(PSSBASE)
    PSSXML += CHEKDRUG(PSSBASE)
    PSSXML += CHEKTHER(PSSBASE)
    PSSXML += "</checks>"
    
    # Return the full drugCheck element
    return PSSXML

def CHEKDOSE(PSSBASE):
    # @DESC Sets the drugDoseCheck element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing the doseCheck element
    PSSXML = ""
    
    if "DOSE" in PSSBASE["IN"]:
        PSSXML = "<drugDoseCheck>"
        # Get the demographics PSSXML section
        PSSXML += DEMOGRAF(PSSBASE)
        PSSXML += "</drugDoseCheck>"
    
    return PSSXML

def DEMOGRAF(PSSBASE):
    # @DESC Builds the demographic element
    #
    # @PSSBASE Input global base
    #
    # @RETURNS An PSSXML string representation of the demographics element
    PSSXML = ""
    PSS = {}
    
    PSS["bodySurfaceAreaInSqM"] = ATRIBUTE("bodySurfaceAreaInSqM",PSSBASE["IN"]["DOSE"]["BSA"])
    
    PSS["weightInKG"] = ATRIBUTE("weightInKG",PSSBASE["IN"]["DOSE"]["WT"])
    
    PSS["ageInDays"] = ATRIBUTE("ageInDays",PSSBASE["IN"]["DOSE"]["AGE"])
    
    PSSXML = "<demographics " + PSS["bodySurfaceAreaInSqM"] + " " + PSS["weightInKG"] + " " + PSS["ageInDays"] + "/>"
    
    return PSSXML

def CHEKDRUG(PSSBASE):
    # @DESC Sets the drugDrugCheck element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML String representing drugDoseCheck element
    PSSXML = ""
    
    # If drug drug global set, add drug drug check
    if "DRUGDRUG" in PSSBASE["IN"]:
        PSSXML = "<drugDrugCheck />"
    
    return PSSXML

def CHEKTHER(PSSBASE):
    # @DESC Sets the drugTherapyCheck element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing the drugTherapyCheck element
    PSSXML = ""
    
    # If drug therapy set, add therapy check
    if "THERAPY" in PSSBASE["IN"]:
        PSSXML = "<drugTherapyCheck />"
    
    return PSSXML

def MEDPROF(PSSBASE):
    # @DESC Builds a medicationProfile element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS PSSXML string element of the medicationProfile
    PSSXML = "<medicationProfile>"
    PSSXML += DRUGPROF(PSSBASE)
    PSSXML += "</medicationProfile>"
    
    return PSSXML

def DRUGPROS(PSSBASE):
    # @DESC Builds prospectiveDrugs element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing prospectiveDrugs
    PSSXML = ""
    PSSDRUGS = {}
    
    # Read drug info from input global, store in PSSDRUGS hash
    READRUGS(PSSBASE,"PROSPECTIVE",PSSDRUGS)
    if not PSSDRUGS["DRUG"]:
        PSSXML = ""
        return PSSXML
    # Write the drugs as PSSXML
    PSSXML = "<prospectiveDrugs>" + RITEDRGS(PSSDRUGS) + "</prospectiveDrugs>"
    
    return PSSXML

def DRUGPROF(PSSBASE):
    # @DESC Builds a prospective drug element
    #
    # @PSSBASE Base of input global
    #
    # @RETURNS An PSSXML string representing profile drugs
    PSSXML = ""
    PSSDRUGS = {}
    
    # Read from the input global and put in PSSDRUGS hash
    READRUGS(PSSBASE,"PROFILE",PSSDRUGS)
    # Write the profile drugs as PSSXML
    PSSXML = RITEDRGS(PSSDRUGS)
    
    return PSSXML

def READRUGS(PSSBASE,DRUGTYPE,PSSDRUGS):
    # @DESC Builds either a prospective or a profile drug element.
    # Note the "DRUGTYPE" parameter.  This param allows for re-use, so either
    # a profile or a prospective drug can be created.
    #
    # @PSSBASE Base of input global
    # @DRUGTYPE A drug type, either Prospective or Profile
    # @PSSDRUGS ByRef, variable to store drug attributes in
    #
    # @RETURNS Nothing, values stored in drugs variable
    PSS = {}
    
    PSS["ien"] = ""
    PSS["count"] = 0
    
    # Loop through the unique order numbers
    PSS["orderNumber"] = ""
    while PSS["orderNumber"]:
        PSS["count"] += 1
        PSS["value"] = PSSBASE["IN"][DRUGTYPE][PSS["orderNumber"]]
        # Set the drug order number
        PSSDRUGS["DRUG"][PSS["count"]]["orderNumber"] = PSS["orderNumber"]
        # Set the drug gcn sequence number
        PSSDRUGS["DRUG"][PSS["count"]]["gcn"] = int(PSS["value"].split("^")[0])
        # Set the drug vuid
        PSSDRUGS["DRUG"][PSS["count"]]["vuid"] = int(PSS["value"].split("^")[1])
        # Set the drug ien
        PSSDRUGS["DRUG"][PSS["count"]]["ien"] = int(PSS["value"].split("^")[2])
        # Set the drug name
        PSSDRUGS["DRUG"][PSS["count"]]["drugName"] = PSS["value"].split("^")[3]
        # Set the cprs order number
        PSSDRUGS["DRUG"][PSS["count"]]["cprsOrderNumber"] = PSS["value"].split("^")[4]
        # Set the package
        PSSDRUGS["DRUG"][PSS["count"]]["package"] = PSS["value"].split("^")[5]
        
        # Get the possible dose information for the drug
        READDOSE(PSSBASE,PSSDRUGS,PSS["count"],PSS["orderNumber"])
        # Increment order number
        PSS["orderNumber"] += 1
    
    return

def RITEDRGS(PSSDRUGS):
    # @DESC Loop through the drugs and return PSSXML
    #
    # @PSSDRUGS Array containing the list of drugs
    #
    # @RETURNS PSSXML representing the drugs in array
    PSSCOUNT = ""
    PSSXML = ""
    
    for PSSCOUNT in PSSDRUGS["DRUG"]:
        # loop through drugs and append to PSSXML
        PSSXML += RITEDRUG(PSSDRUGS,PSSCOUNT)
    
    return PSSXML

def RITEDRUG(PSSDRUGS,PSSCOUNT):
    # @DESC Builds a single drug xml element
    #
    # @PSSDRUGS A handle to the drug object
    # @PSSCOUNT The counter where the information should be taken from
    #
    # @RETURNS An PSSXML string representing a single drug
    PSS = {}
    PSSXML = ""
    
    if "drugName" in PSSDRUGS["DRUG"][PSSCOUNT]:
        PSS["drugName"] = ATRIBUTE("drugName",PSSDRUGS["DRUG"][PSSCOUNT]["drugName"])
    
    PSS["gcnSeqNo"] = ATRIBUTE("gcnSeqNo",PSSDRUGS["DRUG"][PSSCOUNT]["gcn"])
    
    PSS["ien"] = ATRIBUTE("ien",PSSDRUGS["DRUG"][PSSCOUNT]["ien"])
    
    # Concatenate the orderNumber, cprs order number, and package
    # ex. orderNumber|cprsOrderNumber|package
    PSSORDR = PSSDRUGS["DRUG"][PSSCOUNT]["orderNumber"] + "|" + PSSDRUGS["DRUG"][PSSCOUNT].get("cprsOrderNumber","") + "|" + PSSDRUGS["DRUG"][PSSCOUNT].get("package","")
    
    PSS["orderNumber"] = ATRIBUTE("orderNumber",PSSORDR)
    
    # vuid is optional
    if "vuid" in PSSDRUGS["DRUG"][PSSCOUNT]:
        PSS["vuid"] = ATRIBUTE("vuid",PSSDRUGS["DRUG"][PSSCOUNT]["vuid"])
    
    PSSXML = "<drug " + PSS["drugName"] + " " + PSS["gcnSeqNo"] + " " + PSS["ien"] + " " + PSS["orderNumber"] + " " + PSS["vuid"] + " >"
    PSSXML += RITEDOSE(PSSDRUGS,PSSCOUNT)
    PSSXML += "</drug>"
    
    return PSSXML

def READDOSE(PSSBASE,PSSHASH,PSSCOUNT,ORDRNM):
    # @DESC Sets the individual drugDose elements, including all dosing amounts,
    # frequency, etc for an individual drug.
    #
    # @DOSE A handle to the drug dose you want to turn into PSSXML
    #
    # @RETURNS Nothing, values stored in hash
    PSS = {}
    
    # If no drug dose information exist for the drug quit
    if "DOSE" not in PSSBASE["IN"][ORDRNM]:
        PSSHASH["DRUG"][PSSCOUNT]["hasDose"] = 0
        return
    PSSHASH["DRUG"][PSSCOUNT]["hasDose"] = 1
    
    PSS["value"] = PSSBASE["IN"][ORDRNM]
    # If specific get values (doseAmount,doseUnit,doseRate,frequency,
    # duration,durationRate,medicalRoute,doseType)
    PSSHASH["DRUG"][PSSCOUNT]["doseAmount"] = PSS["value"].split("^")[4]
    PSSHASH["DRUG"][PSSCOUNT]["doseUnit"] = PSS["value"].split("^")[5]
    PSSHASH["DRUG"][PSSCOUNT]["doseRate"] = PSS["value"].split("^")[6]
    PSSHASH["DRUG"][PSSCOUNT]["frequency"] = PSS["value"].split("^")[7]
    PSSHASH["DRUG"][PSSCOUNT]["duration"] = PSS["value"].split("^")[8]
    PSSHASH["DRUG"][PSSCOUNT]["durationRate"] = PSS["value"].split("^")[9]
    PSSHASH["DRUG"][PSSCOUNT]["route"] = PSS["value"].split("^")[10]
    PSSHASH["DRUG"][PSSCOUNT]["doseType"] = PSS["value"].split("^")[11]
    
    return

def RITEDOSE(PSSHASH,I):
    # @DESC Writes the doseInformation PSSXML element
    #
    # @PSSHASH Hash value with variables used to create element
    #
    # @RETURNS A valid drugDose XML element
    PSSXML = ""
    
    if not PSSHASH["DRUG"][I]["hasDose"]:
        return PSSXML
    
    # Create dose information
    PSSXML = "<doseInformation>"
    PSSXML += "<doseType>" + PSSHASH["DRUG"][I]["doseType"] + "</doseType>"
    PSSXML += "<doseAmount>" + PSSHASH["DRUG"][I]["doseAmount"] + "</doseAmount>"
    PSSXML += "<doseUnit>" + PSSHASH["DRUG"][I]["doseUnit"] + "</doseUnit>"
    PSSXML += "<doseRate>" + PSSHASH["DRUG"][I]["doseRate"] + "</doseRate>"
    if len(PSSHASH["DRUG"][I]["frequency"]) > 0:
        PSSXML += "<frequency>" + PSSHASH["DRUG"][I]["frequency"] + "</frequency>"
    if len(PSSHASH["DRUG"][I]["duration"]) > 0:
        PSSXML += "<duration>" + PSSHASH["DRUG"][I]["duration"] + "</duration>"
    if len(PSSHASH["DRUG"][I]["durationRate"]) > 0:
        PSSXML += "<durationRate>" + PSSHASH["DRUG"][I]["durationRate"] + "</durationRate>"
    PSSXML += "<route>" + PSSHASH["DRUG"][I]["route"] + "</route>"
    
    # Close off dose information
    PSSXML += "</doseInformation>"
    
    return PSSXML