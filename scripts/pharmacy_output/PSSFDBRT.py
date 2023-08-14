def GROUTE(PSSIEN, PSSOUT):
    BASE = "PSSFDBRT GROUTE"
    GCNSEQ = DRUGGCN(PSSIEN)
    if GCNSEQ == 0:
        PSSOUT[0] = "-1^GCN sequence number is not defined."
        return
    PSSXML = BLDXML(GCNSEQ)
RETRY:
    POST(PSSXML, PSSOUT)
    if not PSSRETR1 and PSSOUT[0].split('^')[0] == "-1":
        del PSSOUT
        PSSRETR1 = 1
        time.sleep(3)
        goto RETRY


def DRUGGCN(DRGIEN):
    GCN = 0
    VAPROD = DRGIEN['ND'][2]
    if VAPROD:
        GCN = int(DRGIEN['ND'][2][1]['1'])
    return GCN


def BLDXML(GCNSEQ):
    PSSXML = ""
    GETHEAD(PSSXML)
    GETREQ(PSSXML)
    DRUGTAG = "<drug "
    ENDTAG = "/>"
    PSSXML = PSSXML + DRUGTAG + ATRIBUTE('gcnSeqNo', GCNSEQ) + ENDTAG
    ENDREQ(PSSXML)
    return PSSXML


def POST(XML, PSSOUT):
    PSS = {}
    PSS['server'] = "PEPS"
    PSS['webserviceName'] = "DRUG_INFO"
    PSS['path'] = "druginfo"
    PSS['parameterName'] = "xmlRequest"
    PSS['parameterValue'] = XML

    PSS['restObject'] = GETREST(PSS['webserviceName'], PSS['server'])
    if 'EXCEPTION' in PSS:
        PSSOUT[0] = "-1^" + PSS['EXCEPTION']
        del PSS['EXCEPTION']
        return PSSOUT

    PSS['restObject'].InsertFormData(PSS['parameterName'], PSS['parameterValue'])
    if 'EXCEPTION' in PSS:
        PSSOUT[0] = "-1^" + PSS['EXCEPTION']
        del PSS['EXCEPTION']
        return PSSOUT

    PSS['postResult'] = POST(PSS['restObject'], PSS['path'], PSS['ERR'])
    if 'EXCEPTION' in PSS:
        PSSOUT[0] = "-1^" + PSS['EXCEPTION']
        del PSS['EXCEPTION']
        return PSSOUT

    if not PSS['postResult']:
        PSSOUT[0] = "-1^Unable to make http request."
        PSS['result'] = 0
        return

    PSS['result'] = gov.va.med.pre.ws.XMLHandler.getHandleToXmlDoc(PSS['restObject'].HttpResponse.Data, DOCHAND)
    PSSOUT[0] = 0
    PARSXML(DOCHAND, PSSOUT)


def PARSXML(DOCHAND, PSSOUT):
    PSS['rootName'] = NAME(DOCHAND, 1)
    PSS['child'] = 0
    while PSS['child'] != 0:
        PSS['child'] = CHILD(DOCHAND, 1, PSS['child'])
        if PSS['child'] != 0:
            PSS['childName'] = NAME(DOCHAND, PSS['child'])
            if PSS['childName'] == "drug":
                PARSDRUG(DOCHAND, PSS['child'], PSSOUT)


def PARSDRUG(DOCHAND, NODE, PSSOUT):
    PSS['child'] = 0
    while PSS['child'] != 0:
        PSS['child'] = CHILD(DOCHAND, NODE, PSS['child'])
        if PSS['child'] != 0:
            PSS['childName'] = NAME(DOCHAND, PSS['child'])
            if PSS['childName'] == "routes":
                PARSRTES(DOCHAND, PSS['child'], PSSOUT)


def PARSRTES(DOCHAND, NODE, PSSOUT):
    PSS['child'] = 0
    while PSS['child'] != 0:
        PSS['child'] = CHILD(DOCHAND, NODE, PSS['child'])
        if PSS['child'] != 0:
            PSS['childName'] = NAME(DOCHAND, PSS['child'])
            if PSS['childName'] == "route":
                PARSRTE(DOCHAND, PSS['child'], PSSOUT)


def PARSRTE(DOCHAND, NODE, PSSOUT):
    PSS['child'] = 0
    while PSS['child'] != 0:
        PSS['child'] = CHILD(DOCHAND, NODE, PSS['child'])
        if PSS['child'] != 0:
            PSS['childName'] = NAME(DOCHAND, PSS['child'])
            if PSS['childName'] == "name":
                PSS['childText'] = GETTEXT(DOCHAND, PSS['child'])
                if PSS['childText'] != "":
                    PSSOUT[PSS['childText']] = ""
                    PSSOUT[0] = 1


def GETHEAD(PSSXML):
    PSSXML = PSSXML + XMLHDR()


def GETREQ(PSSXML):
    TAG = "<drugInfoRequest "
    SUBXML = TAG
    SUBXML += ATRIBUTE('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
    SUBXML += ATRIBUTE('xsi:schemaLocation',
                      "gov/va/med/pharmacy/peps/external/common/preencapsulation/vo/drug/info/request drugInfoSchemaInput.xsd")
    SUBXML += ATRIBUTE('xmlns', "gov/va/med/pharmacy/peps/external/common/preencapsulation/vo/drug/info/request")
    PSSXML = PSSXML + SUBXML + ">"


def ENDREQ(PSSXML):
    PSSXML = PSSXML + "</drugInfoRequest>"


def XMLHDR():
    return '<?xml version="1.0" encoding="utf-8" ?>'