# PSS219PO - AITC/BWF-Post Install routine for patch PSS*1*219 - 11/24/2017
# 1.0;PHARMACY DATA MANAGEMENT;**219**;9/30/97;Build 14

def POSTINIT():
    FBUCC = None
    PATCH = None
    FBUCC = next((item for item in range(len(^PS(50.606)) if ^PS(50.606)[item] == "FILM,BUCCAL"), None)
    PATCH = next((item for item in range(len(^PS(50.606)) if ^PS(50.606)[item] == "PATCH"), None)
    PUT^XPAR("PKG","PSS BUPRENORPHINE PAIN DFS",1,FBUCC)
    PUT^XPAR("PKG","PSS BUPRENORPHINE PAIN DFS",2,PATCH)
    return