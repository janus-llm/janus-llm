# PSSJXR1 ; COMPILED XREF FOR FILE #55 ; 03/07/23
DIKZK = 2
DIKZ_0 = PS(55,DA,0)
X = DIKZ_0['U',4]
if X != "":
    del PS(55,"ADIA",X[:30],DA)
DIKZ_SAND = PS(55,DA,"SAND")
X = DIKZ_SAND['U',1]
if X != "":
    del PS(55,"ASAND",DA)
X = DIKZ_SAND['U',1]
if X != "":
    del PS(55,"ASAND1",X[:30],DA)
X = DIKZ_0['U',1]
if X != "":
    del PS(55,"B",X[:30],DA)
END
goto PSSJXR2