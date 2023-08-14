def PSSNOUNR():
    print("\nThis report shows the Dosage Forms and Nouns, along with the package use for")
    print("each Noun and the resulting Local Possible Dosage.\n")
    IOP, %ZIS, POP = None, None, None
    %ZIS = "QM"
    ^%ZIS()
    if POP:
        print("\nNothing queued to print.\n")
        return
    if IO("Q"):
        ZTRTN = "START^PSSNOUNR"
        ZTDESC = "Dosage Form/Noun Report"
        ^%ZTLOAD()
        %ZIS = None
        print("\nReport queued to print.\n")
        return

def START():
    PSSOUT = 0
    PSSDV = "C" if IOST[0] == "C" else "P"
    PSSCT = 1
    PSSLINE = "-" * 78
    NOHD()
    PSSDF = ""
    while True:
        PSSDF = $O(^PS(50.606,"B",PSSDF))
        if PSSDF == "" or PSSOUT:
            break
        PSSN = 0
        while True:
            PSSN = $O(^PS(50.606,"B",PSSDF,PSSN))
            if not PSSN or PSSOUT:
                break
            PSSMDF = GETMDF(PSSN)
            if ($Y+5)>IOSL:
                NOHD()
                if PSSOUT:
                    break
            print("\n" + $P(^PS(50.606,PSSN,0), "^"), end="")
            if $L(PSSMDF):
                print(" [" + PSSMDF + "]", end="")
            else:
                print(" ", end="")
            PSSDAR = {}
            PSSDUP = 0
            while True:
                PSSDUP = $O(^PS(50.606,PSSN,"DUPD",PSSDUP))
                if not PSSDUP:
                    break
                if $P($G(^(PSSDUP,0)), "^"):
                    PSSDAR($P($G(^(0)), "^")) = ""
            if $O(PSSDAR(0)):
                print(" " * 68, end="")
                PSSX = 0
                while True:
                    PSSX = $O(PSSDAR(PSSX))
                    if not PSSX:
                        break
                    print(PSSX, end="")
                    if $O(PSSDAR(PSSX)):
                        print(",", end="")
            if ($Y+5)>IOSL:
                NOHD()
                if PSSOUT:
                    break
            PSSNFLAG = 0
            PSSNN = 0
            while True:
                PSSNN = $O(^PS(50.606,PSSN,"NOUN",PSSNN))
                if not PSSNN or PSSOUT:
                    break
                PSSNAME = $P($G(^(PSSNN,0)), "^")
                PSSPAK = $P($G(^(0)), "^", 2)
                if PSSNAME != "":
                    PSSNFLAG = 1
                    if ($Y+5)>IOSL:
                        NOHD()
                        if PSSOUT:
                            break
                    if not $O(PSSDAR(0)):
                        print(" " * 2 + PSSNAME, end="")
                        if not PSSPAK:
                            print(" " * 42 + "(No package)")
                        else:
                            print(" " * (61 - len(PSSPAK)) + PSSPAK + "--> " + PSSNAME)
                    else:
                        if not PSSPAK:
                            print(" " * 2 + PSSNAME + " " * 61 + "(No package)")
                        else:
                            print(" " * 2 + PSSNAME + " " * (61 - len(PSSPAK)) + PSSPAK)
                        PSSZC = 1
                        PSSZ = 0
                        while True:
                            PSSZ = $O(PSSDAR(PSSZ))
                            if not PSSZ or PSSOUT:
                                break
                            if PSSZC == 1:
                                PARN()
                                print("--> " + PSSZ + " " + (PSSXN if $G(PSSXN) != "" else PSSNAME), end="")
                                PSSZC += 1
                            else:
                                if ($Y+5)>IOSL:
                                    NOHD()
                                    if PSSOUT:
                                        break
                                PARN()
                                print(" " * 61 + (PSSPAK if $L($G(PSSPAK))>1 else " " + $G(PSSPAK)) + "--> " + PSSZ + " " + (PSSXN if $G(PSSXN) != "" else PSSNAME))
            if not $G(PSSNFLAG):
                print(" " * 2 + "(No Nouns)")
    if not $G(PSSOUT):
        if $G(PSSDV) == "C":
            print("\nEnd of Report.")
            DIR = {}
            DIR(0) = "E"
            DIR("A") = "Press Return to continue"
            ^DIR
    if $G(PSSDV) == "C":
        print("\n")
    else:
        ^IOF
    PSSDF = None
    PSSN = None
    PSSOUT = None
    PSSLINE = None
    PSSDV = None
    PSSCT = None
    PSSDAR = None
    PSSDUP = None
    PSSX = None
    PSSNN = None
    PSSNFLAG = None
    PSSNAME = None
    PSSNODE = None
    PSSPAK = None
    PSSZ = None
    PSSZC = None
    PSSXN = None
    PSSXNX = None
    ^%ZISC
    if $D(ZTQUEUED):
        ^ZTREQ = "@"

def NOHD():
    if $G(PSSDV) == "C" and $G(PSSCT) != 1:
        DIR = {}
        DIR(0) = "E"
        DIR("A") = "Press Return to continue, '^' to exit"
        ^DIR
        if not Y:
            PSSOUT = 1
            return
    ^IOF
    print("Dosage Form [RxNorm Name]", end="")
    print(" " * 40 + "Dispense Units per Dose", end="")
    print(" " * 69 + "PAGE: " + $G(PSSCT))
    PSSCT += 1
    # print("RxNorm Dose Form")
    print(" " * 2 + "Noun(s)" + " " * 36 + "Package-->Local Possible Dosage")
    print(PSSLINE)

def PARN():
    if $G(PSSNAME) == "":
        return
    if $L(PSSNAME) <= 3:
        return
    PSSXNX = $E(PSSNAME, ($L(PSSNAME) - 2), $L(PSSNAME))
    if $G(PSSXNX) == "(S)" or $G(PSSXNX) == "(s)":
        if $G(PSSZ) <= 1:
            PSSXN = $E(PSSNAME, 1, ($L(PSSNAME) - 3))
        if $G(PSSZ) > 1:
            PSSXN = $E(PSSNAME, 1, ($L(PSSNAME) - 3)) + $E(PSSXNX, 2)

def GETMDF(PSSDFI):
    PSSMDFN = ""
    PSSMDFI = $P($G(^PS(50.606,+$G(PSSDFI),"MASTER")), "^")
    if $L(PSSMDFI):
        PSSMDFN = $P($G(^PSMDF(50.60699,PSSMDFI,0)), "^")
    return PSSMDFN

PSSNOUNR()