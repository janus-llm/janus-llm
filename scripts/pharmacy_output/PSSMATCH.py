def PSSMATCH():
    PRI()
    
def PRI():
    CPK()
    if PSSITEQT:
        CPK1()
    else:
        print("These reports are based on creating your Orderable Item file by Primary Name,")
        print("then by VA Generic Name.")
        VAONLY = 0
        DIR()
        
def VA():
    CPK()
    if PSSITEQT:
        CPK1()
    else:
        print("These reports are based on creating your Orderable Item File by VA Generic Name.")
        VAONLY = 1
        DIR()
        
def DIR():
    DIR = {}
    DIR['0'] = "S^M:Drugs that will match;C:Drugs that can't be matched"
    DIR['A',1] = "Enter M for Orderable Items that will auto-create,"
    DIR['A',2] = "which includes Dispense Drugs, Additives, and Solutions that will match."
    DIR['A',3] = "Enter C for the report of Dispense Drugs that can't auto-match."
    DIR['A',4] = ""
    DIR['A'] = "Enter M or C"
    Y = input()
    if Y in ["^", "^^"] or any(x in Y for x in ["^", "^^"]):
        END()
    PSMATCH = 1 if Y == "M" else 0
    print(chr(7))
    print("**WARNING** THIS REPORT MAY BE VERY LONG!")
    RMES_PSSPOIM1()
    QUE()
    
def QUE():
    print()
    ZTRTN = "BEG^PSSMATCH"
    ZTDESC = "Orderable Item Reports"
    ZTSAVE = {"PSMATCH": "", "VAONLY": ""}
    ZTLOAD()
    END()
    
def END():
    del ^TMP("PSSD",$J)
    del ^TMP("PSS",$J)
    del ^TMP("PSSADD",$J)
    del ^TMP("PSSOL",$J)
    del AAA
    del BBB
    del DIR
    del DOSEFORM
    del EEE
    del GFLAG
    del GGG
    del LINE
    del LLL
    del PAGE
    del PSMATCH
    del PSODD
    del PSOIV
    del PSOLU
    del REASON
    del ANM
    del AVL
    del SSS
    del TTT
    del VAONLY
    del VARONE
    del VARTWO
    del ZFLAG
    del ZZZ
    ^%ZISC()
    if ZTQUEUED:
        ZTREQ = "@"
    return
    
def BEG():
    SSITE = $O(^PS(59.7,0))
    SITEADD = $P($G(^PS(59.7,+SSITE,31)),"^",2) if $P($G(^PS(59.7,+SSITE,31)),"^",2) != "" else "IV"
    del SSITE
    if PSMATCH:
        CANT()
    ^PSSSPD()
    if VAONLY:
        del ^TMP("PSSD",$J)
        del ^TMP("PSS",$J)
        del ^TMP("PSSADD",$J,"ZZZZ")
        del ^TMP("PSSOL",$J,"ZZZZ")
        PASS()
    del ^TMP("PSSD",$J,"ZZZZ")
    del ^TMP("PSSADD",$J,"ZZZZ")
    del ^TMP("PSSOL",$J,"ZZZZ")
    PASS()
    
def PASS():
    if VAONLY:
        BEG_PSSPOIM()
    else:
        BEG_PSSPOIC()
    del LINE
    LINE = "-" * 79
    PAGE = 1
    ZFLAG = 0
    ADD()
    SOL()
    PAGE = 1
    HEAD()
    ZZZ = ""
    while ZZZ:
        if ($Y + 6) > IOSTL:
            ZFLAG = 1
        if ZFLAG:
            HEAD()
        else:
            print(LINE)
            print(ZZZ)
        ZFLAG = 0
        GGG = ""
        while GGG:
            if ($Y + 4) > IOSTL:
                GFLAG = 1
            if GFLAG:
                HEAD()
            else:
                print(GGG, "  ", ^(GGG) if ^TMP("PSSD",$J,ZZZ,GGG) != "" else "")
    print(chr(12))
    END()
    
def HEAD():
    print(chr(12))
    if VAONLY:
        print("ORDERABLE ITEMS - MATCHES BY VA GENERIC NAME ONLY             PAGE ", PAGE)
    else:
        print("ORDERABLE ITEMS - MATCHES BY PRIMARY NAME THEN VA GENERIC NAME    PAGE ", PAGE)
        print("(PRIMARY DRUG) IN PARENTHESIS")
    print(LINE)
    PAGE += 1
    if ZFLAG:
        print()
        print(ZZZ)
    if GFLAG:
        print()
        print(ZZZ, " (cont.)")
    GFLAG = 0
    return
    
