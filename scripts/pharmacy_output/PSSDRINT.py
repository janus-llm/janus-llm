print("\nThis report gives you a printed copy of locally added drug interactions and their severity. You may queue the report to print, if you wish.\n")
DIC = "^PS(56,"
L = 0
FLDS = "[PSNLOCAL]"
BY = 'NATIONALLY ENTERED=""'
DHD = "LOCALLY ADDED DRUG INTERACTION LIST"
EN1^DIP()
DIC = None
DHD = None
BY = None
FLDS = None
L = None