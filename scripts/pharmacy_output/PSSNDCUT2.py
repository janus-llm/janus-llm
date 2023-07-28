def PSSNDCUT2(PSS50):
    while True:
        OPS1()
        
def OPS1():
    import os
    import datetime
    import fileinput
    
    NDCSITE = input("Select OUTPATIENT SITE: ")
    NDC1PRE = ""
    NDC2PRE = ""
    NDCAR = {}
    QUIT = False
    
    if not os.path.isfile("DRUG.txt"):
        print("No valid NDCs found.")
        return
        
    with fileinput.FileInput("DRUG.txt", inplace=True, backup=".bak") as file:
        for line in file:
            if line.startswith("Field 31 - NDC"):
                NDC = line.split(" - ")[1]
                NDCAR[1] = NDC
            elif line.startswith("Field 2 - NDC CODE"):
                NDC = line.split(" - ")[1]
                NDCAR[1] = NDC
    
    if not NDCAR:
        print("No valid NDCs found.")
        return
    
    NDC = input("Last LOCAL NDC: ")
    if NDC != "" and NDC1PRE != NDC:
        FILENDC(1)
    
    NDC = input("Last CMOP NDC: ")
    if NDC != "" and NDC2PRE != NDC:
        FILENDC(2)
    
    AUDIT()

def FILENDC(FLG):
    with open("NDC.txt", "a") as file:
        file.write(f"{FLG} = {NDC}\n")

def AUDIT():
    NDC1POST = ""
    NDC2POST = ""
    NDCAR = {}
    PSSNO2 = ""
    PSSNOW = datetime.datetime.now()
    
    if NDC1PRE == NDC1POST and NDC2PRE == NDC2POST:
        return
    
    with open("NDC_AUDIT.txt", "a") as file:
        file.write(f"{PSSNOW} - {DUZ}\n")
        if NDC1PRE != NDC1POST:
            file.write(f"NDC1PRE: {NDC1PRE}\n")
            file.write(f"NDC1POST: {NDC1POST}\n")
        if NDC2PRE != NDC2POST:
            file.write(f"NDC2PRE: {NDC2PRE}\n")
            file.write(f"NDC2POST: {NDC2POST}\n")