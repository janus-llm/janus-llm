def PSS187PO():
    """
    BIR/MA - Post install reindexing xrefs
    Dec 06, 2021@08:18:18
    """
    return

def POST():
    """
    Post installation process
    """
    MES_XPDUTL("===================================================================")
    MES_XPDUTL("Start reindexing INDICATIONS FOR USE and OTHER LANGUAGE INDICATIONS")
    MES_XPDUTL("of PHARMACY ORDERABLE ITEM file (#50.7).")
    EN()
    BMES_XPDUTL("Completed Reindexing ..............................................")
    MES_XPDUTL("===================================================================")

def EN():
    """
    Reindexing process
    """
    DIK, DA = None, None
    DA1 = 0
    while True:
        DA1 = $O(^PS(50.7,DA1))
        if not DA1:
            break
        DIK = f"^PS(50.7,{DA1},'IND')"
        DIK1 = ".01"
        ENALL2(DIK, DIK1)
        DA = ""
        ENALL(DIK, DA)
        DA = ""

    DA1 = 0
    while True:
        DA1 = $O(^PS(50.7,DA1))
        if not DA1:
            break
        DIK = f"^PS(50.7,{DA1},'INDO')"
        DIK1 = ".01"
        ENALL2(DIK, DIK1)
        DA = ""
        ENALL(DIK, DA)

def ENALL(DIK, DA):
    """
    Reindexing process for all entries
    """
    return

def ENALL2(DIK, DIK1):
    """
    Reindexing process for specific entry
    """
    return

def MES_XPDUTL(message):
    """
    Display message using XPDUTL
    """
    return

def BMES_XPDUTL(message):
    """
    Display bold message using XPDUTL
    """
    return