def ADD():
    ADHEAD()
    AAA = ""
    while AAA:
        if ($Y + 5) > IOSTL:
            ADHEAD()
        print(AAA, "   ", SITEADD)
        print(PSODD, "  ", DOSEFORM)
        print(LINE)
    print(chr(12))
    return

def ADHEAD():
    print(chr(12))
    print("ORDERABLE ITEM (ADDITIVE)    IV FLAG", " " * 69, "PAGE ", PAGE)
    print("   DISPENSE DRUG   DOSE FORM")
    print(LINE)
    PAGE += 1
    return

def SOL():
    PAGE = 1
    GFLAG = 0
    ZFLAG = 0
    SOLHEAD()
    FFF = ""
    while FFF:
        if ($Y + 6) > IOSTL:
            ZFLAG = 1
        if ZFLAG:
            SOLHEAD()
        else:
            print(LINE)
            print(FFF, "  ", ZZZ)
        ZFLAG = 0
        WWW = ""
        while WWW:
            if ($Y + 4) > IOSTL:
                GFLAG = 1
            if GFLAG:
                SOLHEAD()
            else:
                print(FFF, "   ", $P($G(^PS(52.7,+^TMP("PSSOL",$J,FFF,ZZZ,WWW),0)),"^",3))
    print(chr(12))
    return

def SOLHEAD():
    print(chr(12))
    print("ORDERABLE ITEM (SOLUTION)   DOSE FORM", " " * 69, "PAGE ", PAGE)
    print("   SOLUTION       VOLUME")
    print(LINE)
    PAGE += 1
    if ZFLAG:
        print()
        print(FFF, "  ", ZZZ)
    if GFLAG:
        print()
        print(FFF, "  ", ZZZ, " (cont.)")
    GFLAG = 0
    return

def CANT():
    ^PSSSPD()
    if VAONLY:
        del ^TMP("PSSD",$J)
        del ^TMP("PSS",$J)
    SKIP()
    if VAONLY:
        CANT_PSSPOIM()
    else:
        CANT_PSSPOIC()
    del LINE
    LINE = "-" * 79
    PAGE = 1
    ZFLAG = 0
    ADDCANT()
    SOLCANT()
    PAGE = 1
    NOHEAD()
    EEE = ""
    while EEE:
        if ($Y + 5) > IOSTL:
            NOHEAD()
        print(EEE, " " * 43, REASON)
        if ($O(^(EEE,0))):
            TTT = 0
            while TTT:
                if ($Y + 5) > IOSTL:
                    ZFLAG = 1
                if ($Y + 5) > IOSTL:
                    NOHEAD()
                print(" " * 3, ^(TTT))
                TTT += 1
    print(chr(12))
    END()
    
def NOHEAD():
    print(chr(12))
    print("ORDERABLE ITEMS - VA GENERIC NAME ONLY, CAN'T MATCH" if VAONLY else "ORDERABLE ITEMS - PRIMARY NAME THEN VA GENERIC NAME, CAN'T MATCH", " " * 69, "PAGE ", PAGE)
    print(LINE)
    PAGE += 1
    if ZFLAG:
        print()
        print(EEE, " " * 43, REASON)
        ZFLAG = 0
    return

def ADDCANT():
    HEADA()
    BBB = ""
    while BBB:
        if ($Y + 5) > IOSTL:
            HEADA()
        print(BBB, " " * 43, REASON)
        ANM = $O(^PSDRUG("B",BBB,0))
        if ANM:
            ANM = $P($G(^PS(52.6,"AC",ANM,0)),"^")
            print(ANM, " " * 43, REASON)
    print(chr(12))
    return

def HEADA():
    print(chr(12))
    print("ORDERABLE ITEMS - ADDITIVES THAT CANNOT AUTO MATCH", " " * 69, "PAGE ", PAGE)
    print(LINE)
    PAGE += 1
    return

def SOLCANT():
    PAGE = 1
    HEADS()
    LLL = ""
    while LLL:
        if ($Y + 6) > IOSTL:
            ZFLAG = 1
        if ZFLAG:
            HEADS()
        else:
            print(LINE)
            print(ANM, " " * 43, AVL)
            print(" " * 5, REASON)
    print(chr(12))
    return

def HEADS():
    print(chr(12))
    print("ORDERABLE ITEMS - SOLUTIONS THAT CANNOT AUTO MATCH", " " * 69, "PAGE ", PAGE)
    print(LINE)
    PAGE += 1
    return

def CPK():
    PSSITE = +$O(^PS(59.7,0))
    if +$P($G(^PS(59.7,PSSITE,80)),"^",2) > 1:
        print("The Orderable Item auto-create has already run to completion!")
        PSSITEQT = 1
        DIR()
    return

def CPK1():
    del PSSITEQT
    return