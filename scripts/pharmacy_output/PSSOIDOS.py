def PSSOIDOS():
    PSSHOW = input("Print Report for (A)ll or (S)elect a Range (default=S): ")
    if PSSHOW == "A":
        PSSBEG = "A"
        PSSEND = "Z"
        PSSSRT = "A"
        DEV()
    else:
        PSSBEG = input("Enter the beginning letter or range: ")
        PSSEND = input("Enter the ending letter of the range: ")
        PSSSRT = "X"
        DEV()

def DEV():
    print()
    print("Report will be for items starting with the letter", PSSBEG, "and ending with items starting with the letter", PSSEND + ".")
    print()

def START():
    print("Start function")
    # rest of the code

def HD():
    print("Header function")
    # rest of the code

PSSOIDOS()