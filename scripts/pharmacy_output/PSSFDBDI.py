def PSSFDBDI():
    """
    BIR/LE - Sends XML Request to PEPS via HWSC for Dose Information
    01/23/12
    """
    pass

def EN(PSSGCN, PSSOUT):
    """
    Get dosing information based on GCNSEQNO
    input: PSSGCN - GCNSEQNO from file 50.68
    output: builds TMP file for dosing information
            e.g. ^TMP($J,"PSSFDBDI"
            PSSOUT(0) = 1 for successful
                      -1^error message (when an error occurs: example "-1^ERROR #6059: Unable to open TCP/IP socket to server nn.n.nnn.nn:nnnn"
    """
    pass

def BLDXML(GCNSEQ):
    """
    Build and return the XML request with drug information for given GCN sequence number
    input: GCNSEQ - drug IEN from drug file (#50)
    output: returns the XML request for given GCN sequence number
            Example: where 22211 is the GCN Sequence number passed by reference at line tag EN above.
                     PSSXML="<?xml version=""1.0"" encoding=""utf-8"" ?><dosingInfoRequest  xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" 
                              xsi:schemaLocation=""gov/va/med/pharmacy/peps/external/common/preencapsulation/vo/dosing/info/request dosingInfoSchemaInput.xsd"" 
                              xmlns=""gov/va/med/pharmacy/peps/external/common/preencapsulation/vo/dosing/info/request"">
                              <dosingInfo gcnSeqNo=""22211"" fdbdx=""999"" />
                              </dosingInfoRequest>"
    """
    pass

def POST(XML, PSSGCN, PSSOUT):
    """
    Post the XML request to PEPS server and return the routes
    input: XML request
    output: PSSOUT - array containing the list of route names for the given drug.
    """
    pass

def PARSXML(DOCHAND, PSSGCN, PSSOUT):
    """
    Read result
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def PARSDOIN(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Parse dosingInfo element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def READDOIN(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Read dosingInfo attributes
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def PARSDORG(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Parse doseRange element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def READDORG(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Read doseRange attributes
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def PARSDORC(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Parse doseRange child element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def PARSDOMM(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Parse minMaxResults element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def PARSDONN(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Parse neonatalDoseRanges element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def READDODN(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Read dispensableDrugName element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def READDODD(DOCHAND, PSSGCN, NODE, PSSOUT):
    """
    Read dispensableDrugDescription element
    DOCHAND = Handle to XML Document
    PSSGCN = GCN passed in to API
    NODE = Document node
    PSSOUT = output array
    """
    pass

def SETXREFS(PSSOUT2):
    """
    Set "A","B","C", zero node cross references & values
    """
    pass

def GETFILE(PSSDR, PSSMM):
    """
    Get file structure for the temp file for each data field imported from FDB
    """
    pass