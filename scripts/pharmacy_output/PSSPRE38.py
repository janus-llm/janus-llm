# BIR/RTR-Pre init routine ;04/03/00
# 1.0;PHARMACY DATA MANAGEMENT;**38**;9/30/97

import datetime

PSSSYS = int(next(iter(^PS(59.7,0))))
if int(^PS(59.7,PSSSYS,80).split("^")[2]) != 3:
    print("\nDosage conversion is not complete, cannot install!\n")
    XPDABORT = 2
else:
    PSSTIMEZ = None
    ^XTMP("PSSTIMEX") = {}
    X1 = datetime.date.today()
    X2 = +30
    PSSTIMEZ = (X1 + datetime.timedelta(days=X2)).strftime("%Y%m%d")
    ^XTMP("PSSTIMEX",0) = PSSTIMEZ + "^" + datetime.date.today().strftime("%Y%m%d")
    ^XTMP("PSSTIMEX","START") = datetime.datetime.now()